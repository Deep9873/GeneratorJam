from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime

# Import our models and services
from models import (
    GenerationRequest, 
    TextGenerationResponse, 
    ImageGenerationResponse, 
    HistoryItem,
    HistoryResponse
)
from services.gemini_service import GeminiService
from services.huggingface_service import HuggingFaceService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
gemini_service = GeminiService()
huggingface_service = HuggingFaceService()

# Create the main app without a prefix
app = FastAPI(title="Generator Jam API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "Generator Jam API is running!", "version": "1.0.0"}

@api_router.post("/generate/text", response_model=TextGenerationResponse)
async def generate_text_content(request: GenerationRequest):
    """Generate text content using Gemini AI"""
    try:
        if request.content_type not in ['blog', 'twitter', 'instagram', 'linkedin']:
            raise HTTPException(
                status_code=400, 
                detail="Invalid content type. Must be one of: blog, twitter, instagram, linkedin"
            )
        
        result = await gemini_service.generate_text_content(request.prompt, request.content_type)
        
        # Save to history
        history_item = HistoryItem(
            type="text",
            content_type=request.content_type,
            prompt=request.prompt,
            result=result.dict()
        )
        
        await db.history.insert_one(history_item.dict())
        
        return result
        
    except HTTPException as e:
        # Re-raise HTTP exceptions directly
        raise e
    except Exception as e:
        logging.error(f"Text generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")

@api_router.post("/generate/image", response_model=ImageGenerationResponse)
async def generate_image_content(request: GenerationRequest):
    """Generate image content using Hugging Face API"""
    try:
        if request.content_type != 'image':
            raise HTTPException(
                status_code=400, 
                detail="Content type must be 'image' for image generation"
            )
        # Use Hugging Face instead of Gemini
        result = await huggingface_service.generate_image(request.prompt)

        # Save to history
        history_item = HistoryItem(
            type="image",
            content_type=request.content_type,
            prompt=request.prompt,
            result=result.dict()
        )
        await db.history.insert_one(history_item.dict())
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Image generation failed: {str(e)}")
        if "rate limit" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again in a few minutes.")
        elif "loading" in str(e).lower():
            raise HTTPException(status_code=503, detail="AI model is loading. Please wait and try again.")
        else:
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

 
@api_router.get("/history", response_model=HistoryResponse)
async def get_history(limit: Optional[int] = 50, offset: Optional[int] = 0):
    """Get generation history"""
    try:
        # Get total count
        total = await db.history.count_documents({})
        
        # Get history items with pagination
        cursor = db.history.find({}).sort("timestamp", -1).skip(offset).limit(limit)
        history_docs = await cursor.to_list(length=limit)
        
        # Convert to HistoryItem objects
        history_items = []
        for doc in history_docs:
            # Convert MongoDB ObjectId to string for serialization
            doc['_id'] = str(doc['_id'])
            history_items.append(HistoryItem(**doc))
        
        return HistoryResponse(items=history_items, total=total)
        
    except Exception as e:
        logging.error(f"Failed to get history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")

@api_router.put("/history/{item_id}/favorite")
async def toggle_favorite(item_id: str):
    """Toggle favorite status of a history item"""
    try:
        result = await db.history.find_one({"id": item_id})
        if not result:
            raise HTTPException(status_code=404, detail="History item not found")
        
        new_favorite_status = not result.get("is_favorite", False)
        await db.history.update_one(
            {"id": item_id},
            {"$set": {"is_favorite": new_favorite_status}}
        )
        
        return {"success": True, "is_favorite": new_favorite_status}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to toggle favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle favorite")

@api_router.delete("/history/{item_id}")
async def delete_history_item(item_id: str):
    """Delete a history item"""
    try:
        result = await db.history.delete_one({"id": item_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="History item not found")
        
        return {"success": True, "message": "History item deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to delete history item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete history item")

@api_router.delete("/history")
async def clear_history():
    """Clear all history"""
    try:
        result = await db.history.delete_many({})
        return {"success": True, "deleted_count": result.deleted_count}
        
    except Exception as e:
        logging.error(f"Failed to clear history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear history")

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check MongoDB connection
        await db.command("ping")
        
        # Check Hugging Face service
        hf_healthy = await huggingface_service.health_check()
        
        return {
            "status": "healthy",
            "database": "connected",
            "gemini": "configured",
            "huggingface": "healthy" if hf_healthy else "unavailable",
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
