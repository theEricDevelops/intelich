from django.db import models

# Create your models here.
class AdminInterfaceSettings(models.Model):
    site_header = models.CharField(max_length=255, default='IntelICH Administration')
    site_title = models.CharField(max_length=255, default='IntelICH site admin')
    index_title = models.CharField(max_length=255, default='Site administration')

    def __str__(self):
        return "Admin Interface Settings"