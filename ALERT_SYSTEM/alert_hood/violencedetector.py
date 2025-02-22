import os
from django.core.mail import send_mail
from django.conf import settings
import time

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
    recipient_list = ['rojanadhikari02@gmail.com']  # Authority email address

    try:
        print("Sending alert email...")  # Log before sending
        send_mail(subject, message, from_email, recipient_list)
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

import os
import time
from django.core.mail import send_mail
from django.conf import settings

def send_alert():
    """
    Function to send an email alert if violence is detected.
    """
    subject = "Violence Alert"
    message = "Violence detected. Please take necessary action."
    from_email = os.environ.get('EMAIL_HOST_USER')
    recipient_list = ['rojanadhikari02@gmail.com']  # Authority email address

    try:
        print("Sending alert email...")
        send_mail(subject, message, from_email, recipient_list)
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_violence():
    """
    Function to check the pose detection file and send alert if violence is detected.
    Returns 1 if no violence is detected, else 0.
    """
    file_path = os.path.join(settings.BASE_DIR, '/Users/lalitramanmishra/Music/Project_mini/ALERT_SYSTEM/alert_hood/rojan.txt')  # Using relative path

    # Debug: Print the file path to verify
    print(f"Checking file at: {file_path}")

    try:
        # Check if the file exists at the specified path
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                result = file.read().strip().replace(" ", "")  # Remove spaces between numbers and trim

                print(f"Pose detection result: {result}")  # Log the result

                # Check if '0' exists in the result, indicating violence detected
                if '0' in result:  # Violence detected
                    send_alert()  # Trigger email alert
                    return 0  # Return 0 to indicate violence detected
                else:
                    return 1  # Return 1 to indicate no violence detected
        else:
            print(f"File not found at path: {file_path}")
            return 1  # Default to no violence if the file does not exist
    except Exception as e:
        print(f"Error reading the file: {e}")
        return 1  # Default to no violence if there's an error reading the file

# Periodically check the file every 4 seconds
while True:
    check_violence()  # Check if violence is detected
    time.sleep(4)  # Wait for 4 seconds before checking again
