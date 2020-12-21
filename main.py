from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import create_app
from app.forms import LoginForm, NewCashierForm, ProductForm, PasswordChangeForm, RecForm
from app.clases.usuario import Usuario
from app.clases.producto import Producto
from app.clases.conexion import Conexion
from app.clases.database import Database

from flask_login import login_required, current_user
import os
import sqlite3 #Temporal


app = create_app()
current_file_path = os.path.abspath(os.path.dirname(__file__))
images_path = os.path.join(current_file_path, "app/static/uploads/")


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
    
    current_user.db.conexion.iniciar()
    cur = current_user.db.conexion.conn.cursor()
    cur.execute('SELECT referencia, nombre, precio, unidades, foto FROM Productos')
    itemData = cur.fetchall()
    current_user.db.conexion.cerrar()
    itemData = parse(itemData)
    
    context = {
        'product_form' : product_form,
        'itemData': itemData
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
                save_filename = secure_filename(product_name +'.'+ filename.rsplit('.',1)[1].lower())
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
                save_filename = secure_filename(ref_number +'.'+ filename.rsplit('.',1)[1].lower())
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

    pass_change_form = PasswordChangeForm()
    context = {
        'pass_change_form':pass_change_form,
    }
    print('Validate on submit: {}'.format(pass_change_form.validate_on_submit()))
    if pass_change_form.validate_on_submit():
        prev_pass = pass_change_form.prev_pass.data
        new_pass = pass_change_form.new_pass.data
        confirm_pass = pass_change_form.confirmPass.data
        print('Ingresados al formulario')
        print(prev_pass)
        print(new_pass)
        print(confirm_pass)

        # Si la contraseña previa es válida, procedemos a hacer el cambio en BBDD
        if check_password_hash(current_user.clave, prev_pass):
            # En BBDD guardamos únicamente la versión hasheada de la contraseña
            password_hash = generate_password_hash(new_pass)
            print('New hashpass', password_hash)
            # Si se logra hacer la actualización con éxito en la BBDD se le avisa al usuario
            if current_user.actualizar_pass_BBDD(password_hash):
                flash('Contraseña actualizada con éxito','success')
            # Si no se logra actualizar en BBDD también se avisa al usuario
            else:
                flash('Error al actualizar la contraseña en la base de datos')
            
            return redirect( url_for('cambiar_clave'))
        else:
            flash('Contraseña actual inválida','danger')
    
    return render_template('cambiar_password.html', **context)


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
    return render_template('venta.html')

@app.route('/galeria', methods=['GET','POST'])
@login_required
def show_galeria():
    return render_template('galeria.html')



@app.route('/ventas', methods=['GET','POST'])
@login_required
def show_ventas():	
    
    current_user.db.conexion.iniciar()
    cur = current_user.db.conexion.conn.cursor()
    cur.execute('SELECT referencia, nombre, precio, unidades, foto FROM Productos')
    itemData = cur.fetchall()
    current_user.db.conexion.cerrar()
    itemData = parse(itemData)
    
    """
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT referencia, nombre, precio, unidades, foto FROM Productos')
        itemData = cur.fetchall()
    conn.close()
    print("antes del parse")
    print(itemData)
    itemData = parse(itemData)
    print("after parse")
    print(itemData)
    """
    return render_template('ventas.html', itemData=itemData, isLogged=True)

@login_required
def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False


@app.route('/agregar', methods=['POST'])
@login_required
def agregar_prod():
	
    if request.method =='POST':
        cant = int(request.form['cant'])
        referencia = int(request.form['referencia'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        stock = int(request.form['stock'])
        foto = request.form['foto']
        totalp = 0
        totalp = cant * precio
        
        aProd = { 
            str(referencia) : {
                'nombre' : nombre,
                'referencia' : referencia,
                'cantidad' : cant,
                'precio' : precio,
                'stock' : stock,
                'foto' : foto,
                'pTotal': totalp
            }
        }
        
        cant_prod_total = 0
        precio_prod_total = 0
        session.modified = True
        
        if 'lst_compra' in session:
            #--Ya Existe el carrito
            if str(referencia) in session['lst_compra']:
                #--Ya Existe la referencia en el carrito
                for key, value in session['lst_compra'].items():
                    if str(referencia) == key:
                        cant_ant = session['lst_compra'][key]['cantidad']
                        total_cant = cant_ant + cant
                        session['lst_compra'][key]['cantidad'] = total_cant
                        session['lst_compra'][key]['pTotal'] = total_cant * precio
            else:
                #--No Existe la referencia en el carrito
                session['lst_compra'] = array_merge(session['lst_compra'], aProd) #agregado
            
            for key, value in session['lst_compra'].items():
                cant_ref = session['lst_compra'][key]['cantidad']
                pTotal_ref = session['lst_compra'][key]['pTotal']
                cant_prod_total += cant_ref
                precio_prod_total += pTotal_ref
            
        else:
            #--No Existe el carrito
            session['lst_compra'] = aProd
            cant_prod_total += cant
            precio_prod_total += cant * precio
            
        session['cant_prod_total'] = cant_prod_total
        session['precio_prod_total'] = precio_prod_total 
        
        """
        flash("--cantidades--")
        flash(session['cant_prod_total'])
        flash("--precio total--")
        flash(session['precio_prod_total'])
        flash("--lista--")
        flash(session['lst_compra'])
        """
    return redirect(url_for('show_ventas'))


@app.route('/borrar/<string:ref>')
@login_required
def borrar_producto(ref):
    try:
        cant_prod_total = 0
        precio_prod_total = 0
        session.modified = True
		
        for item in session['lst_compra'].items():
            if item[0] == ref:				
                session['lst_compra'].pop(item[0], None)
                if 'lst_compra' in session:
                    for key, value in session['lst_compra'].items():
                        cant_ref = session['lst_compra'][key]['cantidad']
                        pTotal_ref = session['lst_compra'][key]['pTotal']
                        precio_prod_total += pTotal_ref
                        cant_prod_total += cant_ref
                break
		
        if precio_prod_total == 0:
            borrar_venta()
        else:
            session['precio_prod_total'] = precio_prod_total
            session['cant_prod_total'] = cant_prod_total
		
        return redirect(url_for('show_ventas'))
    except Exception as e:
        print(e)

@app.route('/reg_venta')
@login_required
def reg_venta():
    nFac = 0
    #--Registra en BD (Ventas) los datos generales guardados en la sesión y genera un número de factura
    print("///////////////////////////DICT////////////////////")
    print(session.__dict__)
    print("///////////////////////////LST_COMPRA////////////////////")
    print(session['lst_compra'])
    print("//////////////////////cantidad total/////////////////////////")
    print(session['cant_prod_total'])
    print("///////////////////////////precio total////////////////////")
    print(session['precio_prod_total'])
    
    
    try:
        current_user.db.conexion.iniciar()
        cur = current_user.db.conexion.conn.cursor()
        cur.execute("INSERT INTO Ventas (usuario, fecha, cliente, cantidades, total) VALUES (?, julianday('now'), ?, ?, ?)",(current_user.id, "pedro perez", session['cant_prod_total'], session['precio_prod_total']))
        current_user.db.conexion.conn.commit()
        nFac = cur.lastrowid
        current_user.db.conexion.cerrar()   
    except Exception as e:
        print(e)
    """ 
    
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Ventas (usuario, fecha, cliente, cantidades, total) VALUES (?, julianday('now'), ?, ?, ?)",("Current_user.id", "pedro perez", session['cant_prod_total'], session['precio_prod_total']))
        nFac = cur.lastrowid
    conn.close()
    """
    print("EL NUMERO DE FACTURA ES: " + str(nFac))
    
    #--Registra en BD (Detalle) el detalle de cada referencia vendida guardados en la sesión.
    for key, value in session['lst_compra'].items():
        ref = session['lst_compra'][key]['referencia']
        nombre = session['lst_compra'][key]['nombre']
        precio = session['lst_compra'][key]['precio']
        cant = session['lst_compra'][key]['cantidad']
        pTotal = session['lst_compra'][key]['pTotal']
        
        current_user.db.conexion.iniciar()
        cur = current_user.db.conexion.conn.cursor()
        cur.execute("INSERT INTO Detalle (factura, referencia, nombre, precio, cantidad, total) VALUES (?, ?, ?, ?, ?, ?)",(nFac, ref, nombre, precio, cant, pTotal))
        current_user.db.conexion.conn.commit()
        current_user.db.conexion.cerrar()

        """
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor() 
            cur.execute("INSERT INTO Detalle (factura, referencia, nombre, precio, cantidad, total) VALUES (?, ?, ?, ?, ?, ?)",(nFac, ref, nombre, precio, cant, pTotal))
        conn.close()
        """
    borrar_lst_compra()
    return redirect(url_for('gen_factura', nFac=nFac))
    
@login_required
def borrar_lst_compra():
    session.pop('lst_compra', None)
    session.pop('cant_prod_total', None)
    session.pop('precio_prod_total', None)


@app.route('/vaciar')   #temporal, modificar
@login_required
def vaciar():
    borrar_lst_compra()
    return redirect(url_for('show_ventas'))

@app.route("/factura/<nFac>")
@login_required
def gen_factura(nFac):
    #--Recupera datos de BD(Ventas) con el numero de factura dado.
    current_user.db.conexion.iniciar()
    cur = current_user.db.conexion.conn.cursor()
    cur.execute("SELECT usuario, cliente, date(fecha), time(fecha), cantidades, total FROM Ventas WHERE numero=?",[nFac])
    factData = cur.fetchone()       
    current_user.db.conexion.cerrar()
    
    """
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT usuario, cliente, date(fecha), time(fecha), cantidades, total FROM Ventas WHERE numero=?",[nFac])
        factData = cur.fetchone()
    conn.close()
    
    #usuario 0, cliente 1, date(fecha) 2, time(fecha) 3, cantidades 4, total 5
    print("/////////////////////////////////////////////////////////")
    print("LA FACTURA ES: " + str(nFac) +" - Fecha: " + factData[2] +" - Hora: "+ factData[3])
    print("/////////////////////////////////////////////////////////")
    print("DATOS GENERALES - lista")
    print(factData)
    print("/////////////////////////////////////////////////////////")
    """
    #--Recupera detalle de factura de BD(Ventas) con el numero de factura dado.
    current_user.db.conexion.iniciar()
    cur = current_user.db.conexion.conn.cursor()
    cur.execute("SELECT referencia, nombre, precio, cantidad, total FROM Detalle WHERE factura=?",[nFac])
    factDetail = cur.fetchall()       
    current_user.db.conexion.cerrar()

    """
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT referencia, nombre, precio, cantidad, total FROM Detalle WHERE factura=?",[nFac])
        factDetail = cur.fetchall()
    conn.close()
    
    #referencia 0, nombre 1, precio 2, cantidad 3, total 4
    print("/////////////////////////////////////////////////////////")
    print("detalle de factura")
    print(factDetail)
    print("/////////////////////////////////////////////////////////")
    """
    return render_template('factura.html',  nFact=nFac, factData=factData, factDetail=factDetail)



if __name__ == "__main__":
    #app.run(port=5000, debug=True)
    app.run(host='127.0.0.1', port=443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))