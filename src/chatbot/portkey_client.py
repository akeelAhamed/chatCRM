import os
import requests
from dotenv import load_dotenv

load_dotenv()

PORTKEY_API_KEY = os.getenv('PORTKEY_API_KEY')

def get_response(user_input: str):
    # Placeholder for Portkey API call
    return {'message': 'Simulated response for: ' + user_input}
