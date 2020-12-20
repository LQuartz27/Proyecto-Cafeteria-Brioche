""" This auth package is a flask Blueprint, a modular 'mini' app which includes the functionalities for
    users login, logout and users creation. This routes.py module is the one containing said functions and
    routes. """

from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from . import auth
from app.forms import LoginForm, NewCashierForm
from app.clases.usuario import Usuario


# CREDENCIALES CREADAS PARA SIMULAR EL ACCESO POR EL LOGIN
fake_credentials = {
    'admin': 'admin_pass',
    'cajero1':'cajero_pass'
}

# AL SER UN BLUEPRINT, CAMBIA EL @app por @[blueprint name], por eso ahora es @auth
@auth.route('/login', methods=['GET','POST'])
def login(): #ANTES ERA  show_main_menu()
    """ Entry point of the application. LOGIN VIEW."""
    if current_user.is_authenticated:
        if current_user.tipo == 'administrador':
            return redirect( url_for('show_admin_menu') )
        return redirect( url_for('show_cajero_menu') )


    login_form = LoginForm()

    context = {
        'login_form':login_form,
    }

    if login_form.validate_on_submit():

        # print('Datos tomados del formulario:\n User: {}\n Pass: {}'.format(login_form.username.data, login_form.password.data))

        username = login_form.username.data  # Tomamos el username y pass ingresados al formulario
        password = login_form.password.data

        if not Usuario.query(username) is None:
            user_db = Usuario.query(username)

            if check_password_hash(user_db.clave, password):
            # if fake_credentials[username] == password:

                login_user(user_db)

                # flash('Bienvenido, {}!'.format(username))
                if user_db.tipo == 'administrador':
                    return redirect( url_for('show_admin_menu') )

                return redirect( url_for('show_cajero_menu') )
            
            else:
                flash('Usuario y contraseña no coinciden. Vuelve a intentarlo.','warning')

        else:
            flash('El usuario no existe','danger')

    return render_template('inicio.html', **context)

@auth.route('/logout')
@login_required
def logout():
    """ Logs the current user out. """
    out_user = current_user.id
    logout_user()
    flash('Buen día. Regresa pronto {}!'.format(out_user),'info')
    return redirect(url_for('auth.login'))