from flask_login import UserMixin
from .database import Database
from .conexion import Conexion

class Usuario(UserMixin):


    def __init__(self, username, password):
        self.id = username
        self.clave = password
        self.correo = ""
        self.tipo = ""
        con = Conexion()
        self.con = con
        db = Database(con)
        self.db = db


    @staticmethod
    def query(username):
        con = Conexion()
        db = Database(con)
        user_data = db.buscar_usuario(username)
        if user_data is None:
            return None
        user = Usuario(user_data[0], user_data[1])
        user.set_correo(user_data[2])
        user.set_tipo(user_data[3])
        
        return user


    def set_correo(self, correo):
        self.correo = correo

    def set_tipo(self, tipo):
        self.tipo = tipo


    def crear_en_BBDD(self):
        """ Crea el actual usuario en la BBDD"""
        # con = Conexion()
        # db = Database(con)
        return self.db.agregar_usuario_db(self)

    def actualizar_pass_BBDD(self, new_pass):
        """ Actualiza la contraseña """
        try:
            self.db.conexion.iniciar()
            cur = self.db.conexion.conn.cursor()

            query = "UPDATE Usuarios SET clave=? WHERE usuario=?"
            cur.execute(query, (new_pass, self.id))

            self.db.conexion.conn.commit()
            self.db.conexion.cerrar()
            return True
            
        except Exception as e:
            print(e)
            return False

    def agregar_cajero(self, cajero):
        """Llama a la clase Database para la creación de cajeros."""
        if self.tipo == 'administrador':
            self.db.agregar_cajero_db(cajero)


    def eliminar_cajero(self, cajero):
        """Llama a la clase Database para la eliminación de cajeros."""
        if self.tipo == 'administrador':
            return self.db.eliminar_cajero_db()


    def agregar_producto(self, producto):
        """Llama a la clase Database para la creación de productos."""
        if self.tipo == 'administrador':
            # Si el producto fue agregado con exito, retorna True, de lo contrario False
            return self.db.agregar_producto_db(producto)
            

    def actualizar_producto(self, producto):
        """Llama a la clase Database para actualizar la información de un producto."""
        if self.tipo == 'administrador':
            return self.db.actualizar_producto_db(producto)


    def eliminar_producto(self, producto):
        """Llama a la clase Database para eliminar un producto."""
        if self.tipo == 'administrador':
            return self.db.eliminar_producto_db(producto)

    def buscar_producto(self, referencia):
        """ Busca un producto en la BBDD, retorna una tupla con los atributos en orden
            (referencia, nombre, precio, unidades, foto) """

        producto_data = self.db.buscar_producto(referencia)
        if producto_data is None:
            return None
        
        return {'referencia': producto_data[0],
                'nombre': producto_data[1],
                'precio': producto_data[2],
                'unidades': producto_data[3],
                'foto': producto_data[4]}


    def registrar_venta(self, venta):
        """Registra una nueva venta en la base de datos."""
        self.db.registrar_venta_db(venta)


