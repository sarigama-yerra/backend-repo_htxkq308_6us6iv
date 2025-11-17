import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Tailor, Service, PortfolioItem, Review, BlogPost, Booking, DeliveryUpdate

app = FastAPI(title="TailorHub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers
class IdResponse(BaseModel):
    id: str


def to_serializable(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if doc.get("_id"):
        doc["id"] = str(doc.pop("_id"))
    # Convert datetimes to isoformat
    for k, v in list(doc.items()):
        try:
            if hasattr(v, "isoformat"):
                doc[k] = v.isoformat()
        except Exception:
            pass
    return doc


@app.get("/")
def root():
    return {"message": "TailorHub API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "❌ Database not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Public content endpoints (read-only lists)
@app.get("/api/tailors", response_model=List[dict])
def list_tailors(limit: int = 20):
    docs = get_documents("tailor", {}, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/tailors", response_model=IdResponse)
def create_tailor(payload: Tailor):
    new_id = create_document("tailor", payload)
    return IdResponse(id=new_id)

@app.get("/api/services", response_model=List[dict])
def list_services(limit: int = 20):
    docs = get_documents("service", {}, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/services", response_model=IdResponse)
def create_service(payload: Service):
    new_id = create_document("service", payload)
    return IdResponse(id=new_id)

@app.get("/api/portfolio", response_model=List[dict])
def list_portfolio(limit: int = 20):
    docs = get_documents("portfolioitem", {}, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/portfolio", response_model=IdResponse)
def create_portfolio_item(payload: PortfolioItem):
    new_id = create_document("portfolioitem", payload)
    return IdResponse(id=new_id)

@app.get("/api/testimonials", response_model=List[dict])
def list_reviews(limit: int = 10):
    docs = get_documents("review", {}, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/testimonials", response_model=IdResponse)
def create_review(payload: Review):
    new_id = create_document("review", payload)
    return IdResponse(id=new_id)

@app.get("/api/blog", response_model=List[dict])
def list_blog(limit: int = 10):
    docs = get_documents("blogpost", {}, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/blog", response_model=IdResponse)
def create_blog(payload: BlogPost):
    new_id = create_document("blogpost", payload)
    return IdResponse(id=new_id)

# Booking & delivery
@app.post("/api/bookings", response_model=IdResponse)
def create_booking(payload: Booking):
    new_id = create_document("booking", payload)
    return IdResponse(id=new_id)

@app.get("/api/bookings", response_model=List[dict])
def list_bookings(email: Optional[str] = None, limit: int = 20):
    filt = {"email": email} if email else {}
    docs = get_documents("booking", filt, limit)
    return [to_serializable(d) for d in docs]

@app.post("/api/delivery", response_model=IdResponse)
def delivery_update(payload: DeliveryUpdate):
    new_id = create_document("deliveryupdate", payload)
    return IdResponse(id=new_id)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
