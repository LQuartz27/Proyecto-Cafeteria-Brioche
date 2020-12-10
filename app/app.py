from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('inicio.html')

@app.route('/cambiarClave', methods=['GET', 'POST'])
def clave():
    return render_template('cambiar_password.html')

@app.route('/recuperarCuenta', methods=['GET', 'POST'])
def recuperar():
    return render_template('recuperar_cuenta.html')

@app.route('/crearCajero', methods=['GET', 'POST'])
def crearcajero():
    return render_template('crear_cajero.html')

@app.route('/admin')
def admin():
    return render_template('logged_admin.html')

@app.route('/cajero')
def cajero():
    return render_template('logged_cajero.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/productos')
def productos():
    return render_template('gestionar_productos.html')