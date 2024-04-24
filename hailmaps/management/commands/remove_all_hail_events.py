from django.core.management.base import BaseCommand
from hailmaps.models import HailEvents

class Command(BaseCommand):
    help = 'Removes all HailEvents from the database.'

    def handle(self, *args, **options):
        deleted_count, _ = HailEvents.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} HailEvents.'))
