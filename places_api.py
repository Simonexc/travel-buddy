import requests
import os

from dotenv import load_dotenv

load_dotenv()
PLACES_API_KEY = os.getenv('GCP_PLACES_API_KEY')

SEARCH_TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
NEARBY_PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"


def get_places(search_text: str) -> list[dict[str, str | float | None]]:
    data = {
        "textQuery": search_text,
        "languageCode": "en",
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.location'
    }

    response = requests.post(SEARCH_TEXT_URL, headers=headers, json=data)

    if response.status_code == 200:
        return [
            {
                "name": place.get('displayName', {}).get('text'),
                "latitude": place.get('location', {}).get('latitude'),
                "longitude": place.get('location', {}).get('longitude'),
            } for place in response.json().get("places", [])
        ]
    else:
        print(response.status_code, response.content)
        print("Error getting places from Google Places API")
        return []


def get_nearby_places(search_type: str, latitude: float, longitude: float, radius: float = 10000, max_results: int = 5) -> list[dict[str, str | float | None]]:
    data = {
        "includedPrimaryTypes": [search_type],
        "maxResultCount": max_results,
        "languageCode": "en",
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius,
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.websiteUri,places.location,places.rating,places.editorialSummary'
    }

    response = requests.post(NEARBY_PLACES_URL, headers=headers, json=data)

    if response.status_code == 200:
        return [
            {
                "name": place.get('displayName', {}).get('text'),
                "latitude": place.get('location', {}).get('latitude'),
                "longitude": place.get('location', {}).get('longitude'),
                "description": place.get('editorialSummary', {}).get('text'),
                "rating": place.get('rating'),
                "website": place.get('websiteUri'),
            } for place in response.json().get("places", [])
        ]
    else:
        print(response.status_code, response.content)
        print("Error getting places from Google Places API")
        return []
