from typing import List

from fastapi import APIRouter, Depends, HTTPException
from app.configs import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SERVER
from app.utils.mail_utils import send_email_via_gmail, send_email_with_attachment
from fastapi import FastAPI, File, UploadFile, Form

router = APIRouter()


@router.get("/")
def test_api():
    return 'THIS IS A TEST METHOD'

@router.post("/")
async def send_email(
    bank: str = Form(...),
    fullName: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    file: UploadFile = File(None)  # File is optional; use None if not provided
     ):
    # Replace these with your own details
    RECIPIENT = "aviadazriel2@gmail.com"
    SUBJECT = "Test Email from Python"
    BODY = f"file.filename: {file.filename}  phone: {phone} Hello! This is a test email sent from Python using an App Password.\nbank: {bank} fullName: {fullName} email:{email}"

    if not file:
        return "no have file to upload"

    await send_email_with_attachment(
        gmail_user=EMAIL_ADDRESS,
        gmail_app_password=EMAIL_PASSWORD,
        recipient=RECIPIENT,
        subject=SUBJECT,
        body=BODY,
        file=file
    )
    print('mail sent')
    return "its working"

