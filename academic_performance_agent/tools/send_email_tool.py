"""
Email dispatch tool — routes to the configured backend.

Switch backend by setting EMAIL_BACKEND in .env:

    EMAIL_BACKEND=brevo   ← recommended (HTTPS, works everywhere, free)
    EMAIL_BACKEND=smtp    ← use when on a network that allows SMTP ports 587/465
    EMAIL_BACKEND=gmail   ← Gmail API via OAuth2 (requires one-time browser login)

All backends expose the same interface: send_email(to, subject, body).
"""
from langchain.tools import tool
import config


def _dispatch(to_email: str, subject: str, body: str) -> str:
    backend = config.EMAIL_BACKEND.lower().strip()

    if backend == "brevo":
        from tools.brevo_sender import send_via_brevo
        return send_via_brevo(to_email, subject, body)

    elif backend == "smtp":
        from tools.smtp_sender import send_via_smtp
        return send_via_smtp(to_email, subject, body)

    elif backend == "gmail":
        from tools.gmail_sender import send_via_gmail_api
        return send_via_gmail_api(to_email, subject, body)

    else:
        raise ValueError(
            f"Unknown EMAIL_BACKEND='{backend}'. "
            "Valid options: brevo | smtp | gmail"
        )


@tool
def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email to a single recipient using the configured email backend.
    Use this as the FINAL step after drafting a message to actually deliver it.

    Args:
        to_email: recipient's email address
        subject:  email subject line
        body:     full plain-text email body — write it fully formed and
                  professional before calling this tool; this tool does not
                  edit or improve the content, it only sends exactly what you give it.
    """
    try:
        return _dispatch(to_email, subject, body)
    except Exception as e:
        return f"FAILED to send email to {to_email}: {e}"
