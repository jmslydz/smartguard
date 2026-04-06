import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from monitoring.models import Building, Sensor, EnergyReading, Anomaly

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create 3 Buildings
        buildings_data = [
            {'name': 'Main Campus Building', 'building_type': 'Educational', 'address': '123 University Ave, College Station, TX 77840'},
            {'name': 'Research Laboratory', 'building_type': 'Laboratory', 'address': '456 Science Park, College Station, TX 77841'},
            {'name': 'Student Housing Complex', 'building_type': 'Residential', 'address': '789 Dormitory Lane, College Station, TX 77842'},
        ]
        
        buildings = []
        for data in buildings_data:
            building, created = Building.objects.get_or_create(name=data['name'], defaults=data)
            buildings.append(building)
            self.stdout.write(f"{'Created' if created else 'Found'} building: {building.name}")

        # Create 2 sensors per building
        sensor_types = ['Current Sensor', 'Voltage Sensor', 'Power Meter', 'Energy Monitor']
        locations = ['Main Panel', 'Sub-Panel A', 'Sub-Panel B', 'Kitchen', 'Server Room', 'HVAC Unit']

        sensors = []
        for building in buildings:
            for i in range(2):
                sensor_data = {
                    'building': building,
                    'serial_number': f'SN-{buildings.index(building)}-{i}',
                    'location': random.choice(locations),
                    'sensor_type': random.choice(sensor_types),
                    'is_active': True,
                }
                sensor, created = Sensor.objects.get_or_create(
                    serial_number=sensor_data['serial_number'],
                    defaults=sensor_data
                )
                sensors.append(sensor)
                self.stdout.write(f"{'Created' if created else 'Found'} sensor: {sensor.serial_number}")

        # Create 100+ energy readings per sensor
        anomaly_types = ['Voltage Spike', 'Overload', 'Power Factor Anomaly', 'Frequency Deviation', 'High Current Draw', 'Power Surge']
        severities = ['Low', 'Medium', 'High']
        
        anomaly_count = 0
        for sensor in sensors:
            # Get existing reading count for this sensor
            existing_count = EnergyReading.objects.filter(sensor=sensor).count()
            
            # Create readings to reach 100+ per sensor
            readings_to_create = max(0, 120 - existing_count)
            
            base_time = datetime.now() - timedelta(days=7)
            for i in range(readings_to_create):
                timestamp = base_time + timedelta(hours=i)
                reading = EnergyReading(
                    sensor=sensor,
                    appliance=None,
                    timestamp=timestamp,
                    voltage=random.uniform(110, 125),
                    current=random.uniform(5, 50),
                    power_kw=random.uniform(0.5, 10),
                    power_factor=random.uniform(0.7, 0.99),
                    frequency=random.uniform(59.5, 60.5),
                )
                reading.save()
            
            self.stdout.write(f"Created {readings_to_create} readings for sensor {sensor.serial_number}")

        # Create at least 10 anomaly records
        for i in range(15):
            sensor = random.choice(sensors)
            building = sensor.building
            detected_at = datetime.now() - timedelta(days=random.randint(0, 30))
            
            anomaly_data = {
                'sensor': sensor,
                'building': building,
                'anomaly_type': random.choice(anomaly_types),
                'detected_at': detected_at,
                'severity': random.choice(severities),
                'description': f'Detected {random.choice(anomaly_types).lower()} in {sensor.location} at {building.name}. Power factor: {random.uniform(0.5, 0.7):.2f}',
                'resolved': random.choice([True, False]),
            }
            
            anomaly, created = Anomaly.objects.get_or_create(
                sensor=sensor,
                building=building,
                anomaly_type=anomaly_data['anomaly_type'],
                detected_at=anomaly_data['detected_at'],
                defaults=anomaly_data
            )
            if created:
                anomaly_count += 1
                if anomaly.resolved:
                    anomaly.resolved_at = detected_at + timedelta(hours=random.randint(1, 48))
                    anomaly.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database!'))
        self.stdout.write(f'- Buildings: {Building.objects.count()}')
        self.stdout.write(f'- Sensors: {Sensor.objects.count()}')
        self.stdout.write(f'- Energy Readings: {EnergyReading.objects.count()}')
        self.stdout.write(f'- Anomalies: {Anomaly.objects.count()}')
