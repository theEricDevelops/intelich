from django.db.models import Count
import sys
import os
import django
import logging

sys.path.insert(0, '/mnt/c/users/eric/dev/intelich')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intelich.settings')
django.setup()

# Configure the logger
logging.basicConfig(filename='process_hail_events.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from hailmaps.models import HailEvents

duplicate_events = HailEvents.objects.values('location', 'size', 'date_time_event').annotate(count=Count('*')).filter(count__gt=1)

for event in duplicate_events:
    events_to_delete = HailEvents.objects.filter(**event).order_by('-date_time_created')[1:]
    events_to_delete.delete()
