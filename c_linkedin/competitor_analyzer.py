# c_linkedin/competitor_analyzer.py
import json
import re
import requests
import plotly.graph_objs as go
from collections import Counter
import google.generativeai as genai
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import base64
from PIL import Image
import io
from post_analyzer import process_posts

# Load environment variables
load_dotenv()

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model for OCR
model = genai.GenerativeModel('gemini-pro-vision')

class LinkedInSession:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def setup_driver(self):
        """Setup and return a configured Chrome driver."""
        try:
            chrome_options = Options()
            # Basic options - removed headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")  # Disable GPU to avoid context errors
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Additional options for stability and to avoid detection
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            chrome_options.add_argument("--disable-site-isolation-trials")
            chrome_options.add_argument("--disable-webgl")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-webrtc")  # Disable WebRTC to avoid STUN errors
            
            # More realistic user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.69 Safari/537.36")
            
            # Add additional preferences to avoid detection
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Add additional preferences for better stealth
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.managed_default_content_settings.images": 1,
                "disk-cache-size": 4096,
                "webrtc.ip_handling_policy": "disable_non_proxied_udp"  # Disable non-proxied UDP
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Get the absolute path to chromedriver.exe
            current_dir = os.path.dirname(os.path.abspath(__file__))
            chromedriver_path = os.path.join(current_dir, "chromedriver.exe")
            
            if not os.path.exists(chromedriver_path):
                raise Exception(f"ChromeDriver not found at: {chromedriver_path}")
                
            print(f"Using ChromeDriver at: {chromedriver_path}")
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout and script timeout
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # Add additional JavaScript to avoid detection
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                    Object.defineProperty(navigator, 'platform', {
                        get: () => 'Win32'
                    });
                    Object.defineProperty(navigator, 'maxTouchPoints', {
                        get: () => 10
                    });
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8
                    });
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8
                    });
                    Object.defineProperty(navigator, 'userAgent', {
                        get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.69 Safari/537.36'
                    });
                """
            })
            
            return True
        except Exception as e:
            print(f"Error setting up Chrome driver: {str(e)}")
            return False

    def login(self, email, password):
        """Login to LinkedIn with provided credentials."""
        if self.is_logged_in:
            return True
            
        try:
            print("Attempting to log in to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Simulate human behavior before login
            self.simulate_human_behavior()
            
            # Enter email with human-like typing
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            for char in email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(0.5, 1.5))
            
            # Enter password with human-like typing
            password_field = self.driver.find_element(By.ID, "password")
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(0.5, 1.5))
            
            # Move mouse to login button (simulated)
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", login_button)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            login_button.click()
            
            # Wait for login to complete with natural behavior
            time.sleep(random.uniform(3, 5))
            self.simulate_human_behavior()
            
            # Check for checkpoint page
            if "checkpoint" in self.driver.current_url:
                print("LinkedIn security checkpoint detected. Please complete the verification manually.")
                print("You have 60 seconds to complete the verification...")
                time.sleep(60)  # Wait for manual verification
                
                # After verification, check if we're logged in
                if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                    print("Successfully logged in to LinkedIn after verification")
                    self.is_logged_in = True
                    return True
                else:
                    print("Login failed after verification. Current URL:", self.driver.current_url)
                    return False
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("Successfully logged in to LinkedIn")
                self.is_logged_in = True
                return True
            else:
                print("Login might have failed. Current URL:", self.driver.current_url)
                return False
                
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False

    def simulate_human_behavior(self):
        """Simulate natural human behavior to avoid detection."""
        try:
            # Random mouse movements
            for _ in range(3):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.driver.execute_script(f"window.scrollTo({x}, {y});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Natural scrolling behavior
            scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = 0
            while current_position < scroll_height:
                # Random scroll amount
                scroll_amount = random.randint(100, 300)
                current_position += scroll_amount
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.3, 1.0))
                
                # Sometimes scroll back up a bit
                if random.random() < 0.3:
                    current_position -= random.randint(50, 150)
                    self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(random.uniform(0.2, 0.8))
            
            # Random pauses
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error in human behavior simulation: {str(e)}")

    def capture_post_screenshot(self, element):
        """Capture screenshot of a post element."""
        try:
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(0.5, 1.0))
            
            # Get element location and size
            location = element.location
            size = element.size
            
            # Take full page screenshot
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            
            # Crop to element
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            
            # Add some padding
            padding = 20
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(image.width, right + padding)
            bottom = min(image.height, bottom + padding)
            
            # Crop and save
            element_screenshot = image.crop((left, top, right, bottom))
            
            # Convert to base64 for Gemini
            buffered = io.BytesIO()
            element_screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            print(f"Error capturing post screenshot: {str(e)}")
            return None

    def analyze_post_image(self, image_base64):
        """Analyze post content using Gemini Vision."""
        try:
            # Prepare the image for Gemini
            image_parts = [
                {
                    "mime_type": "image/png",
                    "data": image_base64
                }
            ]
            
            # Generate prompt for analysis
            prompt = """
            Analyze this LinkedIn post and provide:
            1. Main content/topic
            2. Type of post (article, update, announcement, etc.)
            3. Key points or highlights
            4. Any hashtags or mentions
            5. Overall tone and style
            """
            
            # Get response from Gemini
            response = model.generate_content([prompt, image_parts[0]])
            
            return response.text
            
        except Exception as e:
            print(f"Error analyzing post image: {str(e)}")
            return None

    def fetch_profile_posts(self, profile_url):
        """Fetch posts from a LinkedIn profile."""
        try:
            print(f"Fetching posts from: {profile_url}/recent-activity/shares/")
            self.driver.get(f"{profile_url}/recent-activity/shares/")
            time.sleep(random.uniform(3, 5))
            
            # Handle security checks
            if not self.handle_security_check():
                return []
            
            # Scroll to load more content
            self.simulate_human_behavior()
            
            # Find post elements
            post_elements = []
            selectors = [
                "div.feed-shared-update-v2",
                "div.feed-shared-article",
                "div.feed-shared-external-video",
                "div.feed-shared-text"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    post_elements.extend(elements)
                    break
                
            print(f"Found {len(post_elements)} post elements")
            
            # Process posts
            posts_data = []
            for element in post_elements[:4]:  # Limit to 4 posts for testing
                try:
                    # Wait for element to be fully loaded
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of(element)
                    )
                    
                    # Capture screenshot
                    screenshot = self.capture_post_screenshot(element)
                    if screenshot:
                        # Save screenshot to file
                        timestamp = int(time.time())
                        screenshot_path = f"post_screenshot_{timestamp}.png"
                        with open(screenshot_path, "wb") as f:
                            f.write(screenshot)
                        
                        posts_data.append({
                            'image_path': screenshot_path,
                            'timestamp': timestamp
                        })
                        
                except Exception as e:
                    print(f"Error processing post element: {str(e)}")
                    continue
                
                # Add random delay between posts
                time.sleep(random.uniform(2, 4))
            
            # Process posts using the new function signature
            return process_posts(posts_data)
            
        except Exception as e:
            print(f"Error fetching profile posts from {profile_url}: {str(e)}")
            return []

    def handle_security_check(self):
        """Handle LinkedIn security checks and reCAPTCHA."""
        try:
            # Check for checkpoint page
            if "checkpoint" in self.driver.current_url:
                print("LinkedIn security checkpoint detected. Please complete the verification manually.")
                print("You have 60 seconds to complete the verification...")
                time.sleep(60)  # Wait for manual verification
                return True
                
            # Check for reCAPTCHA
            recaptcha = self.driver.find_elements(By.CSS_SELECTOR, 
                "iframe[title*='reCAPTCHA'], " +
                "iframe[src*='recaptcha'], " +
                "div.g-recaptcha"
            )
            
            if recaptcha:
                print("reCAPTCHA detected. Please complete it manually in the Chrome window.")
                print("You have 60 seconds to complete the reCAPTCHA...")
                time.sleep(60)  # Increased time for manual completion
                return True
                
            # Check for security verification
            security_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "button[data-control-name='security_verification'], " +
                "button[data-control-name='security_check'], " +
                "button[data-control-name='verify_identity'], " +
                "div[data-control-name='security_verification'], " +
                "div[data-control-name='security_check'], " +
                "div[data-control-name='verify_identity']"
            )
            
            if security_elements:
                print("Security check detected. Please complete the verification manually in the Chrome window.")
                print("You have 60 seconds to complete the verification...")
                time.sleep(60)  # Increased time for manual verification
                return True
                
            # Check for bot detection
            bot_detection = self.driver.find_elements(By.CSS_SELECTOR,
                "iframe[src*='protechts.net'], " +
                "iframe[src*='security'], " +
                "div[data-control-name='bot_detection']"
            )
            
            if bot_detection:
                print("Bot detection triggered. Please complete any verification manually in the Chrome window.")
                print("You have 60 seconds to complete the verification...")
                time.sleep(60)  # Increased time for manual verification
                return True
                
            return False
            
        except Exception as e:
            print(f"Error checking for security measures: {str(e)}")
            return False

    def close(self):
        """Close the browser session."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.is_logged_in = False

