import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


ALIN_API_BASE = "https://api.al-in.fr/api/dmo"

AUTH_URL = (
    "https://api.be-ys.com/"
    "als-back/v1/accounts/authenticate"
)

TOKEN_EXCHANGE_URL = (
    "https://api.al-in.fr/"
    "api/token_exchange/als_hermes_salarie"
)


HOUSING_REQUEST_ID = os.getenv(
    "ALIN_HOUSING_REQUEST_ID",
    ""
).strip()

ALIN_LOGIN = os.getenv(
    "ALIN_LOGIN",
    ""
).strip()

ALIN_PASSWORD = os.getenv(
    "ALIN_PASSWORD",
    ""
).strip()

GEXRT_API_KEY = os.getenv(
    "ALIN_GEXRT_API_KEY",
    ""
).strip()

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    ""
).strip()

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
).strip()


DATABASE_PATH = (
    BASE_DIR
    / "data"
    / "offers.db"
)


def require(name: str, value: str) -> str:
    if not value:
        raise RuntimeError(
            f"Variable manquante : {name}"
        )

    return value