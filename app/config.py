import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "propfirm.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Security & Sessions
SECRET_KEY = "fundeddesk_super_secure_jwt_session_secret_2026"
SESSION_COOKIE_NAME = "fundeddesk_session"

# Brand Identity
APP_NAME = "FundedDesk"
APP_SUB_NAME = "INDIA'S PREMIER PROP FIRM"
APP_TAGLINE = "Empowering Indian Traders with Institutional Capital"

# Razorpay Credentials
RAZORPAY_KEY_ID = "rzp_test_TSjqPvwaeUHguA"
RAZORPAY_KEY_SECRET = "DxYT3GsAqCAN4JIzpcvjU7fN"
