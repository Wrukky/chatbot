import base64
import requests
from io import BytesIO
from PIL import Image

# Function to encode image
def encode_image(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

# API details
API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJycnVrczIyMTBAZ21haWwuY29tIiwiaWF0IjoxNzQyNzI4MjI0fQ.2MAEqwoqta3fFgwyvhboGiNHTrheYE8kR6cTjgc56X8"  # Replace with your actual API key

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# Function to send image to Pixtral API
def chat_with_pixtral(image_path, text_prompt):
    base64_img = encode_image(image_path)

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "model": "mistralai/Pixtral-12B-2409",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    return response.json()

# Run chatbot
if __name__ == "__main__":
    image_path = "path_to_your_image.png"  # Change this to an actual image path
    prompt = "What is in this image?"
    response = chat_with_pixtral(image_path, prompt)
    
    print(response)
