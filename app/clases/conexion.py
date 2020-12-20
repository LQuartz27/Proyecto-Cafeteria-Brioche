import sqlite3
from sqlite3 import Error
import os


class Conexion:
    """
    Se encarga de abrir y cerrar la conexión con la base de datos.
    Tiene como argumento opcional apuntar a otra base de datos.
    """
    current_file_path = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(current_file_path, "../database/database.db")

    # def __init__(self, data_base="C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\database\\database.db"):
    def __init__(self, data_base=db_path):
        self.db = data_base
        self.conn = None

    def iniciar(self):
        """Inicia la conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db)
            # print("\nConexion exitosa\n")
            return self.conn
        except Error:
            print("\nError al conectar con la base de datos.\n")

    def cerrar(self):
        """Cierra la conexión con la base de datos."""
        if self.conn is not None:
            self.conn.close()
            # print("Conexion cerrada")

if __name__ == '__main__':
    con = Conexion()
    con.iniciar()
    con.cerrar()
