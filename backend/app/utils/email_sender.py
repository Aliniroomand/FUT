import os, smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@example.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

def send_reset_email(to_email: str, token: str):
    reset_link = f"{FRONTEND_URL}/reset-password/{token}"
    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(f"Click here to reset your password:\n\n{reset_link}\n")

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    # برای سرور Debug فقط ارسال پیام بدون TLS یا لاگین
    if SMTP_USER and SMTP_PASS:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
    server.send_message(msg)
    server.quit()
