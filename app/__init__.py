from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os
from flask_uploads import configure_uploads
from flask_uploads import UploadSet, IMAGES

from .config import Config
from .auth import auth
from .clases.usuario import Usuario


# Inicializando y customizando un poco el LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Por favor, inicia sesión! :)"
login_manager.login_message_category = "info"

# current_file_path = os.path.abspath(os.path.dirname(__file__))
# images_path = os.path.join(current_file_path, "./uploaded_images/")

@login_manager.user_loader
def load_user(username):
    return Usuario.query(username)

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)

    photos = UploadSet('photos', IMAGES, default_dest=lambda app: app.config['UPLOAD_FOLDER'])
    configure_uploads(app, (photos,))

    login_manager.init_app(app)
    
    #Registrando el Blueprint auth, que incluye funciones de login, logout y registro de nuevos cajeros
    app.register_blueprint(auth)

    return app
