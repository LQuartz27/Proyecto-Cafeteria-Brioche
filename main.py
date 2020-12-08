from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from app import create_app


app = create_app()

@app.route('/')
def show_main_menu():
    return render_template('inicio.html')

@app.route('/logged_admin')
def show_admin_menu():
    return render_template('logged_admin.html')

@app.route('/logged_cajero')
def show_cajero_menu():
    return render_template('logged_cajero.html')

@app.route('/crear_cajero')
def crear_cajero():
    return render_template('crear_cajero.html')

@app.route('/gestionar_productos')
def gestionar_productos():
    return render_template('gestionar_productos.html')

@app.route('/cambiar_clave')
def cambiar_clave():
    return render_template('cambiar_password.html')

@app.route('/recuperacion_cuenta')
def recuperar_cuenta():
    return render_template('recuperar_cuenta.html')

@app.route('/venta')
def vender():
    return render_template('ventas.html')

@app.route('/galeria')
def show_galeria():
    return render_template('galeria.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)