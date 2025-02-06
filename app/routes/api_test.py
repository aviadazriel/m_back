from typing import List

from fastapi import APIRouter, Depends, HTTPException
from app.configs import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER
from app.utils.mail_utils import send_email_via_gmail

router = APIRouter()




# Get all users
@router.get("/")
def read_users():
    # Replace these with your own details
    RECIPIENT = "aviadazriel2@gmail.com"
    SUBJECT = "Test Email from Python"
    BODY = "Hello! This is a test email sent from Python using an App Password."

    send_email_via_gmail(
        gmail_user=EMAIL_ADDRESS,
        gmail_app_password=EMAIL_PASSWORD,
        recipient=RECIPIENT,
        subject=SUBJECT,
        body=BODY
    )
    print('mail sent')

    # ATTACHMENT_PATH = "path/to/your/file.pdf"  # e.g. "/Users/john/Documents/report.pdf"
    # send_email_with_attachment(
    #     gmail_user=GMAIL_ADDRESS,
    #     gmail_app_password=GMAIL_APP_PASSWORD,
    #     recipient=RECIPIENT,
    #     subject=SUBJECT,
    #     body=BODY,
    #     attachment_path=ATTACHMENT_PATH
    # )
    return "its working"

