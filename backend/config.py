import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

_raw_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
# Accept either the base URL or a full ".../openai/deployments/..." URL pasted from the portal.
_u = urlparse(_raw_endpoint)
AZURE_OPENAI_ENDPOINT = f"{_u.scheme}://{_u.netloc}/" if _u.netloc else ""
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
API_VERSION = "2025-01-01-preview"

POLICY_PDF = ROOT / "backend" / "data" / "hr_policy.pdf"
FRONTEND_DIR = ROOT / "frontend"
MAX_MESSAGE_CHARS = 500
MAX_HISTORY_MESSAGES = 10
