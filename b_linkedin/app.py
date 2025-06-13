import streamlit as st
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()

def generate_campaign_plan(posts):
    """Generate a strategic campaign plan using Gemini"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    As a LinkedIn marketing expert, analyze these posts and create a strategic campaign plan:
    
    {posts}
    
    For each post in the campaign:
    1. Post Text: Engaging, professional content
    2. Visual Concept: Clear visual idea
    3. Image Generation Prompt: For Stable Diffusion
    4. Text Overlay Instructions
    
    Format in Markdown with clear sections.
    """
    
    response = model.generate_content(prompt)
    return response.text

def parse_campaign_markdown(markdown_text):
    """Parse the campaign markdown into structured data"""
    posts = []
    current_post = {}
    
    for line in markdown_text.split('\n'):
        if line.startswith('### Post'):
            if current_post:
                posts.append(current_post)
            current_post = {}
        elif line.startswith('**Post Text:**'):
            current_post['post_text'] = line.replace('**Post Text:**', '').strip()
        elif line.startswith('**Visual Concept:**'):
            current_post['visual_concept'] = line.replace('**Visual Concept:**', '').strip()
        elif line.startswith('**Image Generation Prompt:**'):
            current_post['image_prompt'] = line.replace('**Image Generation Prompt:**', '').strip()
        elif line.startswith('**Text Overlay Instructions:**'):
            current_post['text_overlay'] = line.replace('**Text Overlay Instructions:**', '').strip()
    
    if current_post:
        posts.append(current_post)
    
    return posts

def main():
    st.title("📈 LinkedIn Campaign Designer")

    user_input = st.text_area(
        "Paste your recent 5-10 LinkedIn posts here to generate a strategic campaign:",
        height=150,
    )

    if st.button("Generate Campaign Plan"):
        if not user_input.strip():
            st.warning("Please enter some recent LinkedIn posts.")
            return

        with st.spinner("Generating campaign plan..."):
            campaign_markdown = generate_campaign_plan(user_input)
        
        st.success("✅ Campaign plan generated!")

        posts = parse_campaign_markdown(campaign_markdown)
        st.session_state["campaign_posts"] = posts

        for i, post in enumerate(posts):
            st.markdown(f"### Post {i+1}")

            st.markdown("**Post Text:**")
            st.write(post["post_text"])

            st.markdown("**Visual Concept:**")
            st.write(post["visual_concept"])

            st.markdown("**Image Generation Prompt:**")
            st.code(post["image_prompt"])

            st.markdown("**Text Overlay Instructions:**")
            st.write(post["text_overlay"])

            if st.button(f"Copy Image Prompt for Post {i+1}", key=f"copy_prompt_{i}"):
                st.experimental_set_clipboard(post["image_prompt"])
                st.success("Copied image prompt to clipboard!")

    st.markdown("---")

    st.header("Generate Image from Prompt")

    if "show_dialog" not in st.session_state:
        st.session_state["show_dialog"] = False

    if st.button("Open Image Generation Dialog"):
        st.session_state["show_dialog"] = True

    if st.session_state["show_dialog"]:
        with st.expander("Image Generation Dialog", expanded=True):
            img_prompt = st.text_area(
                "Enter Image Prompt",
                value="",
                height=100,
                help="Enter or paste the prompt you want to generate the image for.",
            )
            if st.button("Generate Image"):
                if not img_prompt.strip():
                    st.warning("Please enter an image generation prompt.")
                else:
                    encoded_prompt = img_prompt.replace(" ", "_")
                    image_url = f"https://pollinations.ai/p/{encoded_prompt}"
                    st.image(image_url, caption="Generated Image Preview", use_column_width=True)

                    # Download button
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            st.download_button(
                                label="Download Image",
                                data=response.content,
                                file_name="generated_image.jpg",
                                mime="image/jpeg",
                            )
                        else:
                            st.error("Failed to download image.")
                    except Exception as e:
                        st.error(f"Error downloading image: {e}")

            if st.button("Close Dialog"):
                st.session_state["show_dialog"] = False

if __name__ == "__main__":
    main()
