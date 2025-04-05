import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_path, target_size=(224, 224)):
        """
        Preprocess image for model inference
        
        Args:
            image_path (str): Path to the image file
            target_size (tuple): Desired image size for model input
        
        Returns:
            numpy.ndarray: Preprocessed image
        """
        try:
            # Read image using OpenCV
            img = cv2.imread(image_path)
            
            # Resize image
            img_resized = cv2.resize(img, target_size)
            
            # Normalize pixel values
            img_normalized = img_resized / 255.0
            
            # Add batch dimension
            img_processed = np.expand_dims(img_normalized, axis=0)
            
            return img_processed
        
        except Exception as e:
            raise ValueError(f"Image preprocessing failed: {str(e)}")