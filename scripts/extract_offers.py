
import json
import requests

from pathlib import Path
from datetime import datetime, timezone


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"

INPUT_FILE = Path("data/offers/raw_offers.json")
OUTPUT_FILE = Path("data/offers/extracted_offers.json")


# --------------------------------------------------
# OLLAMA EXTRACTION
# --------------------------------------------------

def extract_skills(offer):
    """Extract structured information from one job offer."""

    title = offer.get("title", "")
    description = offer.get("snippet", "")
    company = offer.get("company", "")

    prompt = f"""
You are an expert in recruitment and technical skill extraction.

Analyze the following internship offer.

Title: {title}
Company: {company}
Description: {description}

Extract the information and return ONLY valid JSON with this structure:

{{
    "technical_skills": [],
    "soft_skills": [],
    "tools": [],
    "missions": [],
    "experience_level": "",
    "education": ""
}}

Rules:
- Extract only information explicitly mentioned or clearly required.
- Do not invent skills or requirements.
- Use English for the extracted labels.
- Use empty lists or empty strings when information is unavailable.
- Return valid JSON only.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    result = response.json()
    extracted_text = result.get("response", "{}")

    return json.loads(extracted_text)


# --------------------------------------------------
# PROCESS ALL OFFERS
# --------------------------------------------------

def process_offers(offers):
    """Process all offers using the local LLM."""

    extracted_offers = []

    total = len(offers)

    for index, offer in enumerate(offers, start=1):

        print(f"Processing offer {index}/{total}: {offer.get('title', 'Unknown')}")

        try:
            extracted_data = extract_skills(offer)

            enriched_offer = {
                **offer,
                "extracted_skills": extracted_data
            }

            extracted_offers.append(enriched_offer)

        except requests.RequestException as error:
            print(f"API error: {error}")

        except (json.JSONDecodeError, ValueError) as error:
            print(f"Invalid JSON response: {error}")

    return extracted_offers


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(offers):
    """Save extracted offers into a JSON file."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "source": "Jooble + Ollama",
        "model": MODEL,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "total_processed": len(offers),
        "offers": offers
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"\nExtraction completed.")
    print(f"Offers processed: {len(offers)}")
    print(f"Output: {OUTPUT_FILE}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    offers = data.get("offers", [])

    print(f"Loaded {len(offers)} offers.")

    extracted_offers = process_offers(offers)

    save_results(extracted_offers)


if __name__ == "__main__":
    main()
