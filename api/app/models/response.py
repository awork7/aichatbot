from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"

class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI assistant response")
    sources: List[str] = Field(default=[], description="Information sources used")
    response_time: float = Field(..., description="Response time in seconds")
    session_id: str = Field(..., description="Chat session identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: ResponseStatus = Field(default=ResponseStatus.SUCCESS)
    
class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall system status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    components: dict = Field(..., description="Component health status")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="Request identifier")

class ServiceInfo(BaseModel):
    id: int = Field(..., description="Service ID")
    name: str = Field(..., description="Service name")
    description: Optional[str] = Field(None, description="Service description")
    icon: str = Field(..., description="Service icon")
    category: str = Field(..., description="Service category")

class ServicesResponse(BaseModel):
    services: List[ServiceInfo] = Field(..., description="Available banking services")
    total: int = Field(..., description="Total number of services")
