import os
import requests
from dotenv import load_dotenv

load_dotenv()
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
PROXYCURL_PROFILE_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"
PROXYCURL_RECOMMENDATION_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin/recommendations"

HEADERS = {
    "Authorization": f"Bearer {PROXYCURL_API_KEY}"
}

def fetch_profile_data(linkedin_url: str) -> dict:
    params = {"url": linkedin_url, "use_cache": "if-present"}

    response = requests.get(PROXYCURL_PROFILE_ENDPOINT, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    experiences = []
    for exp in data.get("experiences", []):
        title = exp.get("title", "")
        company = exp.get("company_name") or exp.get("company") or ""
        if title or company:
            experiences.append(f"{title} at {company}")

    return {
        "full_name": data.get("full_name", ""),
        "headline": data.get("headline", ""),
        "summary": data.get("summary", ""),
        "experiences": experiences,
        "profile_picture_url": data.get("profile_pic_url", "")
    }


def fetch_recommendations(linkedin_url: str, limit: int = 5) -> list:
    params = {
        "profile_url": linkedin_url,
        "limit": limit
    }

    response = requests.get(PROXYCURL_RECOMMENDATION_ENDPOINT, headers=HEADERS, params=params)
    if response.status_code == 404:
        # Proxycurl may return 404 if recommendations are not available
        return []

    response.raise_for_status()
    return response.json().get("recommended_profiles", [])
