from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class GenerationRequest(BaseModel):
    prompt: str
    content_type: str  # blog, twitter, instagram, linkedin, image
    
class TextGenerationResponse(BaseModel):
    content: str
    title: Optional[str] = None
    hashtags: Optional[List[str]] = None
    word_count: Optional[int] = None
    character_count: Optional[int] = None
    reading_time: Optional[str] = None

class ImageGenerationResponse(BaseModel):
    image_base64: str
    prompt: str
    dimensions: str
    format: str = "PNG"

class HistoryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str  # ✅ Add this line
    type: str  # text or image
    content_type: str
    prompt: str
    result: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_favorite: bool = False
        

class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int
