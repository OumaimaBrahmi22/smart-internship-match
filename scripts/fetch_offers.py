
import os
import json
import requests

from pathlib import Path
from datetime import datetime, timezone


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_KEY = os.getenv("JOOBLE_API_KEY")

API_URL = f"https://fr.jooble.org/api/{API_KEY}" if API_KEY else None

OUTPUT_FILE = Path("data/offers/raw_offers.json")

LOCATION = "France"
RESULTS_PER_PAGE = 20

# Four targeted searches to cover the main areas
SEARCH_KEYWORDS = [
    "stage data engineer",
    "stage intelligence artificielle",
    "stage machine learning",
    "stage data science NLP LLM"
]


# --------------------------------------------------
# FETCH OFFERS FROM JOOBLE
# --------------------------------------------------

def fetch_offers(keywords, page=1):
    """Retrieve internship offers from Jooble."""

    if not API_KEY:
        raise ValueError("Missing JOOBLE_API_KEY environment variable.")

    payload = {
        "keywords": keywords,
        "location": LOCATION,
        "page": str(page),
        "ResultOnPage": RESULTS_PER_PAGE,
        "companysearch": False
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )

    if response.status_code == 403:
        raise RuntimeError("Jooble API key is invalid or access is denied.")

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

def remove_duplicates(offers):
    """Remove duplicate offers using their IDs or links."""

    unique_offers = {}
    
    for offer in offers:
        identifier = offer.get("id") or offer.get("link")

        if identifier and identifier not in unique_offers:
            unique_offers[identifier] = offer

    return list(unique_offers.values())


# --------------------------------------------------
# COLLECT ALL SEARCH RESULTS
# --------------------------------------------------

def collect_offers():
    """Collect offers from all predefined keyword searches."""

    all_offers = []

    for keywords in SEARCH_KEYWORDS:
        print(f"Searching: {keywords}")

        try:
            result = fetch_offers(keywords)

            jobs = result.get("jobs", [])
            all_offers.extend(jobs)

            print(f"Found {len(jobs)} offers.")

        except requests.RequestException as error:
            print(f"Request failed for '{keywords}': {error}")
        except RuntimeError as error:
            raise error

    return remove_duplicates(all_offers)



def save_offers(offers):
    """Save collected offers as a JSON file."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "source": "Jooble",
        "location": LOCATION,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_offers": len(offers),
        "offers": offers
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"\nCollection completed.")
    print(f"Total unique offers: {len(offers)}")
    print(f"Saved to: {OUTPUT_FILE}")



def main():
    offers = collect_offers()
    save_offers(offers)


if __name__ == "__main__":
    main()

