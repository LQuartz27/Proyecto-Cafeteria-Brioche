#Creando nuestros formularios primer formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, PasswordField, FileField
# Images upload config
from flask_uploads import IMAGES
from flask_wtf.file import FileRequired, FileAllowed
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField("Acceder")


class NewCashierForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField("Crear cajero")


class ProductForm(FlaskForm):

    ref_number = StringField('Número de referencia', validators=[DataRequired()])
    product_name = StringField('Nombre del producto', validators=[DataRequired()])
    price = StringField('Precio', validators=[DataRequired()])
    qty = StringField('Precio', validators=[DataRequired()])
    photo = FileField('Foto', validators=[FileRequired(), FileAllowed(IMAGES, 'Images only!')])


class PasswordChangeForm(FlaskForm):
    prev_pass = StringField('Contraseña anterior', validators=[DataRequired()])
    new_pass = StringField('Nueva Contraseña', validators=[DataRequired()])
    confirm_pass = StringField('Confirmar Contraseña', validators=[DataRequired()])




    
    