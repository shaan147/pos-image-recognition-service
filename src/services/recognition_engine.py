import pytesseract
import cv2
import numpy as np
from pymongo import MongoClient
from fuzzywuzzy import fuzz

class RecognitionEngine:
    def __init__(self, mongodb_uri, database_name):
        """
        Initialize recognition engine with database connection
        
        Args:
            mongodb_uri (str): MongoDB connection string
            database_name (str): Name of the database
        """
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.products_collection = self.db['products']
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for better OCR recognition
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            numpy.ndarray: Preprocessed image
        """
        # Read the image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Apply deskewing
        gray = self._deskew(gray)
        
        return gray
    
    def _deskew(self, image):
        """
        Deskew the image to improve OCR accuracy
        
        Args:
            image (numpy.ndarray): Input image
        
        Returns:
            numpy.ndarray: Deskewed image
        """
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    def extract_text(self, image_path):
        """
        Extract text from the image using Tesseract OCR
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            str: Extracted text
        """
        # Preprocess image
        preprocessed_image = self.preprocess_image(image_path)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(preprocessed_image)
        return text.strip()
    
    def find_matching_product(self, extracted_text):
        """
        Find the most matching product based on extracted text
        
        Args:
            extracted_text (str): Text extracted from the image
        
        Returns:
            dict: Matching product or None
        """
        # Normalize extracted text
        normalized_text = extracted_text.lower()
        
        # Find products with the highest text match
        best_match = None
        best_score = 0
        
        # Query all products (you might want to add indexing or limit this in a large database)
        for product in self.products_collection.find():
            # Check product name and description
            name_score = fuzz.partial_ratio(normalized_text, product['name'].lower())
            description_score = fuzz.partial_ratio(normalized_text, product.get('description', '').lower())
            
            # Combine scores
            total_score = max(name_score, description_score)
            
            if total_score > best_score and total_score > 60:  # Adjust threshold as needed
                best_match = product
                best_score = total_score
        
        return best_match