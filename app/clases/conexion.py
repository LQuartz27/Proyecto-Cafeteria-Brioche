import sqlite3
from sqlite3 import Error


class Conexion:
    """
    Se encarga de abrir y cerrar la conexión con la base de datos.
    Tiene como argumento opcional apuntar a otra base de datos.
    """
    def __init__(self, data_base="C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\database\\database.db"):
        self.db = data_base
        self.conn = None

    def iniciar(self):
        """Inicia la conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db)
            return self.conn
        except Error:
            print("Error al conectar con la base de datos.")

    def cerrar(self):
        """Cierra la conexión con la base de datos."""
        if self.conn is not None:
            self.conn.close()
