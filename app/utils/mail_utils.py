
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from fastapi import  File, UploadFile

def send_email_via_gmail(
    gmail_user: str,
    gmail_app_password: str,
    recipient: str,
    subject: str,
    body: str
) -> None:
    """
    Send an email from a Gmail account using SMTP and an App Password.

    :param gmail_user: Your Gmail address (e.g. 'example@gmail.com')
    :param gmail_app_password: The 16-character app password from your Google account
    :param recipient: The recipient's email address
    :param subject: The subject of the email
    :param body: The body text of the email
    """
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server (port 587 for TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(gmail_user, gmail_app_password)  # Log in with the app password
        server.sendmail(gmail_user, recipient, msg.as_string())
        server.quit()

        print(f"Email successfully sent to {recipient}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")



async def send_email_with_attachment(
    gmail_user: str,
    gmail_app_password: str,
    recipient: str,
    subject: str,
    body: str,
    file: UploadFile = File(None),
    attachment_path: str = None
) -> None:
    """
    Send an email from a Gmail account using SMTP with an optional file attachment.

    :param gmail_user: Your Gmail address (e.g. 'example@gmail.com')
    :param gmail_app_password: The 16-character app password from your Google account
    :param recipient: The recipient's email address
    :param subject: The subject of the email
    :param body: The body text of the email
    :param attachment_path: The file path to the attachment (optional)
    """
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body, 'plain'))

    # If an attachment path is provided, try to attach the file

    if file is not None:
        print("Filename:", file.filename)
        print("Content-Type:", file.content_type)
        # print("File Size in bytes:", len(file_contents))
        mime_part = MIMEBase("application", "pdf")
        # Path("test_upload.pdf").write_bytes(file_contents)

        # 2) Then attach to the email
        mime_part.set_payload(await file.read())
        encoders.encode_base64(mime_part)
        print("Filename:", file.filename)
        mime_part.add_header(
            "Content-Type",
            f'{file.content_type}; name="{file.filename}"'
        )
        mime_part.add_header(
            "Content-Disposition",
            f'attachment; filename="{file.filename}"'
        )
        msg.attach(mime_part)


    try:
        # Connect to Gmail's SMTP server (port 587 for TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        # Log in with the App Password
        server.login(gmail_user, gmail_app_password)
        # Send the email
        server.sendmail(gmail_user, recipient, msg.as_string())
        server.quit()

        print(f"Email successfully sent to {recipient}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

        # if attachment_path and os.path.exists(attachment_path):
        #     try:
        #         with open(attachment_path, 'rb') as attachment_file:
        #             # Create a MIMEBase object
        #             mime_part = MIMEBase('application', 'octet-stream')
        #             mime_part.set_payload(attachment_file.read())
        #
        #         # Encode the payload in Base64
        #         encoders.encode_base64(mime_part)
        #
        #         # Add a header with the attachment file name
        #         filename = os.path.basename(attachment_path)
        #         mime_part.add_header(
        #             'Content-Disposition',
        #             f'attachment; filename="{filename}"'
        #         )
        #
        #         # Attach the MIMEBase object to the email
        #         msg.attach(mime_part)

        # except Exception as e:
        #     print(f"Could not attach file. Error: {e}")