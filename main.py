from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from app import create_app
from app.forms import LoginForm, NewCashierForm, ProductForm, PasswordChangeForm

app = create_app()

# CREDENCIALES CREADAS PARA SIMULAR EL ACCESO POR EL LOGIN
fake_credentials = {
    'admin': 'admin_password',
    'cashier':'cashier_password'
}

@app.route('/', methods=['GET','POST'])
def show_main_menu():
    """ Entry point of the application. LOGIN VIEW."""
    login_form = LoginForm()

    context = {
        'login_form':login_form,
    }

    if login_form.validate_on_submit():

        print('Datos tomados del formulario:\n User: {}\n Pass: {}'.format(login_form.username.data, login_form.password.data))

        username = login_form.username.data  # Tomamos el username y pass ingresados al formulario
        password = login_form.password.data

        if username in fake_credentials:

            if password == fake_credentials[username]:
                flash('Bienvenido, {}!'.format(username))
                if username == 'admin':
                    return redirect( url_for('show_admin_menu') )

                return redirect( url_for('show_cajero_menu') )
            
            else:
                flash('Usuario y contraseña no coinciden. Vuelve a intentarlo.')

        else:
            flash('El usuario no existe')

    return render_template('inicio.html', **context)

@app.route('/logged_admin')
def show_admin_menu():
    return render_template('logged_admin.html')

@app.route('/logged_cajero')
def show_cajero_menu():
    return render_template('logged_cajero.html')

@app.route('/crear_cajero', methods=['GET','POST'])
def crear_cajero():
    new_cashier_form = NewCashierForm()
    context = {
        'new_cashier_form':new_cashier_form,
    }

    if new_cashier_form.validate_on_submit():
        username = new_cashier_form.username.data
        password = new_cashier_form.password.data 
        email = new_cashier_form.email.data 

        print('\nSe creó el cajero: {}\nPass: {}\nEmail: {}\n'.format(username,
                                                                password, email))
        flash('Se creó un nuevo cajero!')
        return redirect( url_for('crear_cajero'))

    return render_template('crear_cajero.html', **context)

@app.route('/gestionar_productos', methods=['GET','POST'])
def gestionar_productos():
    return render_template('gestionar_productos.html')

@app.route('/cambiar_clave', methods=['GET','POST'])
def cambiar_clave():
    return render_template('cambiar_password.html')

@app.route('/recuperacion_cuenta', methods=['GET','POST'])
def recuperar_cuenta():
    return render_template('recuperar_cuenta.html')

@app.route('/venta', methods=['GET','POST'])
def vender():
    return render_template('ventas.html')

@app.route('/galeria', methods=['GET','POST'])
def show_galeria():
    return render_template('galeria.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)