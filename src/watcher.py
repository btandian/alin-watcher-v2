from src.alin_api import get_eligible_offers
from src.database import init_database, offer_exists, save_offer
from src.telegram import send_message


def is_t2(offer: dict) -> bool:
    attributes = offer.get("attributes", {})

    typology = str(
        attributes.get("typology", "")
    ).upper().strip()

    return typology == "T2"


def format_offer(offer: dict) -> str:
    attributes = offer.get("attributes", {})

    city = attributes.get("district", "?")
    postal_code = attributes.get("postal_code", "?")
    surface = attributes.get("surface", "?")
    rent = attributes.get("rent_with_charges", "?")
    candidates = attributes.get("applicated_nb", "?")
    availability = attributes.get("availability_date", "?")
    publication_end = attributes.get("publication_end_date", "?")
    offer_id = offer.get("id", "?")

    return (
        "🚨 NOUVEAU T2 AL'in\n\n"
        f"📍 Ville : {city} ({postal_code})\n"
        f"🏠 Surface : {surface} m²\n"
        f"💶 Loyer CC : {rent} €\n"
        f"👥 Candidatures : {candidates}\n"
        f"📅 Disponible : {availability}\n"
        f"⏳ Fin offre : {publication_end}\n"
        f"🆔 ID : {offer_id}"
    )


def run_watcher():
    init_database()

    print("Connexion à AL'in...")

    offers = get_eligible_offers()

    print(
        f"Offres éligibles trouvées : {len(offers)}"
    )

    t2_offers = [
        offer
        for offer in offers
        if is_t2(offer)
    ]

    print(
        f"T2 éligibles trouvés : {len(t2_offers)}"
    )

    new_offers = []

    for offer in t2_offers:
        offer_id = offer.get("id")

        if not offer_id:
            continue

        if not offer_exists(offer_id):
            new_offers.append(offer)

        save_offer(offer)

    if not new_offers:
        print("Aucun nouveau T2.")
        return

    print(
        f"{len(new_offers)} nouveau(x) T2 détecté(s)."
    )

    for offer in new_offers:
        message = format_offer(offer)

        print(message)

        send_message(message)