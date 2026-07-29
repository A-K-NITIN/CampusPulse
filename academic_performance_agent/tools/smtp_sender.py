"""
SMTP email backend.

Works when SMTP ports (587 / 465) are NOT blocked by your network.
Tries STARTTLS on port 587 first, falls back to SSL on port 465.

Config keys needed in .env:
    SMTP_HOST        default: smtp.gmail.com
    SMTP_PORT        default: 587
    SMTP_USERNAME    your full Gmail address
    SMTP_PASSWORD    Gmail App Password (NOT your login password)
                     Generate at: https://myaccount.google.com/apppasswords
    SMTP_FROM_EMAIL  same as SMTP_USERNAME (or a display alias)
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_via_smtp(to_email: str, subject: str, body: str) -> str:
    msg = MIMEMultipart()
    msg["From"] = config.SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    raw = msg.as_string()

    errors = []

    # Attempt 1 — STARTTLS on configured port (default 587)
    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=15) as srv:
            srv.starttls()
            srv.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            srv.sendmail(config.SMTP_FROM_EMAIL, to_email, raw)
        return f"Email sent to {to_email} via SMTP (port {config.SMTP_PORT})."
    except Exception as e:
        errors.append(f"Port {config.SMTP_PORT} STARTTLS: {e}")

    # Attempt 2 — SSL on port 465
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(config.SMTP_HOST, 465, context=ctx, timeout=15) as srv:
            srv.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            srv.sendmail(config.SMTP_FROM_EMAIL, to_email, raw)
        return f"Email sent to {to_email} via SMTP (port 465 SSL)."
    except Exception as e:
        errors.append(f"Port 465 SSL: {e}")

    raise ConnectionError(
        f"SMTP failed on all ports — {'; '.join(errors)}\n"
        "Tip: Switch to EMAIL_BACKEND=brevo in .env if SMTP ports are blocked."
    )
