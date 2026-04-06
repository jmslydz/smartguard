from django.shortcuts import render, redirect
from .models import Building, Sensor, Anomaly, Alert

def home(request):
    buildings = Building.objects.count()
    sensors = Sensor.objects.filter(is_active=True).count()
    anomalies = Anomaly.objects.filter(resolved=False).count()
    alerts = Alert.objects.filter(is_acknowledged=False).count()
    return render(request, 'monitoring/home.html', {
        'buildings': buildings,
        'sensors': sensors,
        'anomalies': anomalies,
        'alerts': alerts
    })

def buildings(request):
    return render(request, 'monitoring/buildings.html', {'buildings': Building.objects.all()})

def building_detail(request, building_id):
    building = Building.objects.get(id=building_id)
    sensors = Sensor.objects.filter(building=building)
    return render(request, 'monitoring/building_detail.html', {
        'building': building,
        'sensors': sensors
    })

def anomalies(request):
    return render(request, 'monitoring/anomalies.html', {'anomalies': Anomaly.objects.all()})

def acknowledge_alert(request, alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.is_acknowledged = True
    alert.save()
    return redirect('home')

def resolve_anomaly(request, anomaly_id):
    from django.utils import timezone
    anomaly = Anomaly.objects.get(id=anomaly_id)
    anomaly.resolved = True
    anomaly.resolved_at = timezone.now()
    anomaly.save()
    return redirect('anomalies')
