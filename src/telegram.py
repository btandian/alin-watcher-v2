import requests

from src.config import (
    TELEGRAM_CHAT_ID,
    TELEGRAM_TOKEN,
    require,
)


def send_message(message: str):
    token = require(
        "TELEGRAM_TOKEN",
        TELEGRAM_TOKEN
    )

    chat_id = require(
        "TELEGRAM_CHAT_ID",
        TELEGRAM_CHAT_ID
    )

    url = (
        f"https://api.telegram.org/"
        f"bot{token}/sendMessage"
    )

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message,
        },
        timeout=20,
    )

    response.raise_for_status()