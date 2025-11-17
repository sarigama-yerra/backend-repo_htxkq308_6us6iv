"""
Database Schemas for Tailor Platform

Each Pydantic model corresponds to a MongoDB collection. The collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Tailor(BaseModel):
    name: str = Field(..., description="Tailor or shop name")
    bio: Optional[str] = Field(None, description="Short biography/intro")
    avatar_url: Optional[str] = Field(None, description="Profile image URL")
    location: Optional[str] = Field(None, description="City / area")
    rating: Optional[float] = Field(4.8, ge=0, le=5)
    services: List[str] = Field(default_factory=list, description="Service tags offered")

class Service(BaseModel):
    title: str
    description: Optional[str] = None
    price_from: Optional[float] = Field(None, ge=0)
    duration_days: Optional[int] = Field(None, ge=0)

class PortfolioItem(BaseModel):
    tailor_name: Optional[str] = None
    title: str
    image_url: str
    description: Optional[str] = None

class Review(BaseModel):
    tailor_name: Optional[str] = None
    customer_name: str
    rating: float = Field(..., ge=0, le=5)
    comment: str

class BlogPost(BaseModel):
    title: str
    excerpt: Optional[str] = None
    cover_url: Optional[str] = None
    content: Optional[str] = None

class Booking(BaseModel):
    customer_name: str
    email: EmailStr
    phone: Optional[str] = None
    service: str
    tailor_name: Optional[str] = None
    notes: Optional[str] = None
    status: str = Field("requested", description="requested|confirmed|in-progress|ready|delivered")

class DeliveryUpdate(BaseModel):
    booking_id: str
    status: str
    message: Optional[str] = None