def analyze_competitors(profile_urls, email=None, password=None):
    """Analyze multiple LinkedIn profiles and provide insights."""
    if not profile_urls:
        return {"error": "No profile URLs provided"}
    
    # Validate URLs
    valid_urls = []
    for url in profile_urls:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        if 'linkedin.com/in/' in url:
            valid_urls.append(url)
        else:
            print(f"Invalid LinkedIn URL: {url}")
    
    if not valid_urls:
        return {"error": "No valid LinkedIn profile URLs provided"}
    
    # Create LinkedIn session
    session = LinkedInSession()
    try:
        # Setup driver
        if not session.setup_driver():
            return {"error": "Failed to setup Chrome driver"}
        
        # Login if credentials provided
        if email and password:
            if not session.login(email, password):
                return {"error": "Failed to login to LinkedIn"}
        
        # Process each profile
        all_posts = []
        for url in valid_urls:
            print(f"\nAnalyzing profile: {url}")
            posts = session.fetch_profile_posts(url)
            if posts:
                all_posts.extend(posts)
        
        if not all_posts:
            return {"error": "No posts found from any of the provided profiles"}
        
        # Analyze posts using Gemini
        analysis_results = {
            "posting_frequency": analyze_posting_frequency(all_posts),
            "common_themes": analyze_common_themes(all_posts),
            "profile_analysis": analyze_profiles(valid_urls, all_posts),
            "actionable_insights": generate_actionable_insights(all_posts),
            "summary": generate_summary(valid_urls, all_posts)
        }
        
        return analysis_results
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return {"error": str(e)}
    finally:
        session.close()
