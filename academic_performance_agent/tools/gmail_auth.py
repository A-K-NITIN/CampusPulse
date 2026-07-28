"""
Standalone script to do the one-time Gmail OAuth2 browser login.

Run this ONCE before using the agent:
    python -m tools.gmail_auth

A browser window opens → sign in with your Gmail → grant permission.
The token is saved to credentials/gmail_token.json automatically.
After that, the agent sends emails without any browser prompts.
"""
from tools.gmail_sender import _get_credentials

if __name__ == "__main__":
    creds = _get_credentials()
    print("✅ Gmail authenticated successfully!")
    print(f"   Token saved. You won't need to do this again unless the token is deleted.")
