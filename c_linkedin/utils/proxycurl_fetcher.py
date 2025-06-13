import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PROXYCURL_API_KEY")
ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

def fetch_competitor_posts(profile_url: str) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"url": profile_url, "include": "posts"}

    response = requests.get(ENDPOINT, headers=headers, params=params)
    if response.status_code != 200:
        return None
    
    data = response.json()
    return {
        "full_name": data.get("full_name", "Unknown"),
        "headline": data.get("headline", ""),
        "profile_url": profile_url,
        "posts": [post.get("text", "") for post in data.get("posts", []) if post.get("text")]
    }
