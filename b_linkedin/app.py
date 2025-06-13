import streamlit as st
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

load_dotenv()

def generate_campaign_plan(posts):
    """Generate a strategic campaign plan using Gemini"""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        As a LinkedIn marketing expert, analyze these posts and create a strategic campaign plan.
        Format your response EXACTLY as shown below, with clear section headers and content:

        ### Post 1
        **Post Text:** [Write engaging post text here]
        **Visual Concept:** [Describe the visual concept]
        **Image Generation Prompt:** [Write a detailed prompt for image generation]
        **Text Overlay Instructions:** [Specify text overlay details]

        ### Post 2
        **Post Text:** [Write engaging post text here]
        **Visual Concept:** [Describe the visual concept]
        **Image Generation Prompt:** [Write a detailed prompt for image generation]
        **Text Overlay Instructions:** [Specify text overlay details]

        [Continue for 3-5 posts]

        Analyze these posts:
        {posts}
        
        Important:
        1. Use EXACTLY the format shown above
        2. Include 3-5 posts in your campaign
        3. Each post must have all four sections
        4. Keep the section headers exactly as shown
        5. Make the content engaging and professional
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating campaign: {str(e)}")
        return None

def parse_campaign_markdown(markdown_text):
    """Parse the campaign markdown into structured data"""
    if not markdown_text:
        return []
        
    posts = []
    current_post = {}
    
    # Split the text into lines and process
    lines = markdown_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for new post
        if line.startswith('### Post'):
            if current_post:
                posts.append(current_post)
            current_post = {}
            i += 1
            continue
            
        # Check for post text
        if line.startswith('**Post Text:**'):
            current_post['post_text'] = line.replace('**Post Text:**', '').strip()
            i += 1
            continue
            
        # Check for visual concept
        if line.startswith('**Visual Concept:**'):
            current_post['visual_concept'] = line.replace('**Visual Concept:**', '').strip()
            i += 1
            continue
            
        # Check for image prompt
        if line.startswith('**Image Generation Prompt:**'):
            current_post['image_prompt'] = line.replace('**Image Generation Prompt:**', '').strip()
            i += 1
            continue
            
        # Check for text overlay
        if line.startswith('**Text Overlay Instructions:**'):
            current_post['text_overlay'] = line.replace('**Text Overlay Instructions:**', '').strip()
            i += 1
            continue
            
        i += 1
    
    # Add the last post if exists
    if current_post:
        posts.append(current_post)
    
    # Validate posts
    valid_posts = []
    for post in posts:
        if all(key in post for key in ['post_text', 'visual_concept', 'image_prompt', 'text_overlay']):
            valid_posts.append(post)
    
    return valid_posts

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
            
            if not campaign_markdown:
                st.error("Failed to generate campaign plan. Please try again.")
                return
                
            st.success("✅ Campaign plan generated!")
            
            # Display the raw markdown first
            st.markdown("### Raw Campaign Plan")
            st.markdown(campaign_markdown)
            
            # Parse and display structured campaign
            st.markdown("### Structured Campaign")
            posts = parse_campaign_markdown(campaign_markdown)
            
            if not posts:
                st.warning("No valid posts were found in the generated campaign. Please try again.")
                return
                
            st.session_state["campaign_posts"] = posts

            for i, post in enumerate(posts):
                with st.expander(f"Post {i+1}", expanded=True):
                    st.markdown("**Post Text:**")
                    st.write(post.get("post_text", "No post text generated"))
                    
                    st.markdown("**Visual Concept:**")
                    st.write(post.get("visual_concept", "No visual concept generated"))
                    
                    st.markdown("**Image Generation Prompt:**")
                    st.code(post.get("image_prompt", "No image prompt generated"))
                    
                    st.markdown("**Text Overlay Instructions:**")
                    st.write(post.get("text_overlay", "No text overlay instructions generated"))
                    
                    if st.button(f"Copy Image Prompt for Post {i+1}", key=f"copy_prompt_{i}"):
                        st.experimental_set_clipboard(post.get("image_prompt", ""))
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
                    try:
                        encoded_prompt = img_prompt.replace(" ", "_")
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}"
                        st.image(image_url, caption="Generated Image Preview", use_column_width=True)

                        # Download button
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
                        st.error(f"Error generating image: {str(e)}")

            if st.button("Close Dialog"):
                st.session_state["show_dialog"] = False

if __name__ == "__main__":
    main()
