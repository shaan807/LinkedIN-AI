import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_outreach(data: dict) -> str:
    profile = f"""
Full Name: {data['full_name']}
Headline: {data['headline']}
Summary: {data['summary']}
Experience: {"; ".join(data['experiences'])}
"""
    prompt = f"""
You are an AI assistant integrated into a LinkedIn outreach system. Your role is to analyze a user's profile, stated career goals, and network data to recommend relevant professionals to connect with, and to generate high-quality, personalized connection request messages

Profile:
{profile}

Instructions:
For each recommended person:
- Name, Role, Company, Shared Interest.
- A high-quality, personalized connection message.
- Visual Concept: clear visual idea
- Image Generation Prompt: for Stable Diffusion
- Text Overlay Instructions

Respond in Markdown. Separate each connection with a horizontal rule (---).
"""
    return model.generate_content(prompt).text.strip()
