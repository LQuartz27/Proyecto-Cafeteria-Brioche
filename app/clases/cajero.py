from app.clases.conexion import Conexion
from app.clases.database import Database


class Cajero:

    def __init__(self, usuario, clave, correo):
        self.usuario = usuario
        self.clave = clave
        self.correo = correo
        self.con = Conexion()
        self.db = Database(self.con)

    def registrar_venta(self, venta):
        """Registra una nueva venta en la base de datos."""
        self.db.registrar_venta_db(venta)
