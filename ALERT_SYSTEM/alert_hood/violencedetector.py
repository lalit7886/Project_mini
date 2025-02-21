# violencedetector.py
import os
from django.core.mail import send_mail
from django.conf import settings
from .realtime import detect

# Fetch email credentials from environment variables
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


def send_alert():
    """
    Function to send an email alert if violence is detected.
    """
    subject = "Violence Alert"
    message = "K xa yaar rojan dai"
    from_email = EMAIL_HOST_USER
    recipient_list = ["rojanadhikari02@gmail.com"]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")
