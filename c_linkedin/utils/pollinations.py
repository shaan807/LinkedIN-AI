import requests

def generate_image_from_prompt(prompt: str) -> bytes:
    """Fetch an image from Pollinations AI using a natural language prompt."""
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    response = requests.get(url)
    response.raise_for_status()
    return response.content
