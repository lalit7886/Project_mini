# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.check_violence_view, name="check_violence"
    ),  # Add the route for violence check
]
