import sqlite3

from src.config import DATABASE_PATH


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_PATH
    )


def init_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS offers (
                id TEXT PRIMARY KEY,
                city TEXT,
                postal_code TEXT,
                typology TEXT,
                surface REAL,
                rent REAL,
                candidates INTEGER,
                availability_date TEXT,
                publication_end_date TEXT,
                first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


def offer_exists(offer_id: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT 1
            FROM offers
            WHERE id = ?
            LIMIT 1
            """,
            (offer_id,)
        )

        return cursor.fetchone() is not None


def save_offer(offer: dict):
    attributes = offer.get(
        "attributes",
        {}
    )

    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO offers (
                id,
                city,
                postal_code,
                typology,
                surface,
                rent,
                candidates,
                availability_date,
                publication_end_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                offer.get("id"),
                attributes.get("district"),
                attributes.get("postal_code"),
                attributes.get("typology"),
                attributes.get("surface"),
                attributes.get("rent_with_charges"),
                attributes.get("applicated_nb"),
                attributes.get("availability_date"),
                attributes.get("publication_end_date"),
            )
        )

        connection.commit()