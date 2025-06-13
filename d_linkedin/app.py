import streamlit as st
from linkedin_proxycurl import fetch_profile_data, fetch_recommendations
from outreach_generator import generate_outreach
import requests
from io import BytesIO
from fpdf import FPDF
import os

# DO NOT call st.set_page_config() here; it's already set in the main app.py

def main():
    st.title("🚀 LinkedIn Booster - Outreach + Campaign")

    # Input
    linkedin_url = st.text_input("🔗 Enter your LinkedIn Profile URL:")

    final_text = ""  # Placeholder for PDF generation

    if linkedin_url:
        try:
            with st.spinner("🔍 Fetching profile data..."):
                profile_data = fetch_profile_data(linkedin_url)
            with st.spinner("📡 Getting recommended connections..."):
                recommended_connections = fetch_recommendations(linkedin_url)

            st.image(profile_data.get("profile_picture_url"), width=100)
            st.markdown(f"### {profile_data.get('full_name')}")
            st.markdown(f"**{profile_data.get('headline')}**")
            st.markdown(profile_data.get("summary"))
            st.markdown("**Experiences:**")
            for exp in profile_data.get("experiences", []):
                st.markdown(f"- {exp}")

            if st.button("🎯 Generate Outreach & Campaign Plan"):
                with st.spinner("🧠 Generating personalized campaign and outreach..."):
                    final_text = generate_outreach(profile_data, recommended_connections)
                    st.success("✅ Campaign & Outreach Ready!")
                    st.markdown(final_text)

                    # Extract image generation prompts
                    prompts = []
                    for line in final_text.splitlines():
                        if "Image Generation Prompt:" in line:
                            prompts.append(line.split("Image Generation Prompt:")[1].strip())

                    if prompts:
                        prompt_to_copy = st.selectbox("🎨 Select an Image Generation Prompt:", prompts)
                        if st.button("📋 Copy Prompt"):
                            st.code(prompt_to_copy)

                        if st.button("🖼️ Generate Image from Prompt"):
                            try:
                                def download_image_from_prompt(prompt: str) -> bytes:
                                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
                                    response = requests.get(url)
                                    response.raise_for_status()
                                    return response.content

                                st.info("Generating image...")
                                img_bytes = download_image_from_prompt(prompt_to_copy)
                                st.image(img_bytes)
                                st.download_button(
                                    label="⬇️ Download Generated Image",
                                    data=img_bytes,
                                    file_name="generated_image.jpg",
                                    mime="image/jpeg"
                                )
                            except Exception as e:
                                st.error(f"Image generation failed: {e}")

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a valid LinkedIn profile URL.")

    # PDF Export
    if final_text:
        if st.button("📄 Download as PDF"):
            def generate_pdf(content: str, filename="campaign.pdf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in content.split("\n"):
                    try:
                        pdf.cell(200, 10, txt=line.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
                    except:
                        pdf.cell(200, 10, txt="[Unprintable line]", ln=True)
                pdf.output(filename)

            generate_pdf(final_text)
            with open("campaign.pdf", "rb") as file:
                st.download_button(label="⬇️ Download PDF", data=file, file_name="linkedin_campaign.pdf", mime="application/pdf")

