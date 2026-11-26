"""Settings for the Fyers scripts, read from environment variables (or a .env file).

    FYERS_CLIENT_ID        app id from the Fyers API dashboard, e.g. XXXXXXXX-100
    FYERS_SECRET_KEY       app secret (only needed by access_token.py)
    FYERS_REDIRECT_URI     redirect URL set on the app
    FYERS_AUTH_CODE        auth code from the redirect (only needed by access_token.py)
    FYERS_ACCESS_TOKEN     token printed by access_token.py; valid for one trading day
    GOOGLE_SERVICE_ACCOUNT path to the service-account JSON (default: serviceAccount.json)
    SHEET_NAME             Google Sheet to write to (default: FyersAPI)
    SHARE_WITH             your Google email, so new_sheet.py can share the sheet with you
"""
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def need(name):
    value = os.getenv(name)
    if not value:
        sys.exit(f"Set {name} in your environment or .env file (see config.py).")
    return value


def get(name, default=None):
    return os.getenv(name, default)
