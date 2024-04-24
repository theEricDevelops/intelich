from django.contrib.admin import AdminSite
from django.contrib import admin
from django.http import HttpRequest
from .models import AdminInterfaceSettings
from typing import Any

@admin.register(AdminInterfaceSettings)
class AdminInterfaceSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return not AdminInterfaceSettings.objects.exists()
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False

class IICHAdminSite(AdminSite):
    @property
    def site_header(self):
        settings = AdminInterfaceSettings.objects.first()
        return settings.site_header if settings else 'IICH Administration'
    
    @property
    def site_title(self):
        settings = AdminInterfaceSettings.objects.first()
        return settings.site_title if settings else 'IICH site admin'
    
    @property
    def index_title(self):
        settings = AdminInterfaceSettings.objects.first()
        return settings.index_title if settings else 'Site Administration'

iich_admin = IICHAdminSite(name='iichadmin')