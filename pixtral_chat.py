import os
import base64
import requests
from io import BytesIO
from PIL import Image

# Load API details from environment variables
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# Function to encode an image to base64
def encode_image(img_path):
    img = Image.open(img_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

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
    image_path = "path_to_your_image.png"  # Replace with an actual image path
    prompt = "What is in this image?"
    response = chat_with_pixtral(image_path, prompt)
    print(response)
