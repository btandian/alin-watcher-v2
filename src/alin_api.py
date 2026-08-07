from typing import List

import requests

from src.auth import get_alin_token
from src.config import (
    ALIN_API_BASE,
    HOUSING_REQUEST_ID,
    require,
)


def get_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://al-in.fr",
        "Referer": "https://al-in.fr/",
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        ),
    }


def get_eligible_offers() -> List[dict]:
    request_id = require(
        "ALIN_HOUSING_REQUEST_ID",
        HOUSING_REQUEST_ID
    )

    print(
        "Authentification automatique AL'in..."
    )

    token = get_alin_token()

    print(
        "Authentification réussie."
    )

    url = (
        f"{ALIN_API_BASE}/housing_requests/"
        f"{request_id}/eligible_offers"
    )

    params = {
        "per_page": 30,
        "page": 1,
        "sort[publication_end_date]": 1,
        "eligibility_type": "seeked",
        "options[]": [
            "bordering_count",
            "seeked_count",
            "other_from_department_count",
        ],
    }

    all_offers = []

    while True:
        response = requests.get(
            url,
            headers=get_headers(token),
            params=params,
            timeout=30,
        )

        if response.status_code == 401:
            raise RuntimeError(
                "Le token AL'in a été refusé."
            )

        if response.status_code == 403:
            raise RuntimeError(
                "Accès AL'in refusé."
            )

        response.raise_for_status()

        payload = response.json()

        all_offers.extend(
            payload.get(
                "data",
                []
            )
        )

        pagination = (
            payload
            .get("meta", {})
            .get("pagination", {})
        )

        current_page = params["page"]

        total_pages = pagination.get(
            "total_pages",
            1
        )

        if current_page >= total_pages:
            break

        params["page"] += 1

    return all_offers