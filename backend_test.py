#!/usr/bin/env python3
import requests
import json
import time
import unittest
import os
import sys
import base64
from PIL import Image
import io
import uuid

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://c55a0498-f053-4587-958c-a1cde3ee5eef.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class GeneratorJamBackendTest(unittest.TestCase):
    """Test suite for Generator Jam backend API"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_url = API_URL
        self.history_items = []  # Store created history items for cleanup
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up any remaining history items
        try:
            for item_id in self.history_items:
                requests.delete(f"{self.api_url}/history/{item_id}")
        except Exception as e:
            print(f"Error during teardown: {e}")
    
    def test_01_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.api_url}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"], "connected")
        self.assertEqual(data["gemini"], "configured")
        # Hugging Face might be "healthy" or "unavailable" depending on the service status
        self.assertIn(data["huggingface"], ["healthy", "unavailable"])
        print("✅ Health check endpoint working")
    
    def test_02_generate_text_blog(self):
        """Test text generation for blog content"""
        payload = {
            "prompt": "Write about the future of artificial intelligence",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIn("title", data)
        self.assertIn("word_count", data)
        self.assertIn("reading_time", data)
        
        # Store the history item ID for cleanup
        history_response = requests.get(f"{self.api_url}/history")
        history_data = history_response.json()
        for item in history_data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ Blog text generation working")
    
    def test_03_generate_text_twitter(self):
        """Test text generation for Twitter content"""
        payload = {
            "prompt": "Write a tweet about productivity tips",
            "content_type": "twitter"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIn("hashtags", data)
        self.assertIn("character_count", data)
        
        # Store the history item ID for cleanup
        history_response = requests.get(f"{self.api_url}/history")
        history_data = history_response.json()
        for item in history_data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ Twitter text generation working")
    
    def test_04_generate_text_instagram(self):
        """Test text generation for Instagram content"""
        payload = {
            "prompt": "Write an Instagram caption for a sunset photo",
            "content_type": "instagram"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIn("hashtags", data)
        self.assertIn("character_count", data)
        
        # Store the history item ID for cleanup
        history_response = requests.get(f"{self.api_url}/history")
        history_data = history_response.json()
        for item in history_data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ Instagram text generation working")
    
    def test_05_generate_text_linkedin(self):
        """Test text generation for LinkedIn content"""
        payload = {
            "prompt": "Write a LinkedIn post about career development",
            "content_type": "linkedin"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIn("hashtags", data)
        self.assertIn("character_count", data)
        
        # Store the history item ID for cleanup
        history_response = requests.get(f"{self.api_url}/history")
        history_data = history_response.json()
        for item in history_data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ LinkedIn text generation working")
    
    def test_06_generate_image(self):
        """Test image generation"""
        payload = {
            "prompt": "A beautiful mountain landscape",
            "content_type": "image"
        }
        response = requests.post(f"{self.api_url}/generate/image", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("image_base64", data)
        self.assertIn("prompt", data)
        self.assertIn("dimensions", data)
        self.assertIn("format", data)
        
        # Verify the base64 image can be decoded
        try:
            image_data = base64.b64decode(data["image_base64"])
            image = Image.open(io.BytesIO(image_data))
            self.assertIsNotNone(image)
        except Exception as e:
            self.fail(f"Failed to decode base64 image: {e}")
        
        # Store the history item ID for cleanup
        history_response = requests.get(f"{self.api_url}/history")
        history_data = history_response.json()
        for item in history_data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ Image generation working")
    
    def test_07_get_history(self):
        """Test getting generation history"""
        # First, generate some content to ensure history exists
        payload = {
            "prompt": "Write about history test",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Get history
        response = requests.get(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertIn("total", data)
        self.assertGreater(data["total"], 0)
        
        # Store the history item ID for cleanup
        for item in data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                self.history_items.append(item["id"])
                break
        
        print("✅ Get history working")
    
    def test_08_toggle_favorite(self):
        """Test toggling favorite status"""
        # First, generate some content to ensure history exists
        payload = {
            "prompt": "Write about favorite test",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Get history to find the item ID
        response = requests.get(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        item_id = None
        for item in data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                item_id = item["id"]
                self.history_items.append(item_id)
                break
        
        self.assertIsNotNone(item_id, "Could not find the generated item in history")
        
        # Toggle favorite status
        response = requests.put(f"{self.api_url}/history/{item_id}/favorite")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertTrue(data["is_favorite"])
        
        # Toggle again to revert
        response = requests.put(f"{self.api_url}/history/{item_id}/favorite")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertFalse(data["is_favorite"])
        
        print("✅ Toggle favorite working")
    
    def test_09_delete_history_item(self):
        """Test deleting a history item"""
        # First, generate some content to ensure history exists
        payload = {
            "prompt": "Write about delete test",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Get history to find the item ID
        response = requests.get(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        item_id = None
        for item in data["items"]:
            if item["prompt"] == payload["prompt"] and item["content_type"] == payload["content_type"]:
                item_id = item["id"]
                break
        
        self.assertIsNotNone(item_id, "Could not find the generated item in history")
        
        # Delete the item
        response = requests.delete(f"{self.api_url}/history/{item_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify it's deleted
        response = requests.get(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        found = False
        for item in data["items"]:
            if item["id"] == item_id:
                found = True
                break
        
        self.assertFalse(found, "Item was not deleted from history")
        
        print("✅ Delete history item working")
    
    def test_10_clear_history(self):
        """Test clearing all history"""
        # First, generate some content to ensure history exists
        payload = {
            "prompt": "Write about clear history test",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Clear all history
        response = requests.delete(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify history is empty
        response = requests.get(f"{self.api_url}/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 0)
        self.assertEqual(len(data["items"]), 0)
        
        print("✅ Clear history working")
    
    def test_11_error_handling_invalid_content_type(self):
        """Test error handling for invalid content type"""
        payload = {
            "prompt": "Test invalid content type",
            "content_type": "invalid"
        }
        response = requests.post(f"{self.api_url}/generate/text", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)
        
        print("✅ Error handling for invalid content type working")
    
    def test_12_error_handling_image_content_type(self):
        """Test error handling for wrong content type in image generation"""
        payload = {
            "prompt": "Test wrong content type for image",
            "content_type": "blog"
        }
        response = requests.post(f"{self.api_url}/generate/image", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)
        
        print("✅ Error handling for wrong content type in image generation working")

if __name__ == "__main__":
    print(f"Testing Generator Jam backend API at {API_URL}")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)