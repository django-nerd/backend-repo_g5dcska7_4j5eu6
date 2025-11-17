import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document
from schemas import ContactInquiry

app = FastAPI(title="BCX API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "BCX Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the BCX backend API!"}

@app.get("/api/services")
def get_services():
    services = [
        {
            "key": "landing",
            "name": "Landing Pages",
            "tagline": "High-converting single-page sites",
            "features": [
                "Modern responsive design",
                "Fast load times",
                "SEO friendly sections",
                "Contact & lead capture"
            ],
            "price": 399
        },
        {
            "key": "multipage",
            "name": "Multi‑page Websites",
            "tagline": "Full company sites with multiple pages",
            "features": [
                "Up to 6 core pages",
                "CMS-ready structure",
                "Blog/news setup",
                "Analytics & SEO basics"
            ],
            "price": 1299
        },
        {
            "key": "shop",
            "name": "Shop Pages",
            "tagline": "E‑commerce storefronts that sell",
            "features": [
                "Product catalog & search",
                "Checkout integration",
                "Promo banners & coupons",
                "Order notifications"
            ],
            "price": 1999
        }
    ]
    return {"services": services}

@app.post("/api/contact")
def submit_contact(inquiry: ContactInquiry):
    try:
        doc_id = create_document("contactinquiry", inquiry)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
