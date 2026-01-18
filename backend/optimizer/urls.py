from django.urls import path
from .views import OptimizeBulletView, HealthView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("optimize/", OptimizeBulletView.as_view(), name="optimize"),
]
