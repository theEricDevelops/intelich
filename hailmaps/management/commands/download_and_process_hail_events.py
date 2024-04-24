import os
import csv
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import logging
import requests
from hailmaps.models import HailEvents, HailmapsDataSource
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import time


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Downloads and processes hail event CSV files.'

    def handle(self, *args, **options):
        try:
            today = datetime.today()

            # Get a list of files we already have
            existing_dates = set(
                ds.file_path.split('_')[0]
                for ds in HailmapsDataSource.objects.filter(source_type='csv_file')
            )

            for days_ago in range(7):
                target_date = today - timedelta(days=days_ago)
                download_date_str = target_date.strftime('%y%m%d')

                if download_date_str in existing_dates:
                    logger.info(f"Data source already exists for {download_date_str}, skipping...")
                    continue

                # Download CSV Files (replace with your actual download logic)
                downloader = HailEventDownloader(download_date_str)
                try:
                    downloaded, file_path = downloader.download()
                    if downloaded:
                        logger.info(f"Downloaded data for {download_date_str}")
                    
                        # Get Data Directory
                        data_dir = os.path.join(settings.DATA_DIR, 'hail-reports')
                        file_path = os.path.join(data_dir, f"{download_date_str}_rpts_raw_hail.csv")  
                        with open(file_path, 'r') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                try:
                                    date_time_str = row['Time']
                                    date_time_obj = datetime.strptime(date_time_str, '%H%M').replace(
                                        year=2000 + int(file_path[:2]), month=int(file_path[2:4]), day=int(file_path[4:6])
                                    )
                                    longitude = float(row["LON"])
                                    latitude = float(row["LAT"])
                                    location = Point(longitude, latitude, srid=4326)
                                    size = float(row['Size(1/100in.)']) / 100  # Convert size to inches
                                    timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude) or 'UTC'

                                    geolocator = Nominatim(user_agent="hailmaps")
                                    try:
                                        location_data = geolocator.reverse((latitude, longitude), language='en')
                                        address = location_data.raw.get('address', {})
                                        city = address.get('city', '')
                                        state = address.get('state', '')
                                        zip_code = address.get('postcode', '')
                                    except Exception as e:
                                        logger.error(f"Error during geocoding: {str(e)}")
                                        city = state = zip_code = ''
                                    try:
                                        # Create HailEvent object
                                        HailEvents.objects.create(
                                            location=location,
                                            size=size,
                                            date_time_event=date_time_obj,
                                            city=city,
                                            state=state,
                                            zip_code=zip_code,
                                            timezone=timezone,
                                        )

                                    except Exception as e:
                                        logger.error(f"Error creating HailEvent object: {str(e)}")
                                        errors_occured = True

                                except Exception as e:
                                    # Handle exceptions (e.g., log errors)
                                    logger.error(f"Error processing row: {row} - {str(e)}")
                                    errors_occured = True

                        try:
                            # Create a data source object
                            HailmapsDataSource.objects.create(
                                name=f"Hail Report - {download_date_str}",
                                source_type='csv_file',
                                description="NOAA Hail Report",
                                file_path=file_path,
                                date=download_date_str,
                            )

                        except Exception as e:
                            logger.error(f"Error creating data source object: {str(e)}")
                            errors_occured = True
                            continue

                except Exception as e:
                    logger.error(f"Error downloading data file {file_path}: {str(e)}")
                    continue

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error processing hail events: {str(e)}'))
            return

class HailEventDownloader:
    def __init__(self, download_date):
        self.date = download_date

    def download(self):
        
        # Use Django's file storage API
        file_name = f'{self.date}_rpts_raw_hail.csv'
        file_path = os.path.join(settings.DATA_DIR, 'hail-reports', file_name)
        
        if os.path.exists(file_path):
            logger.info(f"File already exists for {self.date}")
            return True, file_path

        try:
            url = f"https://www.spc.noaa.gov/climo/reports/{self.date}_rpts_raw_hail.csv"
            logger.info(f"Starting download for date: {self.date}")
            
            while True:
                response = requests.get(url)
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 10))
                    logger.info(f"Rate limited. Waiting {wait_time} seconds before retrying.")
                    time.sleep(wait_time)
                else:
                    response.raise_for_status()  

            try:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    logger.info(f"Downloaded file for {self.date}")
            except IOError as e:
                logger.error(f"Error writing file: {str(e)}")
                return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading data for {self.date}: {str(e)}")
            return False, file_path
        
        return True, file_path