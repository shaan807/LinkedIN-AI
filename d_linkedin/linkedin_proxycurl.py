import os
import requests
from dotenv import load_dotenv
from typing import Dict, List, Optional
import re

load_dotenv()
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
API_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

def clean_linkedin_url(url: str) -> str:
    """
    Clean and validate LinkedIn profile URL
    
    Args:
        url (str): Raw LinkedIn URL
        
    Returns:
        str: Cleaned URL or empty string if invalid
    """
    # Remove any trailing slashes and whitespace
    url = url.strip().rstrip('/')
    
    # Basic LinkedIn URL pattern
    pattern = r'^https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+/?$'
    
    if not re.match(pattern, url):
        print(f"Invalid LinkedIn URL format: {url}")
        return ""
        
    return url

def get_profile_data(url: str) -> dict:
    """Fetch comprehensive LinkedIn profile data using Proxycurl API"""
    headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
    
    # First, get the basic profile data
    params = {
        "url": url,
        "include": "profile_pic_url,headline,summary,experiences,education,skills,languages,accomplishments"
    }
    
    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and structure the data
        profile_data = {
            "full_name": data.get("full_name", ""),
            "headline": data.get("headline", ""),
            "summary": data.get("summary", ""),
            "profile_pic_url": data.get("profile_pic_url", ""),
            "industry": data.get("industry", ""),
            "experiences": [
                {
                    "title": exp.get("title", ""),
                    "company": exp.get("company", ""),
                    "description": exp.get("description", ""),
                    "starts_at": exp.get("starts_at", {}),
                    "ends_at": exp.get("ends_at", {})
                }
                for exp in data.get("experiences", [])
            ],
            "education": [
                {
                    "school": edu.get("school", ""),
                    "degree": edu.get("degree", ""),
                    "field_of_study": edu.get("field_of_study", ""),
                    "starts_at": edu.get("starts_at", {}),
                    "ends_at": edu.get("ends_at", {})
                }
                for edu in data.get("education", [])
            ],
            "skills": [skill.get("name", "") for skill in data.get("skills", [])],
            "languages": [lang.get("name", "") for lang in data.get("languages", [])],
            "accomplishments": [
                {
                    "title": acc.get("title", ""),
                    "description": acc.get("description", "")
                }
                for acc in data.get("accomplishments", [])
            ]
        }
        
        return profile_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile data: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {}

def search_profiles(criteria: Dict) -> List[Dict]:
    """Search for LinkedIn profiles using Proxycurl API"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin/search"
    headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
    
    try:
        response = requests.get(api_endpoint, headers=headers, params=criteria)
        response.raise_for_status()
        return response.json().get("profiles", [])
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error searching profiles: {str(e)}")

def get_profile_details(profile_url: str) -> Dict:
    """Get detailed information for a specific profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
    params = {
        "url": profile_url,
        "include": "skills,experiences,education,languages,certifications"
    }
    
    try:
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching profile details: {str(e)}")
