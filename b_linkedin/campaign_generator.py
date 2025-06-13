
import os
import replicate
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Load API keys
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

# Gemini text model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_campaign_plan(user_posts: str) -> str:
    """
    Generates a 2-week content campaign using Gemini based on user's recent posts.
    """
    prompt = f"""
You are a professional LinkedIn strategist.

The user has recently posted the following:
{user_posts}

Based on their tone, topics, and style, generate a 2-week (10-post) LinkedIn content campaign.
Each post should include:

### Post #
- **Post Text**: A complete, engaging LinkedIn post (with emojis and hashtags).
- **Visual Concept**: Description of an AI-generated visual idea.
- **Image Generation Prompt**: The detailed, ready-to-use prompt that could be fed into a text-to-image model.
- **Text Overlay Instructions**: What text (from the post) should be overlayed on the image.

Use Markdown format.
"""
import os
import streamlit as st
import requests
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini text model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_campaign_plan(user_posts: str):
    prompt = f"""
You are a professional LinkedIn strategist.

The user has recently posted the following posts on LinkedIn:
{user_posts}

Analyze their content style, tone, and themes.

Based on this, generate a detailed 2-week (10 posts) LinkedIn content campaign plan.

For each post, generate a complete "post package" containing these four elements:

a. Post Text: The full, ready-to-publish LinkedIn post text including hashtags and emojis.
b. Visual Concept: A clear, concise description of the accompanying visual.
c. Image Generation Prompt: A detailed, ready-to-use prompt suitable for text-to-image models (e.g., Stable Diffusion or DALL-E).
d. Text Overlay Instructions: Simple instructions on what text from the post should be programmatically overlaid onto the image.

Format your response as Markdown with headings for each post, e.g., "### Post 1", followed by labeled sections for the four elements.

Keep each post unique, strategic, and engaging.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

    response = model.generate_content(prompt)
    return response.text.strip()



# def generate_image(prompt: str) -> str:
#     try:
#         output = replicate.run(
#             "stability-ai/sdxl:5c68dbb7e05b08f376a8b1c85a1cc3f3f5a7f147ddfe304ea181eb43c42304e4",
#             input={"prompt": prompt}
#         )
#         # `output` is a list with image URL(s)
#         return output[0] if output else None
#     except Exception as e:
#         print(f"[Image Generation Error]: {e}")
#         return None


def generate_image(prompt: str) -> str:
    """
    Generates image using Replicate (SDXL model) and returns the image URL.
    """
    output = replicate.run(
        "stability-ai/sdxl:1f7cf94f504b02d5750487b1e9ed75bfa37e8eaa0482e6b5e0f6ee3d28eb6ef1",
        input={"prompt": prompt}
    )
    return output[0]  # returns URL string
