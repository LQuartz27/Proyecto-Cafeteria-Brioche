class Database:
    """Maneja todas las peticiones a la base de datos (CRUD y más)."""
    def __init__(self, conexion):
        self.conexion = conexion

    def lista_cajeros(self):
        """Devuelve una lista de tuplas con la información de cada cajero."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "SELECT * FROM Cajeros"

        cur.execute(query)
        lista_cajeros = cur.fetchall()
        self.conexion.cerrar()

        return lista_cajeros

    def agregar_cajero_db(self, cajero):
        """Agrega un nuevo cajero a la base de datos validando que no esté ya creado."""
        lista_cajeros = self.lista_cajeros()

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "INSERT INTO Cajeros VALUES (?, ?, ?)"

        for cajeros in lista_cajeros:
            if cajero.usuario in cajeros or cajero.correo in cajeros:
                print("Error, usuario o correo ya existe en la base de datos.")
                return None

        cur.execute(query, (cajero.usuario, cajero.clave, cajero.correo))
        self.conexion.conn.commit()
        self.conexion.cerrar()

    # TODO
    def eliminar_cajero_db(self, cajero):
        pass

    def lista_productos(self):
        """Devuelve una lista de tuplas con la información de cada producto."""
        conn = self.conexion.iniciar()
        cur = conn.cursor()

        query = "SELECT * FROM Productos"

        cur.execute(query)
        lista_productos = cur.fetchall()
        self.conexion.cerrar()

        return lista_productos

    def agregar_producto_db(self, producto):
        """Agrega un nuevo producto a la base de datos validando que no esté ya creado."""
        lista_productos = self.lista_productos()

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "INSERT INTO Productos VALUES (?, ?, ?, ?, ?)"

        for product in lista_productos:
            if producto.ref in product or producto.nombre in product:
                print("Error, referencia o nombre ya existe en la base de datos.")
                return None

        cur.execute(query, (producto.ref, producto.nombre, producto.precio, producto.unidades, producto.foto))
        self.conexion.conn.commit()

        self.conexion.cerrar()

    def registrar_venta_db(self, venta):
        """Agrega una nueva venta a la base de datos."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "INSERT INTO Ventas (usuario, fecha, compra, cliente, IVA, total) VALUES (?, ?, ?, ?, ?, ?)"

        cur.execute(query, (venta.usuario, venta.fecha, venta.compra, venta.cliente, venta.IVA, venta.total))
        self.conexion.conn.commit()
        self.conexion.cerrar()

    def actualizar_producto_db(self, producto):
        """Actualiza la información de un producto en la base de datos."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "UPDATE Productos SET nombre=?, precio=?, unidades=?, foto=? WHERE referencia=?"

        cur.execute(query, (producto.nombre, producto.precio, producto.unidades, producto.foto, producto.ref))
        self.conexion.conn.commit()
        self.conexion.cerrar()

    def eliminar_producto_db(self, producto):
        """Elimina un producto de la base de datos."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "DELETE FROM Productos WHERE ref=?"

        cur.execute(query, producto.ref)
        self.conexion.conn.commit()
        self.conexion.cerrar()

    def buscar_usuario(self, username):
        """ Busca un usuario en la tabla de  """
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()
        print('\nusername pasado a database.buscar_usuario(): {}\n'.format(username))

        query = "SELECT * FROM Usuarios WHERE usuario=?"
        cur.execute(query, (username,))
        
        db_user = cur.fetchall()
        self.conexion.cerrar()

        if len(db_user) == 0:
            return None

        print('Usuario info encontrado: {}'.format(str(db_user)))

        return db_user[0]

    def listar_usuarios(self):
        """Devuelve una lista de tuplas con la información de cada usuario en la BBDD."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "SELECT * FROM Usuarios"

        cur.execute(query)
        lista_usuarios = cur.fetchall()
        self.conexion.cerrar()

        return lista_usuarios

    def agregar_usuario_db(self, new_user):
        """Agrega un nuevo cajero a la base de datos validando que no esté ya creado."""
        lista_usuarios = self.listar_usuarios()

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "INSERT INTO Usuarios VALUES (?, ?, ?, ?)"

        for usuario in lista_usuarios:
            if new_user.id in usuario or new_user.correo in usuario:
                print("Error, usuario o correo ya existe en la base de datos.")
                return None

        cur.execute(query, (new_user.id, new_user.clave, new_user.correo, new_user.tipo))
        self.conexion.conn.commit()
        self.conexion.cerrar()

    def eliminar_usuario(self, username):
        """ Elimina un usuario de la BBDD """

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = 'DELETE FROM Usuarios WHERE usuario=?'
        cur.execute(query, (username,))

        self.conexion.conn.commit()
        self.conexion.cerrar()
