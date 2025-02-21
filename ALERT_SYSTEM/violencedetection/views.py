from django.shortcuts import render
from django.core.mail import send_mail
from ALERT_SYSTEM.alert_hood.violencedetector import send_alert

# Create your views here.
from django.http import JsonResponse
from .pose_model import predict_violence


def detect_violence(request):
    if request.method == "POST":
        pose_data = request.POST.getlist(
            "pose_data[]", []
        )  # Get pose data from request
        pose_data = [float(i) for i in pose_data]  # Convert to float

        result = predict_violence(pose_data)
        return JsonResponse({"violence_detected": result})
    return JsonResponse({"error": "Invalid request"}, status=400)


# Import your existing email function


def detect_violence(request):
    if request.method == "POST":
        pose_data = request.POST.getlist("pose_data[]", [])
        pose_data = [float(i) for i in pose_data]

        result = predict_violence(pose_data)

        if result == 1:
            send_alert()

        return JsonResponse({"violence_detected": result})
    return JsonResponse({"error": "Invalid request"}, status=400)
