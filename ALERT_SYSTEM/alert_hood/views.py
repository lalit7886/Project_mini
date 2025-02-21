# views.py
from django.shortcuts import render
from .violencedetector import check_violence  # Import the check_violence function


def check_violence_view(request):
    violence_detected = check_violence()  # Call the check_violence function

    return render(request, "my_template.html", {"alert": violence_detected})
