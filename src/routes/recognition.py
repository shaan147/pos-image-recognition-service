from fastapi import APIRouter, File, UploadFile, HTTPException
from src.services.recognition_engine import RecognitionEngine
from src.config.settings import settings
import os
import json
from bson import ObjectId

# Custom JSON encoder for MongoDB objects
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if hasattr(obj, 'isoformat'):  # For datetime objects
            return obj.isoformat()
        return super(MongoJSONEncoder, self).default(obj)

# Helper function to convert MongoDB document to JSON-compatible dict
def mongo_to_dict(obj):
    if isinstance(obj, dict):
        return {k: mongo_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [mongo_to_dict(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif hasattr(obj, 'isoformat'):  # For datetime objects
        return obj.isoformat()
    else:
        return obj

router = APIRouter()
recognition_engine = RecognitionEngine(
    mongodb_uri=settings.MONGODB_URI, 
    database_name=settings.DATABASE_NAME
)

@router.post("/recognize")
async def recognize_product(file: UploadFile = File(...)):
    """
    Recognize product from uploaded image
    """
    try:
        # Ensure uploads directory exists
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        print(f"Received file: {file.filename}")
        
        # Extract text from image
        extracted_text = recognition_engine.extract_text(file_path)
        print(f"Extracted text: {extracted_text}")
        
        # Find matching product
        product = recognition_engine.find_matching_product(extracted_text)
        print(f"Product: {product}")
        
        # Clean up temporary file
        os.remove(file_path)
        
        if not product:
            raise HTTPException(status_code=404, detail="No matching product found")
        
        # Convert MongoDB document to JSON-compatible dict
        product_dict = mongo_to_dict(product)
        
        return {
            "product": product_dict,
            "extracted_text": extracted_text
        }
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))