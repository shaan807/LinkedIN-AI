import base64
from PIL import Image
import io
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# List of available models in order of preference
GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

# Initialize model as None
model = None

def get_working_model():
    """Try to initialize each model in order of preference"""
    global model
    if model is not None:
        return model
        
    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple prompt
            response = model.generate_content("Test connection")
            if response:
                return model
        except Exception as e:
            print(f"Failed to initialize {model_name}: {str(e)}")
            continue
    raise Exception("No working Gemini model found")

def capture_post_screenshot(driver, element):
    """Capture screenshot of a post element."""
    try:
        # Wait for element to be fully loaded and visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of(element)
        )
        
        # Scroll to element with smooth behavior
        driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'center'
            });
        """, element)
        time.sleep(random.uniform(1, 2))
        
        # Get element location and size with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                location = element.location
                size = element.size
                
                # Validate dimensions
                if size['width'] <= 0 or size['height'] <= 0:
                    raise ValueError("Invalid element dimensions")
                    
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Getting element dimensions attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
        
        # Take full page screenshot with retry
        for attempt in range(max_retries):
            try:
                screenshot = driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot))
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Screenshot attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
        
        # Calculate crop coordinates with padding
        padding = 20
        left = max(0, location['x'] - padding)
        top = max(0, location['y'] - padding)
        right = min(image.width, location['x'] + size['width'] + padding)
        bottom = min(image.height, location['y'] + size['height'] + padding)
        
        # Ensure valid dimensions
        if right <= left or bottom <= top:
            print("Invalid element dimensions, trying alternative capture method...")
            # Try capturing the entire viewport
            viewport_width = driver.execute_script("return window.innerWidth;")
            viewport_height = driver.execute_script("return window.innerHeight;")
            left = max(0, location['x'] - viewport_width//4)
            top = max(0, location['y'] - viewport_height//4)
            right = min(image.width, location['x'] + size['width'] + viewport_width//4)
            bottom = min(image.height, location['y'] + size['height'] + viewport_height//4)
            
            if right <= left or bottom <= top:
                print("Alternative capture method failed, using full screenshot")
                return None
        
        # Crop and save with error handling
        try:
            element_screenshot = image.crop((left, top, right, bottom))
            
            # Convert to base64 for Gemini
            buffered = io.BytesIO()
            element_screenshot.save(buffered, format="PNG", optimize=True)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            print(f"Error processing screenshot: {str(e)}")
            return None
        
    except Exception as e:
        print(f"Error capturing post screenshot: {str(e)}")
        return None

def analyze_post_image(image_path):
    """Analyze a post image using Gemini Vision"""
    try:
        model = get_working_model()
        
        # Load and prepare the image
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # Create image part for Gemini
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_data).decode('utf-8')
            }
        ]
        
        # Generate content with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    [
                        "Analyze this LinkedIn post image. Extract and summarize the content, including any text, images, or media. Focus on the main message and key points.",
                        *image_parts
                    ]
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)  # Wait before retrying
                
        return None
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None

def process_posts(posts_data):
    """Process and analyze multiple posts"""
    results = []
    for post in posts_data:
        try:
            if post.get('image_path'):
                analysis = analyze_post_image(post['image_path'])
                if analysis:
                    post['content_analysis'] = analysis
            results.append(post)
        except Exception as e:
            print(f"Error processing post: {str(e)}")
            continue
    return results 