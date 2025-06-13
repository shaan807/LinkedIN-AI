import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import requests

load_dotenv()

def analyze_profile_for_recommendations(profile_data):
    """Analyze LinkedIn profile to generate connection recommendations"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Analyze this LinkedIn profile data and generate connection recommendations:
    
    {json.dumps(profile_data, indent=2)}
    
    Provide recommendations in the following format:
    1. Career Goals (3-5 specific goals)
    2. Target Roles (3-5 specific roles)
    3. Target Industries (3-5 specific industries)
    4. Connection Criteria (specific criteria for valuable connections)
    
    Format as JSON with these exact keys:
    {{
        "career_goals": [string],
        "target_roles": [string],
        "target_industries": [string],
        "connection_criteria": [string]
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {
            "career_goals": ["Unable to analyze profile"],
            "target_roles": ["Please try again"],
            "target_industries": ["Please try again"],
            "connection_criteria": ["Please try again"]
        }

def generate_personalized_message(profile_data, target_profile):
    """Generate a personalized connection message"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Generate a personalized LinkedIn connection message based on:
    
    Your Profile:
    {json.dumps(profile_data, indent=2)}
    
    Target Profile:
    {json.dumps(target_profile, indent=2)}
    
    Requirements:
    1. Reference shared interests/background
    2. Keep it professional but friendly
    3. Focus on mutual value
    4. Stay within LinkedIn's character limit
    5. Include a clear call to action
    
    Format as JSON with these keys:
    {{
        "message": string,
        "shared_interests": [string],
        "value_proposition": string
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {
            "message": "Unable to generate message",
            "shared_interests": ["Please try again"],
            "value_proposition": "Please try again"
        }

def main():
    st.title("🤝 LinkedIn Outreach Generator")
    
    # Profile URL Input
    st.header("Enter LinkedIn Profile URL")
    profile_url = st.text_input(
        "LinkedIn Profile URL",
        help="Enter the LinkedIn profile URL to analyze"
    )
    
    if st.button("Analyze Profile"):
        if not profile_url:
            st.warning("Please enter a LinkedIn profile URL.")
            return
            
        with st.spinner("Analyzing profile..."):
            # Here you would normally fetch profile data using Proxycurl
            # For now, we'll use dummy data for demonstration
            profile_data = {
                "full_name": "John Doe",
                "headline": "Software Engineer",
                "summary": "Passionate about technology and innovation",
                "experience": ["Company A", "Company B"],
                "education": ["University X"],
                "skills": ["Python", "AI", "Machine Learning"]
            }
            
            recommendations = analyze_profile_for_recommendations(profile_data)
            
        st.success("✅ Analysis complete!")
        
        # Display Recommendations
        st.header("Connection Recommendations")
        
        st.subheader("Career Goals")
        for goal in recommendations['career_goals']:
            st.write(f"🎯 {goal}")
            
        st.subheader("Target Roles")
        for role in recommendations['target_roles']:
            st.write(f"👨‍💼 {role}")
            
        st.subheader("Target Industries")
        for industry in recommendations['target_industries']:
            st.write(f"🏢 {industry}")
            
        st.subheader("Connection Criteria")
        for criteria in recommendations['connection_criteria']:
            st.write(f"✅ {criteria}")
        
        # Generate Message
        if st.button("Generate Connection Message"):
            # Here you would normally fetch target profile data
            # For now, we'll use dummy data
            target_profile = {
                "full_name": "Jane Smith",
                "headline": "AI Researcher",
                "summary": "Working on cutting-edge AI solutions",
                "experience": ["Company C"],
                "education": ["University Y"],
                "skills": ["AI", "Machine Learning", "Python"]
            }
            
            with st.spinner("Generating personalized message..."):
                message_data = generate_personalized_message(profile_data, target_profile)
                
            st.subheader("Personalized Message")
            st.write(message_data['message'])
            
            st.subheader("Shared Interests")
            for interest in message_data['shared_interests']:
                st.write(f"🤝 {interest}")
                
            st.subheader("Value Proposition")
            st.write(message_data['value_proposition'])
            
            if st.button("Copy Message"):
                st.experimental_set_clipboard(message_data['message'])
                st.success("Copied to clipboard!")

if __name__ == "__main__":
    main()
