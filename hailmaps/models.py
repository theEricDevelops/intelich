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