# violencedetector.py
import os
from django.core.mail import send_mail
from django.conf import settings

# Fetch email credentials from environment variables
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

def send_alert():
    """
    Function to send an email alert if violence is detected.
    """
    subject = "Violence Alert"
    message = "K xa yaar rojan dai"
    from_email = EMAIL_HOST_USER
    recipient_list = ['rojanadhikari02@gmail.com'] 

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")

def check_violence():
    """
    Function to simulate violence detection and send alert.
    Returns 1 if violent activity is detected, else 0.
    """
    
    violence_detected = 1 

    if violence_detected == 1:
        send_alert()  

    return violence_detected
