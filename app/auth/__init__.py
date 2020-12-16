from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Importamos esto acá abajo para que después de que creemos el
#blueprint, se generen todos los views, y ahí importemos todos esos views
# y configuremos la aplicación

from . import routes