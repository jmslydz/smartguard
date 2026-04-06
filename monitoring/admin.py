from django.contrib import admin
from .models import Building, Appliance, Sensor, EnergyReading, Anomaly, Alert

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'building_type', 'address', 'created_at')
    search_fields = ('name', 'address')

@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'appliance_type', 'rated_power_kw', 'is_critical')
    list_filter = ('building', 'is_critical')

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'building', 'location', 'sensor_type', 'is_active')
    list_filter = ('is_active', 'building')

@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'appliance', 'timestamp', 'voltage', 'current', 'power_kw')

@admin.register(Anomaly)
class AnomalyAdmin(admin.ModelAdmin):
    list_display = ('anomaly_type', 'building', 'sensor', 'severity', 'detected_at', 'resolved')
    list_filter = ('severity', 'resolved')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('building', 'alert_message', 'sent_at', 'is_acknowledged')
    list_filter = ('is_acknowledged',)
