import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_competitor_strategies(competitor_data: list[dict]) -> str:
    prompt = """
You are a LinkedIn content strategist.

Analyze the following competitor profiles and extract:
1. Recurring content themes
2. Posting frequency
3. Style and tone
4. Use of visuals or media
5. What strategy seems to be working best
6. Recommendations for the user to improve their content campaign based on this

Format your answer in Markdown with bold headings and bullet points.

"""

    for person in competitor_data:
        prompt += f"\n\n---\n**{person['full_name']}** - {person['headline']}\nProfile: {person['profile_url']}\nRecent Posts:\n"
        for post in person["posts"][:5]:  # limit to recent 5
            prompt += f"- {post}\n"
    
    response = model.generate_content(prompt)
    return response.text.strip()
