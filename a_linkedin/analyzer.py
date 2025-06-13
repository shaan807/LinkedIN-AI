# analyzer.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# List of available models in order of preference
GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def get_working_model():
    """Try to initialize each model in order of preference"""
    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple prompt
            response = model.generate_content("Test connection")
            if response:
                return model
        except Exception as e:
            print(f"Failed to initialize {model_name}: {str(e)}")
            continue
    raise Exception("No working Gemini model found")

def analyze_profile(profile_data):
    """Analyze LinkedIn profile data using Gemini"""
    try:
        model = get_working_model()
        
        prompt = f"""Analyze this LinkedIn profile data and provide a detailed analysis in JSON format with the following structure:
        {{
            "strengths": "List of key strengths",
            "weaknesses": "List of areas for improvement",
            "suggestions": ["List of specific suggestions"]
        }}

        Profile Data:
        Headline: {profile_data.get('headline', '')}
        About: {profile_data.get('about', '')}
        Experience: {json.dumps(profile_data.get('experience', []), indent=2)}
        """
        
        response = model.generate_content(prompt)
        if response and response.text:
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the response
                text = response.text
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(text[start:end])
                raise
        return None
    except Exception as e:
        print(f"Error in profile analysis: {str(e)}")
        return None

def generate_resume_summary(profile_data):
    """Generate a concise professional summary using Gemini"""
    try:
        model = get_working_model()
        
        prompt = f"""Create a concise, professional summary (2-3 sentences) based on this LinkedIn profile data:

        Headline: {profile_data.get('headline', '')}
        About: {profile_data.get('about', '')}
        Experience: {json.dumps(profile_data.get('experience', []), indent=2)}
        """
        
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return None
    except Exception as e:
        print(f"Error in summary generation: {str(e)}")
        return None
