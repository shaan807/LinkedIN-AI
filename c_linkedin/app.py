import streamlit as st
from c_linkedin.competitor import analyze_competitor_strategy, analyze_competitor_images

def main():
    st.title("🔍 Competitor Strategy Analyzer")

    st.markdown("Enter 1–5 LinkedIn profile URLs of your competitors or aspirational figures.")

    num_competitors = st.slider("Select number of competitors to analyze:", min_value=1, max_value=5, value=3)

    competitors = []
    posts_data = {}
    images_data = {}

    for i in range(num_competitors):
        url = st.text_input(f"Enter LinkedIn Profile URL #{i+1}", key=f"url_{i}")
        if url:
            competitors.append(url)
            posts = st.text_area(f"Paste recent posts for {url}:", height=150, key=f"posts_{i}")
            posts_data[url] = posts

            uploaded_imgs = st.file_uploader(
                f"Upload images of recent posts for {url} (optional):",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True,
                key=f"images_{i}"
            )
            images_data[url] = uploaded_imgs

    if st.button("🔎 Analyze Competitors"):
        if not competitors:
            st.warning("Please enter at least one competitor LinkedIn URL.")
        else:
            st.info("Analyzing competitor strategies...")

            for url in competitors:
                posts = posts_data.get(url, "")
                uploaded_imgs = images_data.get(url, [])

                if not posts.strip() and not uploaded_imgs:
                    st.warning(f"No posts or images provided for {url}. Skipping.")
                    continue

                # Analyze text
                if posts.strip():
                    text_analysis = analyze_competitor_strategy(url, posts)
                    st.markdown(f"### 📝 Text Posts Analysis for {url}")
                    st.markdown(text_analysis)

                # Analyze images
                if uploaded_imgs:
                    image_analysis = analyze_competitor_images(uploaded_imgs)
                    st.markdown(f"### 🖼️ Image Content Analysis for {url}")
                    st.markdown(image_analysis)
