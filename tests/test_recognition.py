import unittest
import os
import cv2
import numpy as np
from src.services.recognition_engine import RecognitionEngine
from unittest.mock import MagicMock, patch

class TestRecognitionEngine(unittest.TestCase):
    def setUp(self):
        # Mock MongoDB for testing
        self.mongo_mock = patch('pymongo.MongoClient').start()
        self.engine = RecognitionEngine("mongodb://localhost:27017", "test_db")
        
    def tearDown(self):
        patch.stopall()
        
    def test_preprocess_image(self):
        # Create a simple test image
        test_image = np.ones((100, 100), dtype=np.uint8) * 255
        cv2.imwrite("test_image.jpg", test_image)
        
        processed = self.engine.preprocess_image("test_image.jpg")
        self.assertIsNotNone(processed)
        
        # Clean up
        os.remove("test_image.jpg")
        
    def test_extract_text(self):
        # Mock the preprocess_image and pytesseract methods
        self.engine.preprocess_image = MagicMock(return_value=np.ones((100, 100), dtype=np.uint8))
        with patch('pytesseract.image_to_string', return_value="sample product text"):
            text = self.engine.extract_text("dummy_path.jpg")
            self.assertEqual(text, "sample product text")
            
    def test_find_matching_product(self):
        # Mock products collection
        self.engine.products_collection.find = MagicMock(return_value=[
            {"_id": "1", "name": "Test Product", "description": "Sample description"}
        ])
        
        # Test with matching text
        product = self.engine.find_matching_product("test product")
        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Test Product")
        
        # Test with non-matching text
        self.engine.products_collection.find = MagicMock(return_value=[
            {"_id": "1", "name": "Test Product", "description": "Sample description"}
        ])
        product = self.engine.find_matching_product("completely different")
        self.assertIsNone(product)

if __name__ == '__main__':
    unittest.main()