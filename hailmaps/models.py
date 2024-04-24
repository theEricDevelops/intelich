from django.contrib.gis.db import models
from django.conf import settings

class Map(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} created on {self.date_time_created.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name_plural = "Maps"
        app_label = "hailmaps"

class MapAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.map.name} on {self.access_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        app_label = 'hailmaps'

class HailEvents(models.Model):
    location = models.PointField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    size = models.FloatField()
    date_time_event = models.DateTimeField()
    date_time_updated = models.DateTimeField(auto_now=True)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.size} inch hail event at {self.location} on {self.date_time_event.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        unique_together = ('location', 'size', 'date_time_event')
        verbose_name_plural = "Hail Events"
        app_label = "hailmaps"

class HailmapsDataSource(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('csv_file', 'CSV File'),
        ('api', 'API'),
        ('webpage', 'Webpage'),
    ]

    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    file_path = models.CharField(max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.source_type})"
    
    class Meta:
        verbose_name = "Hail Map Data Source"
        verbose_name_plural = "Hail Map Data Sources"
        ordering = ['name']
        unique_together = ['name', 'source_type']
        permissions = [
            ("can_manage_data_sources", "Can manage hail map data sources"),
        ]