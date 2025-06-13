import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_outreach(data: dict, recommendations: list) -> str:
    profile = f"""
Full Name: {data['full_name']}
Headline: {data['headline']}
Summary: {data['summary']}
Experience: {"; ".join(data['experiences'])}
"""

    recs_formatted = ""
    for rec in recommendations:
        recs_formatted += f"- Name: {rec.get('full_name', 'N/A')}, Role: {rec.get('occupation', 'N/A')}, Profile URL: {rec.get('profile_url', 'N/A')}\n"

    prompt = f"""
You are a senior LinkedIn strategist. Based on the following user profile and their professional background, create a strategic 2-week content campaign for them AND generate 5 high-quality, personalized outreach messages.

Profile:
{profile}

Recommended Professionals:
{recs_formatted}

Instructions:
For each connection:
- Include a personalized message referencing shared interests.
- Suggest a visual concept with a clear image generation prompt.
- Provide text overlay instructions.
- Output in Markdown format.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
