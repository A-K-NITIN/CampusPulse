"""
Email dispatch tool — the only tool in this project that actually sends
something. Every functionality (1, 2, 3, 4, 6, 7) ends by calling this.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from langchain.tools import tool
import config


def _send(to_email: str, subject: str, body: str) -> str:
    msg = MIMEMultipart()
    msg["From"] = config.SMTP_FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_FROM_EMAIL, to_email, msg.as_string())

    return f"Email sent to {to_email} with subject '{subject}'."


@tool
def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email to a single recipient. Use this as the FINAL step after
    drafting a message, to actually deliver it.

    Args:
        to_email: recipient's email address
        subject: email subject line
        body: full plain-text email body — write it fully formed and
              professional before calling this tool; this tool does not
              edit or improve the content, it only sends exactly what you give it.
    """
    try:
        return _send(to_email, subject, body)
    except Exception as e:
        return f"FAILED to send email to {to_email}: {e}"
