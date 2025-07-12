#!/usr/bin/env python3
import requests
import json
import time
import os
import sys
import base64
from PIL import Image
import io

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://c55a0498-f053-4587-958c-a1cde3ee5eef.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

def test_health_check():
    """Test health check endpoint"""
    try:
        print(f"Testing health check at {API_URL}/health")
        response = requests.get(f"{API_URL}/health")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check endpoint working")
            print(f"Status: {data['status']}")
            print(f"Database: {data['database']}")
            print(f"Gemini: {data['gemini']}")
            print(f"Hugging Face: {data['huggingface']}")
            return True
        else:
            print(f"❌ Health check failed with status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_generate_text(content_type):
    """Test text generation for different content types"""
    prompts = {
        "blog": "Write about the future of artificial intelligence",
        "twitter": "Write a tweet about productivity tips",
        "instagram": "Write an Instagram caption for a sunset photo",
        "linkedin": "Write a LinkedIn post about career development"
    }
    
    try:
        payload = {
            "prompt": prompts[content_type],
            "content_type": content_type
        }
        print(f"Testing {content_type} generation with prompt: {payload['prompt']}")
        response = requests.post(f"{API_URL}/generate/text", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {content_type.capitalize()} text generation working")
            print(f"Content: {data['content'][:100]}...")
            if "hashtags" in data and data["hashtags"]:
                print(f"Hashtags: {data['hashtags']}")
            if "title" in data and data["title"]:
                print(f"Title: {data['title']}")
            return True
        else:
            print(f"❌ {content_type.capitalize()} text generation failed with status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ {content_type.capitalize()} text generation error: {e}")
        return False

def test_generate_image():
    """Test image generation"""
    try:
        payload = {
            "prompt": "A beautiful mountain landscape",
            "content_type": "image"
        }
        print(f"Testing image generation with prompt: {payload['prompt']}")
        response = requests.post(f"{API_URL}/generate/image", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Image generation working")
            print(f"Dimensions: {data['dimensions']}")
            print(f"Format: {data['format']}")
            
            # Verify the base64 image can be decoded
            try:
                image_data = base64.b64decode(data["image_base64"])
                image = Image.open(io.BytesIO(image_data))
                print(f"Image size: {image.size}")
                return True
            except Exception as e:
                print(f"❌ Failed to decode base64 image: {e}")
                return False
        else:
            print(f"❌ Image generation failed with status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return False

def test_history_operations():
    """Test history operations (get, favorite, delete, clear)"""
    try:
        # Get history
        print("Testing get history...")
        response = requests.get(f"{API_URL}/history")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get history working")
            print(f"Total items: {data['total']}")
            
            if data['total'] > 0:
                # Test favorite toggle
                item_id = data['items'][0]['id']
                print(f"Testing favorite toggle for item {item_id}...")
                response = requests.put(f"{API_URL}/history/{item_id}/favorite")
                
                if response.status_code == 200:
                    fav_data = response.json()
                    print("✅ Toggle favorite working")
                    print(f"Is favorite: {fav_data['is_favorite']}")
                    
                    # Test delete item
                    print(f"Testing delete item {item_id}...")
                    response = requests.delete(f"{API_URL}/history/{item_id}")
                    
                    if response.status_code == 200:
                        del_data = response.json()
                        print("✅ Delete history item working")
                        print(f"Success: {del_data['success']}")
                    else:
                        print(f"❌ Delete history item failed with status code {response.status_code}")
                        print(response.text)
                else:
                    print(f"❌ Toggle favorite failed with status code {response.status_code}")
                    print(response.text)
            
            # Test clear history
            print("Testing clear history...")
            response = requests.delete(f"{API_URL}/history")
            
            if response.status_code == 200:
                clear_data = response.json()
                print("✅ Clear history working")
                print(f"Deleted count: {clear_data['deleted_count']}")
                return True
            else:
                print(f"❌ Clear history failed with status code {response.status_code}")
                print(response.text)
                return False
        else:
            print(f"❌ Get history failed with status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ History operations error: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    try:
        # Test invalid content type
        print("Testing invalid content type...")
        payload = {
            "prompt": "Test invalid content type",
            "content_type": "invalid"
        }
        response = requests.post(f"{API_URL}/generate/text", json=payload)
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Error handling for invalid content type working")
            print(f"Error detail: {data['detail']}")
        else:
            print(f"❌ Error handling for invalid content type failed with status code {response.status_code}")
            print(response.text)
        
        # Test wrong content type for image
        print("Testing wrong content type for image...")
        payload = {
            "prompt": "Test wrong content type for image",
            "content_type": "blog"
        }
        response = requests.post(f"{API_URL}/generate/image", json=payload)
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Error handling for wrong content type in image generation working")
            print(f"Error detail: {data['detail']}")
            return True
        else:
            print(f"❌ Error handling for wrong content type in image generation failed with status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"Testing Generator Jam backend API at {API_URL}")
    print("=" * 80)
    
    # Test health check
    health_ok = test_health_check()
    print("=" * 80)
    
    if not health_ok:
        print("❌ Health check failed, skipping remaining tests")
        return
    
    # Test text generation
    for content_type in ["blog", "twitter", "instagram", "linkedin"]:
        test_generate_text(content_type)
        print("=" * 80)
    
    # Test image generation
    test_generate_image()
    print("=" * 80)
    
    # Test history operations
    test_history_operations()
    print("=" * 80)
    
    # Test error handling
    test_error_handling()
    print("=" * 80)
    
    print("All tests completed!")

if __name__ == "__main__":
    run_all_tests()