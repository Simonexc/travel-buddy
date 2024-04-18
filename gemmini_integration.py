# TODO(developer): Vertex AI SDK - uncomment below & run as you're in Cloud Shell
# gcloud auth application-default login

#For local https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
#The authentication

import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('REGION')


def parse_entries(data):
    result = {}
    for entry_type, entries in data.items():
        # Initialize the type of object with an empty list
        result[entry_type] = []
        for entry in entries:
            # Extract the required fields
            parsed_entry = {
                'name': entry.get('name', 'N/A'),
                'description': entry.get('description', 'No description available'),
                'rating': entry.get('rating', 'No rating')
            }
            # Append the parsed entry to the type list
            result[entry_type].append(parsed_entry)
    print(f"{result}")
    return result

def generate_text(city:str, list_of_locations:dict) -> str:
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro")
    parsed_locations = parse_entries(list_of_locations)
    response = multimodal_model.generate_content(f"Pretend you're travel agent that needs to create 3-day in {city} plan for user. You need use locations and their descriptions from the following Python dictionary {parsed_locations}. During 3-day you need propose for the user restaurant for attractions each day and hotel. Must be 1800 or fewer in number of characters.")
    print(response)
    return response.text

