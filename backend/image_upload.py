import os
from werkzeug.utils import secure_filename

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(file):
    """
    Saves an uploaded image file to the frontend/static/images folder.
    Returns the relative path (e.g., 'images/filename.jpg') if successful,
    or None if no file is uploaded or file type is not allowed.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return f"images/{filename}"
    return None
