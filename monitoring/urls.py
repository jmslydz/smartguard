from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buildings/', views.buildings, name='buildings'),
    path('buildings/<int:building_id>/', views.building_detail, name='building_detail'),
    path('anomalies/', views.anomalies, name='anomalies'),
    path('alert/<int:alert_id>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
    path('anomaly/<int:anomaly_id>/resolve/', views.resolve_anomaly, name='resolve_anomaly'),
]
