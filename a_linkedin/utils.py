# utils.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")

def extract_linkedin_data(url):
    api_url = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {
        'Authorization': f'Bearer {PROXYCURL_API_KEY}'
    }
    params = {
        'url': url,
        'use_cache': 'if-present'
    }

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "headline": data.get("headline", ""),
            "about": data.get("summary", ""),
            "experience": data.get("experiences", [])
        }
    else:
        return None
