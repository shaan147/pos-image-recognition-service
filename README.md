# POS Image Recognition Microservice

## Project Overview

This microservice is a crucial component of our Point of Sale (POS) system, designed to recognize products through image processing and text extraction.

## Project Purpose

The primary goal is to enable quick and accurate product identification by:
- Uploading product images
- Extracting text from images
- Matching products in the database
- Providing product details for self-checkout systems

## Folder Structure
pos-image-recognition-service/
│
├── src/                    # Main application source code
│   ├── config/             # Configuration management
│   │   ├── database.py     # Database connection settings
│   │   └── settings.py     # Application-wide settings
│   │
│   ├── models/             # Data models and schemas
│   │   ├── product.py      # Product data model
│   │   └── recognition.py  # Image recognition related models
│   │
│   ├── services/           # Business logic and core services
│   │   ├── image_processor.py   # Image preprocessing
│   │   └── recognition_engine.py# Product recognition logic
│   │
│   ├── routes/             # API endpoint definitions
│   │   └── recognition.py  # Image recognition routes
│   │
│   └── utils/              # Utility functions and helpers
│       └── exceptions.py   # Custom exception handling
│
├── tests/                  # Unit and integration tests
│   ├── test_recognition.py # Tests for recognition service
│   └── test_database.py    # Database connection tests
│
├── ml_models/              # Machine learning model storage
│
├── .env                    # Environment configuration
├── requirements.txt        # Python dependency list
└── README.md               # Project documentation

## 🧰 Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Backend** | FastAPI |
| **OCR** | Tesseract |
| **Database** | MongoDB |
| **Text Matching** | FuzzyWuzzy |
| **Image Processing** | OpenCV |

## 🔧 Prerequisites

- Python 3.8+
- MongoDB
- Tesseract OCR installed

## 🛠 Installation

1. Clone the repository
```bash git clone https://github.com/yourusername/pos-image-recognition-service.git 
cd pos-image-recognition-service

python -m venv venv
source venv/bin/activate  # Unix
# OR
venv\Scripts\activate     # Windows

pip install -r requirements.txt


## 🔍 How It Works

- **Image Upload**: Client uploads a product image
- **Text Extraction**: Tesseract OCR extracts text from image
- **Product Matching**:
    - Uses fuzzy matching algorithm
    - Searches MongoDB for closest product match
- **Result**: Returns matched product details

## 📡 API Endpoints

`POST /api/recognition/recognize`
- Uploads image
- Returns product details