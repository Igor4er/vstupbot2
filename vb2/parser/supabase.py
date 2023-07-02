from vb2.settings import settings
import requests


def insert_category_into_base(category: str):
    r = requests.post(
        f"{settings.DB_URL}/categories",
        json={
            "name": category
        },
        headers={
            "apikey": settings.DB_KEY,
            "Authorization": f"Bearer {settings.DB_KEY}",
            "Content-Type": "application/json",
            #"Prefer": "return=minimal",
        }
    )
    if not r.ok:
        print(r.status_code)
        print(r.content)
