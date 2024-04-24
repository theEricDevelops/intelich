from django.core.management.base import BaseCommand
from hailmaps.models import HailEvents
from django.db.models import Count

class Command(BaseCommand):
    help = 'Deduplicate HailEvents based on location, size, and date/time.'

    def handle(self, *args, **options):
        # Identify potential duplicates (get IDs only)
        duplicate_ids = HailEvents.objects.values('location', 'size', 'date_time_event') \
                                        .annotate(count=Count('*')) \
                                        .filter(count__gt=1) \
                                        .values_list('id', flat=True)

        # Iterate through duplicate IDs and delete duplicates (keeping the most recent)
        for event_id in duplicate_ids:
            events_to_delete = HailEvents.objects.filter(id=event_id).order_by('-date_time_created')[1:]
            deleted_count, _ = events_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} duplicate events for event ID: {event_id}'))
