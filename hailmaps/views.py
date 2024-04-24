from django.shortcuts import render
from django.http import HttpResponse
from .models import Map, HailEvents
from django.core.paginator import Paginator
from django.core.serializers import serialize
import pytz
from timezonefinder import TimezoneFinder

# Create your views here.
def index(request):
    hail_events = HailEvents.objects.all().order_by('-date_time_event')

    # Serialize hail event data as GeoJSON
    hail_events_geojson = serialize('geojson', hail_events, geometry_field='location', fields=('size', 'date_time_event'))
 
    context = {'hail_events_geojson': hail_events_geojson}
    return render(request, 'index.html', context)

def new_hailmap(request):
    return HttpResponse("This is the new hailmap page.")

def hail_events(request):
    return HttpResponse("This is the new events page.")