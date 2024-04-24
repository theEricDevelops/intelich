import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hailmaps.models import HailmapsDataSource

class Command(BaseCommand):
    help = 'Adds existing downloaded CSV files as HailmapsDataSource objects.'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.DATA_DIR, 'hail-reports')  # Path to CSV files

        file_count = 0  # Initialize file counter

        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                date_str = filename.split('_')[0]  # Extract date from filename
                file_path = os.path.join(data_dir, filename)

                # Create HailmapsDataSource object
                HailmapsDataSource.objects.create(
                    name=f"Hail Report - {date_str}",
                    source_type="csv_file",
                    description="NOAA Hail Report", 
                    file_path=file_path 
                )

                file_count += 1  # Increment file counter

        self.stdout.write(self.style.SUCCESS(f'Successfully added {file_count} existing data sources.')) 
