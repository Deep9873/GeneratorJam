import os
import base64
import io
import asyncio
import aiohttp
from typing import Optional
from models import ImageGenerationResponse
from PIL import Image
import logging


logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.api_key = os.getenv('HF_TOKEN')
        if not self.api_key:
            raise ValueError("HF_TOKEN environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try multiple free models in order of preference
        self.models = [
            "black-forest-labs/FLUX.1-dev",
            "black-forest-labs/FLUX.1-schnell",
            stabilityai/stable-diffusion-xl-base-1.0,
            "stabilityai/stable-diffusion-3.5-large"
        ]
    
    async def generate_image(self, prompt: str, retry_count: int = 3) -> ImageGenerationResponse:
        """Generate image using Hugging Face API"""
        for model in self.models:
            try:
                return await self._generate_with_model(prompt, model)
            except Exception as e:
                logger.warning(f"Failed to generate with model {model}: {str(e)}")
                continue
        
        # If all models fail, raise the last error
        raise Exception("All image generation models failed. Please try again later.")
    
    async def _generate_with_model(self, prompt: str, model: str) -> ImageGenerationResponse:
        """Generate image with specific model"""
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 30,
                "guidance_scale": 8,
                "width": 512,
                "height": 512,
                 "negative_prompt": "blurry, distorted, abstract, low quality"
            }
        }
        
        timeout = aiohttp.ClientTimeout(total=60)  # 60 second timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(api_url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    return await self._process_image(image_bytes, prompt)
                elif response.status == 429:
                    raise Exception("Rate limit exceeded. Please try again in a few minutes.")
                elif response.status == 503:
                    error_data = await response.json()
                    if "loading" in str(error_data).lower():
                        # Model is loading, wait and retry
                        await asyncio.sleep(10)
                        return await self._generate_with_model(prompt, model)
                    else:
                        raise Exception(f"Service unavailable: {error_data}")
                else:
                    error_data = await response.text()
                    raise Exception(f"API error {response.status}: {error_data}")
    
    async def _process_image(self, image_bytes: bytes, prompt: str) -> ImageGenerationResponse:
        """Process image bytes into base64 response"""
        try:
            # Verify it's a valid image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return ImageGenerationResponse(
                image_base64=image_base64,
                prompt=prompt,
                dimensions=f"{image.width}x{image.height}",
                format="PNG"
            )
            
        except Exception as e:
            raise Exception(f"Failed to process generated image: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check if the service is healthy"""
        try:
            # Simple test with the first model
            api_url = f"https://api-inference.huggingface.co/models/{self.models[0]}"
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url, headers=self.headers) as response:
                    return response.status in [200, 503]  # 503 means model is available but loading
        except Exception:
            return False
