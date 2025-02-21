from django.urls import path
from .views import detect_violence

urlpatterns = [
    path("detect/", detect_violence, name="detect_violence"),
]
