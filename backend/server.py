from fastapi import FastAPI, APIRouter, HTTPException, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import os

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(
    MONGO_URL,
    tlsCAFile=certifi.where()
)

import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from models import (
    GenerationRequest,
    TextGenerationResponse,
    ImageGenerationResponse,
    HistoryItem,
    HistoryResponse
)
from services.gemini_service import GeminiService
from services.huggingface_service import HuggingFaceService

# === Load Environment ===
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# === MongoDB Connection ===
mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME')]

# === Initialize services ===
gemini_service = GeminiService()
huggingface_service = HuggingFaceService()

# === FastAPI Setup ===
app = FastAPI(title="Generator Jam API", version="1.0.0")
api_router = APIRouter(prefix="/api")

# === API Routes ===

@api_router.get("/")
async def root():
    return {"message": "Generator Jam API is running!", "version": "1.0.0"}


@api_router.post("/generate/text", response_model=TextGenerationResponse)
async def generate_text_content(request: GenerationRequest):
    try:
        if request.content_type not in ['blog', 'twitter', 'instagram', 'linkedin']:
            raise HTTPException(
                status_code=400,
                detail="Invalid content type. Must be one of: blog, twitter, instagram, linkedin"
            )

        result = await gemini_service.generate_text_content(request.prompt, request.content_type)

        history_item = HistoryItem(
             user_id=user_id,
            type="text",
            content_type=request.content_type,
            prompt=request.prompt,
            result=result.dict()
        )
        await db.history.insert_one(history_item.dict())

        return result

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Text generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")


@api_router.post("/generate/image", response_model=ImageGenerationResponse)
async def generate_image_content(request: GenerationRequest):
    try:
        if request.content_type != 'image':
            raise HTTPException(status_code=400, detail="Content type must be 'image' for image generation")

        result = await huggingface_service.generate_image(request.prompt)

        history_item = HistoryItem(
             user_id=user_id,
            type="image",
            content_type=request.content_type,
            prompt=request.prompt,
            result=result.dict()
        )
        await db.history.insert_one(history_item.dict())

        return result

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Image generation failed: {str(e)}")
        if "rate limit" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again in a few minutes.")
        elif "loading" in str(e).lower():
            raise HTTPException(status_code=503, detail="AI model is loading. Please wait and try again.")
        else:
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@api_router.get("/history", response_model=HistoryResponse)
async def get_history(request: Request, limit: Optional[int] = 50, offset: Optional[int] = 0):
    try:
        user_id = get_user_id(request)
        total = await db.history.count_documents({"user_id": user_id})
        cursor = db.history.find({"user_id": user_id}).sort("timestamp", -1).skip(offset).limit(limit)
        history_docs = await cursor.to_list(length=limit)

        history_items = []
        for doc in history_docs:
            doc['_id'] = str(doc['_id'])
            history_items.append(HistoryItem(**doc))

        return HistoryResponse(items=history_items, total=total)

    except Exception as e:
        logging.error(f"Failed to get history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")

@api_router.put("/history/{item_id}/favorite")
async def toggle_favorite(item_id: str, request: Request):
    try:
        user_id = get_user_id(request)

        result = await db.history.find_one({"id": item_id, "user_id": user_id})
        if not result:
            raise HTTPException(status_code=404, detail="History item not found")

        new_favorite_status = not result.get("is_favorite", False)
        await db.history.update_one(
            {"id": item_id, "user_id": user_id},
            {"$set": {"is_favorite": new_favorite_status}}
        )

        return {"success": True, "is_favorite": new_favorite_status}

    except Exception as e:
        logging.error(f"Failed to toggle favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle favorite")

@api_router.delete("/history/{item_id}")
async def delete_history_item(item_id: str, request: Request):
    try:
        user_id = get_user_id(request)

        result = await db.history.delete_one({"id": item_id, "user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="History item not found")

        return {"success": True, "message": "History item deleted"}

    except Exception as e:
        logging.error(f"Failed to delete history item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete history item")

@api_router.delete("/history")
async def clear_history(request: Request):
    try:
        user_id = get_user_id(request)
        result = await db.history.delete_many({"user_id": user_id})
        return {"success": True, "deleted_count": result.deleted_count}

    except Exception as e:
        logging.error(f"Failed to clear history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear history")

@api_router.get("/health")
async def health_check():
    try:
        logging.info("Health check: Pinging MongoDB...")
        await db.command("ping")

        logging.info("Health check: Pinging Hugging Face...")
        hf_healthy = await huggingface_service.health_check()

        logging.info("Health check successful.")
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


# === Register API and CORS Middleware ===
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
