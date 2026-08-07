import requests

from src.config import (
    ALIN_LOGIN,
    ALIN_PASSWORD,
    AUTH_URL,
    GEXRT_API_KEY,
    TOKEN_EXCHANGE_URL,
    require,
)


def authenticate_be_ys() -> str:
    """
    Connexion à BE-YS avec le compte AL'in.

    Retourne le access_token BE-YS.
    """

    login = require(
        "ALIN_LOGIN",
        ALIN_LOGIN
    )

    password = require(
        "ALIN_PASSWORD",
        ALIN_PASSWORD
    )

    api_key = require(
        "ALIN_GEXRT_API_KEY",
        GEXRT_API_KEY
    )

    response = requests.post(
        AUTH_URL,
        json={
            "login": login,
            "password": password,
        },
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://al-in.fr",
            "Referer": "https://al-in.fr/",
            "x-gexrt-api-key": api_key,
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"
            ),
        },
        timeout=30,
    )

    print(
        "Authentification BE-YS :",
        response.status_code
    )

    if response.status_code != 200:
        print(
            "Réponse serveur :",
            response.text[:500]
        )

        raise RuntimeError(
            "Connexion AL'in refusée."
        )

    data = response.json()

    access_token = data.get(
        "access_token"
    )

    if not access_token:
        raise RuntimeError(
            "Aucun access_token reçu."
        )

    return access_token


def exchange_token(
    access_token: str
) -> str:
    """
    Échange le access_token BE-YS
    contre le jwt_token utilisé par AL'in.
    """

    response = requests.post(
        TOKEN_EXCHANGE_URL,
        json={
            "access_token": access_token
        },
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://al-in.fr",
            "Referer": "https://al-in.fr/",
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"
            ),
        },
        timeout=30,
    )

    print(
        "Échange token AL'in :",
        response.status_code
    )

    if response.status_code != 200:
        print(
            "Réponse serveur :",
            response.text[:500]
        )

        raise RuntimeError(
            "Échange du token AL'in refusé."
        )

    data = response.json()

    if not data.get("success"):
        raise RuntimeError(
            "Échec de l'échange du token AL'in."
        )

    jwt_token = data.get(
        "jwt_token"
    )

    if not jwt_token:
        raise RuntimeError(
            "Aucun jwt_token reçu."
        )

    return jwt_token


def get_alin_token() -> str:
    """
    Authentification complète :

    login/password
        -> access_token BE-YS
        -> jwt_token AL'in
    """

    access_token = authenticate_be_ys()

    jwt_token = exchange_token(
        access_token
    )

    return jwt_token