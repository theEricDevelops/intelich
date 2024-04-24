from django.core.management.base import BaseCommand, CommandError
import logging
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from hailmaps.models import HailEvents

# Set up logging
logging.basicConfig(filename='update_hail_events.log', level=logging.INFO)
logger = logging.getLogger(__name__)

tf = TimezoneFinder()
geolocator = Nominatim(user_agent="hail_events_app")  # Create geolocator

class Command(BaseCommand):
    help = 'Updates timezones and location information for hail events.'

    def handle(self, *args, **options):
        try:
            update_timezones_and_locations()
            self.stdout.write(self.style.SUCCESS('Successfully updated hail events.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating hail events: {str(e)}'))
            raise CommandError('Update failed')

def update_timezones_and_locations():
    hail_events = HailEvents.objects.filter(timezone="")  # Get events without timezones

    for event in hail_events:
        longitude = event.location.x
        latitude = event.location.y

        # Determine and update timezone
        try:
            timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
            if timezone_str:
                event.timezone = timezone_str
            else:
                logger.warning(f"Could not determine timezone for hail event at ({latitude}, {longitude}) on {event.date_time_event}")
        except Exception as e:
            logger.error(f"Error determining timezone: {str(e)}")

        # Geocode and update location information
        try:
            location = geolocator.reverse((latitude, longitude))
            if location:
                address = location.raw['address']
                event.city = address.get('city', '')
                event.state = address.get('state', '')
                event.zip_code = address.get('postcode', '')
            else:
                logger.warning(f"Could not geocode hail event at ({latitude}, {longitude}) on {event.date_time_event}")
        except Exception as e:
            logger.error(f"Error geocoding location: {str(e)}")

        event.save()
