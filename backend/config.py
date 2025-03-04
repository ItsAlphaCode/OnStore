import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))
    BASE_DIR = os.getcwd()  # Or use a specific base directory
    STORAGE_FOLDER = os.path.join(BASE_DIR, 'storage')
    UPLOAD_FOLDER = os.path.join(STORAGE_FOLDER, 'uploaded_documents')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app', 'frontend', 'static')
    SESSION_FOLDER = os.path.join(STORAGE_FOLDER, 'sessions')
    INDEX_FOLDER = os.path.join(STORAGE_FOLDER, '.byaldi')
    DEFAULT_IMAGE_HEIGHT = 280
    DEFAULT_IMAGE_WIDTH = 280