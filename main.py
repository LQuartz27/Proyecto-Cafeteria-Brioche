from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import create_app
from app.forms import LoginForm, NewCashierForm, ProductForm, PasswordChangeForm, RecForm
from app.clases.usuario import Usuario
from app.clases.producto import Producto
from app.clases.conexion import Conexion
from app.clases.database import Database

from flask_login import login_required, current_user
import os

app = create_app()
current_file_path = os.path.abspath(os.path.dirname(__file__))
images_path = os.path.join(current_file_path, "app/uploaded_images/")


@app.route('/')
def index():
    return redirect( url_for('auth.login'))

@app.route('/logged_admin')
@login_required
def show_admin_menu():
    return render_template('logged_admin.html')


@app.route('/logged_cajero')
@login_required
def show_cajero_menu():
    return render_template('logged_cajero.html')


@app.route('/crear_cajero', methods=['GET','POST'])
@login_required
def crear_cajero():

    if current_user.tipo == 'cajero':
        return redirect( url_for('show_cajero_menu') )

    new_cashier_form = NewCashierForm()
    context = {
        'new_cashier_form':new_cashier_form,
    }

    if new_cashier_form.validate_on_submit():
        username = new_cashier_form.username.data
        password = new_cashier_form.password.data 
        email = new_cashier_form.email.data
        tipo = 'cajero'

        print('\nSe creó el cajero: {}\nPass: {}\nEmail: {}\n'.format(username,
                                                                password, email))
        
        password_hash = generate_password_hash(password)

        nuevo_cajero = Usuario(username, password_hash)
        nuevo_cajero.set_correo(email)
        nuevo_cajero.set_tipo(tipo)

        if nuevo_cajero.crear_en_BBDD():
            flash('Se creó un nuevo cajero!','success')
        else:
            flash('Error, usuario o correo ya existe en la base de datos.','danger')
                                                                        
        return redirect( url_for('crear_cajero'))

    return render_template('crear_cajero.html', isLogged=True, **context)


@app.route('/gestionar_productos', methods=['GET','POST'])
@login_required
def gestionar_productos():

    if current_user.tipo == 'cajero':
        return redirect( url_for('show_cajero_menu') )

    product_form = ProductForm()
    context = {
        'product_form' : product_form,
    }

    if product_form.validate_on_submit():
        # Tomando datos del formulario
        ref_number = product_form.ref_number.data
        product_name = product_form.product_name.data
        price = product_form.price.data
        qty = product_form.qty.data
        photo = product_form.photo.data

        print('\nRequest form dentro del main:\n{}'.format(request.form))
        filename = photo.filename

        if 'create_button' in request.form:
            # flash('PRESIONE EL BOTON CREAR', 'info')
            # Nombrando la imagen que se guardará en el servidor (el path donde sera guardada)
            if filename:
                save_filename = secure_filename(product_name+'_'+ref_number +'.'+ filename.rsplit('.',1)[1].lower())
            else:
                save_filename = 'coffee-shop.png'

            file_path = os.path.join(images_path, save_filename)

            # Creamos el objeto producto, si no existe se agrega a la BBDD, de lo contrario no y se avisa al user
            nuevo_producto = Producto(ref_number, product_name, price, qty, save_filename)
            if current_user.agregar_producto(nuevo_producto):

                print('\nProducto creado:')
                # print('Ref: {}\nName: {}\nPrice: {}\nQty: {}\nPath: {}\n'.format(ref_number,
                #                                                     product_name, price, qty, save_filename))
                if save_filename == 'coffee-shop.png':
                    pass
                else:
                    photo.save(file_path)

                flash('Producto agregado con éxtio!','success')
            else:
                flash('Error, referencia o nombre ya existe en la base de datos.','danger')

            return redirect( url_for('gestionar_productos') )
        
        elif 'update_button' in request.form:
            # flash('PRESIONE EL BOTON ACTUALIZAR', 'info')
            # Instanciamos un objeto con la informacion del formulario
            if filename:
                # Si se va a actualizar la imagen, debemos buscar la referencia a la imagen anterior
                ddbb_info = current_user.buscar_producto(ref_number)
                prior_filename = ddbb_info['foto']
                delete_path = os.path.join(images_path, prior_filename)
                # Si la imagen relacionada es la estandar para archivos sin imagen, no hay que eliminar nada
                if prior_filename == 'coffee-shop.png':
                    pass
                # Si tiene una referencia distinta a la imagen default, la eliminamos
                elif os.path.exists(delete_path):
                    os.remove(delete_path)
                else:
                    print('No se eliminó el archivo')
                    flash('No se eliminó el archivo anterior','info')
                #En caso de que al actualizar el usuario no haya pasado un nuevo product name al formulario
                # le asignamos el nombre que ya traía, para guardar la imagen
                if not product_name:
                    product_name = ddbb_info['nombre']
                save_filename = secure_filename(product_name+'_'+ref_number +'.'+ filename.rsplit('.',1)[1].lower())
                file_path = os.path.join(images_path, save_filename)
            else:
                save_filename = filename

            producto_a_actualizar = Producto(int(ref_number), product_name, price, qty, save_filename)

            if current_user.actualizar_producto(producto_a_actualizar):
                if save_filename == '':
                    pass
                else:
                    photo.save(file_path)
                flash('Producto actualizado con éxtio!','success')
            else:
                flash('Error, no existe un producto con esa referencia en la base de datos.','danger')

            return redirect( url_for('gestionar_productos') )

        elif 'delete_button' in request.form:
            # flash('PRESIONE EL BOTON ELIMINAR', 'info')
            producto_a_eliminar = Producto(int(ref_number), product_name, price, qty, filename)
            # print('\nProducto a eliminar\n{}\n'.format(producto_a_eliminar.__dict__))
            ddbb_info = current_user.buscar_producto(ref_number)
            # print(ddbb_info)

            if current_user.eliminar_producto(producto_a_eliminar):
                # Accedemos a la info de la BBDD perteneciente a ese producto, necesitamos el nombre de la imagen
                #del producto, para poder eliminarla
                save_filename = ddbb_info['foto']
                file_path = os.path.join(images_path, save_filename)

                if save_filename == 'coffee-shop.png':
                    pass
                elif os.path.exists(file_path):
                    os.remove(file_path)
                    print('\nEl producto fue eliminado de la base de datos y el archivo de la carpeta\n')
                else:
                    print("The file does not exist")
                    flash("The file does not exist",'danger')

                flash('Producto eliminado con éxito!','success')
            else:
                flash('No existe un producto con esa referencia','warning')

            # print('\nAl presionar el boton Eliminar vemos')
            # print('Info de la imagen cargada - product_form.photo.data = {}'.format(photo))
            # print('Uploaded filename ', photo.filename)
            # print(photo.filename == '')
            # print(help(photo))
            return redirect( url_for('gestionar_productos') )

    return render_template('gestionar_productos.html', isLogged=True, **context)


@app.route('/cambiar_clave', methods=['GET','POST'])
@login_required
def cambiar_clave():
    return render_template('cambiar_password.html')


@app.route('/recuperacion_cuenta', methods=['GET','POST'])
def recuperar_cuenta():
    rec_form = RecForm()
    context = {
        'rec_form':rec_form,
    }
    #(...)
    return render_template('recuperar_cuenta.html', **context)


@app.route('/venta', methods=['GET','POST'])
@login_required
def vender():
    return render_template('ventas.html')

@app.route('/galeria', methods=['GET','POST'])
@login_required
def show_galeria():
    return render_template('galeria.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)