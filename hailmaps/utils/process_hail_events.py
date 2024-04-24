import os
import sys
import logging
import csv
from datetime import datetime, timedelta
import django
from django.contrib.gis.geos import Point
import re
from django.conf import settings
import logging.config
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intelich.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
django.setup()
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

from hailmaps.models import HailEvents, HailmapsDataSource

def process_csv_files():
    data_dir = os.path.join(settings.DATA_DIR, 'hail-reports')
    today = datetime.today()
    date_range = [today.strftime('%y%m%d')] + [(today - timedelta(days=i)).strftime('%y%m%d') for i in range(1, 8)]

    # Get a list of files we already have
    existing_dates = set(
        ds.file_path.split('_')[0]
        for ds in HailmapsDataSource.objects.filter(
            source_type='csv_file',
            date__range=date_range
            )
    )

    for days_ago in range(7):
        target_date = today - timedelta(days=days_ago)
        download_date_str = target_date.strftime('%y%m%d')

        if download_date_str in existing_dates:
            logger.info(f"Data source already exists for {download_date_str}, skipping...")
            continue
        elif download_date_str not in existing_dates:
            logger.info(f"Data source does not exist for {download_date_str}, processing...")
        
            # Get the file path
            file_path = os.path.join(data_dir, f"{download_date_str}_rpts_raw_hail.csv")

            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        date_time_str = row['Time']
                        date_time_obj = datetime.strptime(date_time_str, '%H%M').replace(
                            year=2000 + int(download_date_str), month=int(download_date_str[2:4]), day=int(download_date_str[4:6])
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
            
            if not errors_occured:
                # Add to the HailmapsDataSource table
                HailmapsDataSource.objects.create(
                    name = f"Hail Report - {download_date_str}",
                    source_type = 'csv_file',
                    description = f'NOAA Hail Events CSV File for {download_date_str}',
                    url = f"https://www.spc.noaa.gov/climo/reports/{download_date_str}_rpts_raw_hail.csv",
                    file_path = file_path,
                    date = download_date_str
                )

process_csv_files()