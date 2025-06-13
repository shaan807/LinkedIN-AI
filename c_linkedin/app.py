import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

def analyze_post(post_text):
    """Analyze a LinkedIn post using Gemini"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Analyze this LinkedIn post and provide insights:
    
    {post_text}
    
    Provide analysis in the following format:
    1. Engagement Score (0-100)
    2. Key Strengths
    3. Areas for Improvement
    4. Suggested Improvements
    5. Best Posting Time
    6. Recommended Hashtags
    
    Format as JSON with these exact keys:
    {{
        "engagement_score": number,
        "key_strengths": [string],
        "improvements": [string],
        "suggestions": [string],
        "best_time": string,
        "hashtags": [string]
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {
            "engagement_score": 0,
            "key_strengths": ["Unable to analyze post"],
            "improvements": ["Please try again"],
            "suggestions": ["Please try again"],
            "best_time": "Unknown",
            "hashtags": []
        }

def generate_post_improvement(post_text, analysis):
    """Generate an improved version of the post"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Original post:
    {post_text}
    
    Analysis:
    {json.dumps(analysis, indent=2)}
    
    Generate an improved version of this post that:
    1. Addresses the improvement areas
    2. Incorporates the suggestions
    3. Uses the recommended hashtags
    4. Maintains the original message
    5. Is more engaging
    
    Format as JSON with these keys:
    {{
        "improved_post": string,
        "explanation": string
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {
            "improved_post": post_text,
            "explanation": "Unable to generate improvement"
        }

def main():
    st.title("✍️ LinkedIn Content Creator")
    
    # Post Input
    st.header("Analyze Your Post")
    post_text = st.text_area(
        "Enter your LinkedIn post:",
        height=150,
        help="Paste your post text here for analysis"
    )
    
    if st.button("Analyze Post"):
        if not post_text.strip():
            st.warning("Please enter a post to analyze.")
            return
            
        with st.spinner("Analyzing your post..."):
            analysis = analyze_post(post_text)
            
        # Display Analysis
        st.success("✅ Analysis complete!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Engagement Score", f"{analysis['engagement_score']}/100")
            
            st.subheader("Key Strengths")
            for strength in analysis['key_strengths']:
                st.write(f"✅ {strength}")
                
            st.subheader("Areas for Improvement")
            for improvement in analysis['improvements']:
                st.write(f"📝 {improvement}")
        
        with col2:
            st.subheader("Suggested Improvements")
            for suggestion in analysis['suggestions']:
                st.write(f"💡 {suggestion}")
                
            st.subheader("Best Posting Time")
            st.write(f"⏰ {analysis['best_time']}")
            
            st.subheader("Recommended Hashtags")
            hashtags = " ".join([f"#{tag}" for tag in analysis['hashtags']])
            st.write(hashtags)
        
        # Generate Improvement
        if st.button("Generate Improved Version"):
            with st.spinner("Generating improved version..."):
                improvement = generate_post_improvement(post_text, analysis)
                
            st.subheader("Improved Post")
            st.write(improvement['improved_post'])
            
            st.subheader("Explanation")
            st.write(improvement['explanation'])
            
            if st.button("Copy Improved Post"):
                st.experimental_set_clipboard(improvement['improved_post'])
                st.success("Copied to clipboard!")

if __name__ == "__main__":
    main()
