from fastapi import APIRouter, File, UploadFile, HTTPException
from src.config.settings import settings
import os

router = APIRouter()
recognition_engine = RecognitionEngine(
    mongodb_uri=settings.MONGODB_URI, 
    database_name=settings.DATABASE_NAME
)

@router.post("/recognize")
async def recognize_product(file: UploadFile = File(...)):
    """
    Recognize product from uploaded image
    
    Args:
        file (UploadFile): Uploaded image file
    
    Returns:
        dict: Recognized product details
    """
    try:
        # Ensure uploads directory exists
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Extract text from image
        extracted_text = recognition_engine.extract_text(file_path)
        
        # Find matching product
        product = recognition_engine.find_matching_product(extracted_text)
        
        # Clean up temporary file
        os.remove(file_path)
        
        if not product:
            raise HTTPException(status_code=404, detail="No matching product found")
        
        return {
            "product": product,
            "extracted_text": extracted_text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))