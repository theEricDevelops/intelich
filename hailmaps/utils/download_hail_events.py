import os
import requests
import time
import sys
from datetime import datetime, timedelta
from tqdm import tqdm
import django
from django.conf import settings
import logging.config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intelich.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
django.setup()
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

class HailEventDownloader:
    def __init__(self, start_date):
        self.date = start_date
        self.logger = logger

    def download(self, today):
        download_date = today.strftime("%y%m%d")
        file_path = os.path.join(settings.DATA_DIR, 'hail-reports', f'{download_date}_rpts_raw_hail.csv')
        
        if os.path.exists(file_path):
            self.logger.info(f"File already exists for {download_date}")
            return True

        try:
            url = f"https://www.spc.noaa.gov/climo/reports/{download_date}_rpts_raw_hail.csv"
            self.logger.info(f"Starting download for date: {download_date}")
            
            while True:
                response = requests.get(url)
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 10))
                    self.logger.info(f"Rate limited. Waiting {wait_time} seconds before retrying.")
                    time.sleep(wait_time)
                else:
                    response.raise_for_status()  

            with open(file_path, 'wb') as f:
                f.write(response.content)
                self.logger.info(f"Downloaded file for {download_date}")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading data for {download_date}: {str(e)}")
            return False
        return True

    def run(self):
        self.logger.info("Starting Hail Event Downloader")
        today = datetime.today()
        end_date = today - timedelta(days=6)
        total_files = (today - end_date).days + 1
        progress_bar = tqdm(total=total_files, desc="Overall Progress")

        while today >= end_date:
            progress_bar.update(1)
            today -= timedelta(days=1)
        progress_bar.close()

# Usage
downloader = HailEventDownloader(datetime.today())
downloader.run()
