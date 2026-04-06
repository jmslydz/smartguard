from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    building_type = models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Appliance(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    appliance_type = models.CharField(max_length=50)
    rated_power_kw = models.FloatField()
    is_critical = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Sensor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.serial_number

class EnergyReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power_kw = models.FloatField()
    power_factor = models.FloatField()
    frequency = models.FloatField()

class Anomaly(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    anomaly_type = models.CharField(max_length=100)
    detected_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=50)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)

class Alert(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    anomaly = models.ForeignKey(Anomaly, on_delete=models.CASCADE)
    alert_message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_acknowledged = models.BooleanField(default=False)
