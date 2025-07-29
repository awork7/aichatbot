from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    user_id: Optional[str] = Field(None, description="User identifier")
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class DocumentUploadRequest(BaseModel):
    filename: str = Field(..., description="Document filename")
    content_type: str = Field(..., description="Document MIME type")
    
class AdminRequest(BaseModel):
    action: str = Field(..., description="Admin action to perform")
    parameters: Optional[dict] = Field(None, description="Action parameters")
