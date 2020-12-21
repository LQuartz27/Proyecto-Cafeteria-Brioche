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
            if producto.referencia in product or producto.nombre in product:
                print("Error, referencia o nombre ya existe en la base de datos.")
                return False

        cur.execute(query, (producto.referencia, producto.nombre, producto.precio, producto.unidades, producto.foto))
        self.conexion.conn.commit()

        self.conexion.cerrar()
        return True

    def registrar_venta_db(self, venta):
        """Agrega una nueva venta a la base de datos."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "INSERT INTO Ventas (usuario, fecha, compra, cliente, total) VALUES (?, ?, ?, ?, ?)"

        cur.execute(query, (venta.usuario, venta.fecha, venta.compra, venta.cliente, venta.total))
        self.conexion.conn.commit()
        self.conexion.cerrar()

    def actualizar_producto_db(self, producto):
        """Actualiza la información de un producto en la base de datos."""

        lista_productos = self.lista_productos()
        # Verificamos que el producto sí exista en la BBDD
        product_exists = False
        for product in lista_productos:
            if producto.referencia in product:
                product_exists = True
                break
        # Si el producto no existe será imposible actualizarlo
        if not product_exists:
            return False

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        full_change = True
        query = "UPDATE Productos SET "
        new_values = []
        for attribute, value in producto.__dict__.items():
            if attribute == 'referencia':
                continue

            if not value:
                full_change = False
            else:    
                query += '{}=?, '.format(attribute)
                new_values.append(value)

        query = query[:-2] + 'WHERE referencia=?'
        new_values.append(producto.referencia)
        query_tuple = tuple(new_values)

        if full_change:
            query = "UPDATE Productos SET nombre=?, precio=?, unidades=?, foto=? WHERE referencia=?"
            cur.execute(query, (producto.nombre, producto.precio, producto.unidades, producto.foto, producto.referencia))
        
        else:
            cur.execute(query, query_tuple)
        
        self.conexion.conn.commit()
        self.conexion.cerrar()

        return True


    def eliminar_producto_db(self, producto):
        """Elimina un producto de la base de datos."""

        lista_productos = self.lista_productos()
        # print('IMPRIMIENDO LA LISTA DE PRODUCTOS')
        # Verificamos que el producto sí exista en la BBDD
        product_exists = False
        for product in lista_productos:
            # print(product)
            if producto.referencia in product:
                product_exists = True
                break
        # Si el producto no existe será imposible eliminarlo
        if not product_exists:
            return False

        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "DELETE FROM Productos WHERE referencia=?"

        cur.execute(query, (producto.referencia,))
        self.conexion.conn.commit()
        self.conexion.cerrar()

        return True

    def buscar_producto(self, referencia):
        """ Busca un producto en la tabla de productos"""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "SELECT * FROM Productos WHERE referencia=?"
        cur.execute(query, (referencia,))
        
        db_product = cur.fetchall()
        self.conexion.cerrar()

        if len(db_product) == 0:
            return None

        # print('Usuario info encontrado: {}'.format(str(db_user)))

        return db_product[0]

    def buscar_usuario(self, username):
        """ Busca un usuario en la tabla de  """
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()
        # print('\nusername pasado a database.buscar_usuario(): {}\n'.format(username))

        query = "SELECT * FROM Usuarios WHERE usuario=?"
        cur.execute(query, (username,))
        
        db_user = cur.fetchall()
        self.conexion.cerrar()

        if len(db_user) == 0:
            return None

        # print('Usuario info encontrado: {}'.format(str(db_user)))

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
                return False

        cur.execute(query, (new_user.id, new_user.clave, new_user.correo, new_user.tipo))
        self.conexion.conn.commit()
        self.conexion.cerrar()
        return True

    def actualizar_clave_usuario_db(self, correo, clave):
        """Actualiza la clave de un usuario."""
        self.conexion.iniciar()
        cur = self.conexion.conn.cursor()

        query = "UPDATE Usuarios SET clave=? WHERE correo=?"

        cur.execute(query, (clave, correo))
        print(clave, correo)
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
