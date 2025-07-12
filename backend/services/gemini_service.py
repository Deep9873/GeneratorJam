import os
import requests
from models import TextGenerationResponse, ImageGenerationResponse

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent"

    async def generate_text_content(self, prompt: str, content_type: str) -> TextGenerationResponse:
        # Compose a system prompt based on content_type
        system_prompts = {
            'blog': "You are a professional blog writer. Create engaging, well-structured blog posts.",
            'twitter': "You are a social media expert specializing in Twitter content. Create engaging tweets.",
            'instagram': "You are an Instagram content creator expert. Create engaging Instagram captions.",
            'linkedin': "You are a professional LinkedIn content strategist. Create professional LinkedIn posts."
        }
        system_prompt = system_prompts.get(content_type, "You are a helpful assistant.")

        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_prompt}\n\n{prompt}"}
                    ]
                }
            ]
        }
        response = requests.post(self.api_url, headers=headers, params=params, json=data)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} {response.text}")
        result = response.json()
        # Extract the generated text
        try:
            text = result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        return TextGenerationResponse(content=text)

    # async def generate_image_content(self, prompt: str) -> ImageGenerationResponse:
        api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-preview-image-generation:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "response_mime_type": "image/png"
        }
        response = requests.post(api_url, headers=headers, params=params, json=data)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} {response.text}")
        result = response.json()
        try:
            image_base64 = result['candidates'][0]['content']['parts'][0]['inlineData']['data']
        except Exception:
            image_base64 = ''
        return ImageGenerationResponse(
            image_base64=image_base64,
            prompt=prompt,
            dimensions="512x512",
            format="PNG"
        )

