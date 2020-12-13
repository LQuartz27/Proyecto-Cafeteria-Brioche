from app.clases.database import Database
from app.clases.conexion import Conexion


class Admin:
    """Clase para la gestión de los cajeros, los productos y las ventas."""
    def __init__(self, usuario, clave, correo):
        self.usuario = usuario
        self.clave = clave
        self.correo = correo
        con = Conexion()
        self.con = con
        db = Database(con)
        self.db = db

    def agregar_cajero(self, cajero):
        """Llama a la clase Database para la creación de cajeros."""
        self.db.agregar_cajero_db(cajero)

    def eliminar_cajero(self, cajero):
        """Llama a la clase Database para la eliminación de cajeros."""
        self.db.eliminar_cajero_db()

    def agregar_producto(self, producto):
        """Llama a la clase Database para la creación de productos."""
        self.db.agregar_producto_db(producto)

    def registrar_venta(self, venta):
        """Registra una nueva venta en la base de datos."""
        self.db.registrar_venta_db(venta)

    def actualizar_producto(self, producto):
        """Llama a la clase Database para actualizar la información de un producto."""
        self.db.actualizar_producto_db(producto)

    def eliminar_producto(self, producto):
        """Llama a la clase Database para eliminar un producto."""
        self.db.eliminar_producto_db(producto)