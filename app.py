import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LinkedIn Booster Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .api-key-input {
        margin-bottom: 1rem;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def save_api_keys(google_api_key, proxycurl_api_key):
    """Save API keys to .env file"""
    env_content = f"""GOOGLE_API_KEY={google_api_key}
PROXYCURL_API_KEY={proxycurl_api_key}"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    # Update environment variables
    os.environ['GOOGLE_API_KEY'] = google_api_key
    os.environ['PROXYCURL_API_KEY'] = proxycurl_api_key

def main():
    # Sidebar
    with st.sidebar:
        st.title("🔑 API Keys")
        
        # API Key Inputs
        google_api_key = st.text_input(
            "Google API Key (for Gemini)",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Enter your Google API key for Gemini AI"
        )
        
        proxycurl_api_key = st.text_input(
            "Proxycurl API Key",
            value=os.getenv("PROXYCURL_API_KEY", ""),
            type="password",
            help="Enter your Proxycurl API key for LinkedIn data"
        )
        
        if st.button("Save API Keys"):
            if google_api_key and proxycurl_api_key:
                save_api_keys(google_api_key, proxycurl_api_key)
                st.success("API keys saved successfully!")
            else:
                st.error("Please enter both API keys")
        
        st.markdown("---")
        
        # Navigation
        st.title("Navigation")
        page = option_menu(
            menu_title=None,
            options=["Profile Analyzer", "Competitor Analyzer", "Post Analyzer", "Outreach Generator"],
            icons=["📊", "🔍", "📝", "🤝"],
            default_index=0,
        )
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div class="footer">
            <p>Get your API keys:</p>
            <a href="https://makersuite.google.com/app/apikey" target="_blank">Google API Key</a> |
            <a href="https://nubela.co/proxycurl" target="_blank">Proxycurl API Key</a>
        </div>
        """, unsafe_allow_html=True)

    # Main content
    st.title("🚀 LinkedIn Booster Suite")
    
    # Check for API keys
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("PROXYCURL_API_KEY"):
        st.warning("""
        ⚠️ Please enter your API keys in the sidebar to use all features:
        - Google API Key (for Gemini AI)
        - Proxycurl API Key (for LinkedIn data)
        """)
    
    # Display selected page
    try:
        if page == "Profile Analyzer":
            from a_linkedin.app import main as profile_analyzer
            profile_analyzer()
        elif page == "Competitor Analyzer":
            from b_linkedin.app import main as competitor_analyzer
            competitor_analyzer()
        elif page == "Post Analyzer":
            from c_linkedin.app import main as post_analyzer
            post_analyzer()
        elif page == "Outreach Generator":
            from d_linkedin.app import main as outreach_generator
            outreach_generator()
    except Exception as e:
        st.error(f"Error loading {page}: {str(e)}")
        st.info("Please ensure all required dependencies are installed and API keys are set correctly.")

if __name__ == "__main__":
    main() 