"""
Brevo (formerly Sendinblue) email backend.

Works over HTTPS (port 443) — never blocked by college/ISP firewalls.
Free plan: 300 emails/day, no credit card required.

Setup:
    1. Sign up free at https://app.brevo.com/
    2. Go to: Account → SMTP & API → API Keys → Generate a new API key
    3. Set in .env:
           BREVO_API_KEY=xkeysib-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
           SMTP_FROM_EMAIL=your_email@gmail.com

Config keys needed in .env:
    BREVO_API_KEY    your Brevo API key (starts with xkeysib-)
    SMTP_FROM_EMAIL  the sender address (must be verified in Brevo or any address on free plan)
"""
import httpx
import config


BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def send_via_brevo(to_email: str, subject: str, body: str) -> str:
    if not config.BREVO_API_KEY:
        raise ValueError(
            "BREVO_API_KEY is not set in .env.\n"
            "Sign up free at https://app.brevo.com/ and add your API key."
        )

    payload = {
        "sender": {"email": config.SMTP_FROM_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": body,
    }
    headers = {
        "api-key": config.BREVO_API_KEY,
        "Content-Type": "application/json",
    }

    response = httpx.post(BREVO_API_URL, json=payload, headers=headers, timeout=20)

    if response.status_code in (200, 201):
        return f"Email sent to {to_email} via Brevo."

    raise RuntimeError(
        f"Brevo API error {response.status_code}: {response.text}"
    )
