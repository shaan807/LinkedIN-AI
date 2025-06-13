# LinkedIn Booster Suite

A comprehensive suite of tools for LinkedIn profile optimization, content creation, and outreach.

## Features

- 📊 Profile Analyzer: Analyze and optimize your LinkedIn profile
- 🔍 Competitor Analyzer: Analyze competitor profiles and strategies
- 📝 Post Analyzer: Analyze and improve your LinkedIn posts
- 🤝 Outreach Generator: Generate personalized outreach messages

## Deployment Instructions

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   PROXYCURL_API_KEY=your_proxycurl_api_key
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (app.py)
6. Add your secrets in the "Secrets" section:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key"
   PROXYCURL_API_KEY = "your_proxycurl_api_key"
   ```
7. Click "Deploy"

## Required API Keys

- Google API Key: For Gemini AI integration
  - Get it from: https://makersuite.google.com/app/apikey
- Proxycurl API Key: For LinkedIn data
  - Get it from: https://nubela.co/proxycurl

## Project Structure

```
linkedin-booster/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API keys (for deployment)
├── a_linkedin/           # Profile Analyzer
├── b_linkedin/           # Competitor Analyzer
├── c_linkedin/           # Post Analyzer
└── d_linkedin/           # Outreach Generator
```

## License

MIT License 