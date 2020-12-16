import os

class Config:
    # SECRET_KEY = 'SUPER SECRET'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = os.urandom(16)

    current_file_path = os.path.abspath(os.path.dirname(__file__))
    images_path = os.path.join(current_file_path, "../uploaded_images/")
    UPLOAD_FOLDER = images_path