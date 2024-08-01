import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient_email, quiz_link):
    # Define your SMTP server settings and email credentials here
    smtp_server = os.getenv('smtp_server')
    smtp_port = int(os.getenv('smtp_port', 587))  # Default to 587 if not set
    smtp_user = os.getenv('smtp_user')
    smtp_password = os.getenv('smtp_password')

    # Construct the email
    subject = "Your Unique Quiz Link"
    body = f"Please take the quiz by following this link: {quiz_link}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient_email

    try:
        # Connect to the email server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
