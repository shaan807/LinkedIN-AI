import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_competitor_strategy(profile_url: str, recent_posts_text: str) -> str:
    prompt = f"""
You are a LinkedIn content strategist AI. Analyze the following competitor LinkedIn profile and their recent posts content. Provide insights on:

- Recurring themes and topics
- Posting frequency (based on the text provided)
- Content strategy and style (tone, visuals usage)
- Suggestions to improve the user's own campaign based on this competitor

Profile URL: {profile_url}

Recent Posts Content:
{recent_posts_text}

Provide a clear, actionable report in markdown format.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

from PIL import Image
import google.generativeai as genai

def analyze_competitor_images(uploaded_images) -> str:
    analyses = []

    for image_file in uploaded_images:
        # Convert uploaded image file to PIL Image
        image = Image.open(image_file)

        # Combine text + image input in a list
        input_parts = [
            "Analyze this LinkedIn post image. Describe the theme, visual style, and effectiveness for engagement.",
            image
        ]

        try:
            response = model.generate_content(input_parts)
            analyses.append(f"**Image: {image_file.name}**\n\n{response.text.strip()}")
        except Exception as e:
            analyses.append(f"**Image: {image_file.name}**\n\n❌ Error analyzing image: {e}")

    return "\n\n---\n\n".join(analyses)
