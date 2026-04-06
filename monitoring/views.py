from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Building, Sensor, Anomaly, Alert

def home(request):
    buildings = Building.objects.count()
    sensors = Sensor.objects.filter(is_active=True).count()
    anomalies = Anomaly.objects.filter(resolved=False).count()
    alerts = Alert.objects.filter(is_acknowledged=False).count()
    return HttpResponse(f"""
        <h1>SmartGuard Dashboard</h1>
        <h2>Stats:</h2>
        <ul>
            <li>Buildings: {buildings}</li>
            <li>Active Sensors: {sensors}</li>
            <li>Active Anomalies: {anomalies}</li>
            <li>Active Alerts: {alerts}</li>
        </ul>
        <p><a href="/buildings/">View Buildings</a></p>
        <p><a href="/anomalies/">View Anomalies</a></p>
        <p><a href="/admin/">Admin Panel</a></p>
    """)

def buildings(request):
    buildings = Building.objects.all()
    html = "<h1>Buildings</h1><ul>"
    for b in buildings:
        html += f"<li><a href='/buildings/{b.id}/'>{b.name}</a> ({b.building_type})</li>"
    html += "</ul><p><a href='/'>Back</a></p>"
    return HttpResponse(html)

def building_detail(request, building_id):
    building = Building.objects.get(id=building_id)
    sensors = Sensor.objects.filter(building=building)
    html = f"""
        <h1>{building.name}</h1>
        <p>Type: {building.building_type}</p>
        <p>Address: {building.address}</p>
        <h2>Sensors ({sensors.count()}):</h2>
        <ul>
    """
    for s in sensors:
        html += f"<li>{s.serial_number} - {s.location} ({s.sensor_type})</li>"
    html += "</ul><p><a href='/buildings/'>Back</a></p>"
    return HttpResponse(html)

def anomalies(request):
    anomalies = Anomaly.objects.all()
    html = "<h1>Anomalies</h1><ul>"
    for a in anomalies:
        status = "Resolved" if a.resolved else "Pending"
        html += f"<li>{a.anomaly_type} - {a.severity} - {status} ({a.building.name})</li>"
    html += "</ul><p><a href='/'>Back</a></p>"
    return HttpResponse(html)

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
