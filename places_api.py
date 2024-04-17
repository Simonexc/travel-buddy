import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
PLACES_API_KEY = os.getenv('GCP_PLACES_API_KEY')

SEARCH_TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
NEARBY_PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"


async def fetch(url, session, data, headers):
    async with session.post(url, json=data, headers=headers) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()


async def get_places(search_text: str) -> list:
    data = {
        "textQuery": search_text,
        "languageCode": "en",
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': PLACES_API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.location'
    }

    async with aiohttp.ClientSession() as session:
        response = await fetch(SEARCH_TEXT_URL, session, data, headers)
        places = response.get("places", [])
        return [
            {
                "name": place.get('displayName', {}).get('text'),
                "latitude": place.get('location', {}).get('latitude'),
                "longitude": place.get('location', {}).get('longitude'),
            } for place in places
        ]


async def get_nearby_places(search_type: str, latitude: float, longitude: float, radius: float = 10000, max_results: int = 5) -> list:
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

    async with aiohttp.ClientSession() as session:
        response = await fetch(NEARBY_PLACES_URL, session, data, headers)
        places = response.get("places", [])
        return [
            {
                "name": place.get('displayName', {}).get('text'),
                "latitude": place.get('location', {}).get('latitude'),
                "longitude": place.get('location', {}).get('longitude'),
                "description": place.get('editorialSummary', {}).get('text'),
                "rating": place.get('rating'),
                "website": place.get('websiteUri'),
            } for place in places
        ]
