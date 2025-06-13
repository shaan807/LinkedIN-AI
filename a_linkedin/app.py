# app.py
import streamlit as st
import json
from .utils import extract_linkedin_data
from .analyzer import analyze_profile, generate_resume_summary
import os
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO

load_dotenv()

def generate_pdf(result, summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "LinkedIn Profile Analysis Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Strengths:\n{result['strengths']}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Weaknesses:\n{result['weaknesses']}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Suggestions:\n" + "\n".join(f"- {s}" for s in result["suggestions"]))
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Resume Summary Suggestion:\n{summary_text}")

    # ✅ Fix: write PDF to memory as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer

def main():
    st.title("LinkedIn Profile Analyzer")
    st.markdown("""
    This tool helps you:
    1. Analyze your LinkedIn profile
    2. Get insights about your strengths and weaknesses
    3. Receive personalized improvement suggestions
    4. Generate a professional summary
    """)

    # Input section
    st.header("Enter Your LinkedIn Profile URL")
    profile_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/username/")

    if profile_url:
        try:
            with st.spinner("Analyzing your profile..."):
                # Get profile data
                profile_data = extract_linkedin_data(profile_url)
                
                if profile_data:
                    # Display profile info
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if profile_data.get('profile_pic_url'):
                            st.image(profile_data['profile_pic_url'], width=200)
                    with col2:
                        st.subheader(profile_data.get('full_name', ''))
                        st.write(profile_data.get('headline', ''))
                    
                    # Analyze profile
                    analysis = analyze_profile(profile_data)
                    
                    if analysis:
                        # Display analysis results
                        st.header("Profile Analysis")
                        
                        # Strengths
                        st.subheader("Strengths")
                        for strength in analysis.get('strengths', []):
                            st.write(f"✅ {strength}")
                        
                        # Weaknesses
                        st.subheader("Areas for Improvement")
                        for weakness in analysis.get('weaknesses', []):
                            st.write(f"⚠️ {weakness}")
                        
                        # Suggestions
                        st.subheader("Suggestions")
                        for suggestion in analysis.get('suggestions', []):
                            st.write(f"💡 {suggestion}")
                        
                        # Generate and display summary
                        st.header("Professional Summary")
                        summary = generate_resume_summary(profile_data)
                        if summary:
                            st.write(summary)
                            
                            # Copy button
                            if st.button("Copy Summary"):
                                st.code(summary)
                                st.success("Summary copied to clipboard!")
                    else:
                        st.error("Failed to analyze profile. Please try again.")
                else:
                    st.error("Could not fetch profile data. Please check the URL and try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please make sure you have a valid Proxycurl API key in your .env file.")

if __name__ == "__main__":
    main()
