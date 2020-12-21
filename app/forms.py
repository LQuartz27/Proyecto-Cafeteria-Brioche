#Creando nuestros formularios primer formulario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, PasswordField, FileField
# Images upload config
from flask_uploads import IMAGES
from flask_wtf.file import FileRequired, FileAllowed
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, StopValidation, Length


class CustomCheck(object):
    def __init__(self, message=None):
        if not message:
            message = 'Por favor ingrese un valor numérico' 
        self.message = message

    def __call__(self, form, field):
        # print('Form data, retornado dentro de NumericCheck en {}:\n{}\n'.format(field,form.data))
        data_required = DataRequired('Campo requerido')

        def numeric_check(field):
            if field.name == 'qty':
                # print('Cantidad: {}| isdecimal(): {}'.format(field.data, field.data.isdecimal()))
                if not field.data.isdecimal():
                    raise StopValidation("Ingrese un valor numérico entero")
            
            if field.name == 'price':
                try:
                    a = float(field.data)
                    if a <= 0:
                        raise StopValidation("Ingrese un precio válido")
                except Exception as e:
                    print(e)
                    raise StopValidation("Ingrese un precio válido")

        if form.data['create_button']:
            # print('Validando desde el botón CREAR')

            numeric_check(field)

            if field.name in ('product_name','price','qty'):
                return data_required.__call__(form, field)


        elif form.data['update_button']:
            # print('Validando desde el botón ACTUALIZAR')
            if field.name == 'ref_number':
                return data_required.__call__(form, field)

            if (field.name in ('qty','price')) and (field.data != ""):
                # print('Validando el campo {}\n'.format(field.name))
                numeric_check(field)



class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField("Acceder")


class NewCashierForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, message="Debe contener al menos 8 caracteres")])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email('Email inválido')])
    submit = SubmitField("Crear cajero")


class ProductForm(FlaskForm):

    ref_number = StringField('Numero de referencia', validators=[CustomCheck()])
    product_name = StringField('Nombre del producto', validators=[CustomCheck()])
    price = StringField('Precio', validators=[CustomCheck()])
    qty = StringField('Cantidad', validators=[CustomCheck()])
    photo = FileField('Foto', validators=[FileAllowed(IMAGES, 'Anexa una imagen')])

    create_button = SubmitField('Crear producto')
    update_button = SubmitField('Actualizar producto')
    delete_button = SubmitField('Eliminar producto')


class PasswordChangeForm(FlaskForm):
    prev_pass = PasswordField('Contraseña anterior', validators=[DataRequired()])
    new_pass = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=8, message="Debe contener al menos 8 caracteres")])
    confirmPass = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    submit = SubmitField('Cambiar contraseña')
    def validate_confirmPass(form, field):
        if field.name == 'confirmPass':
            print('\nValidando confirmPass. Form Data: {}\n'.format(form.data))
            if form.data['new_pass'] != field.data:
                raise StopValidation('Error al confirmar nueva contraseña')

class RecForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField("Recuperar Contraseña")





    
    