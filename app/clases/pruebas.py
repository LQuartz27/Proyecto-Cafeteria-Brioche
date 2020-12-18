from app.clases.cajero import Cajero
from app.clases.administrador import Admin
from app.clases.producto import Producto
from app.clases.venta import Venta

# Creación de cajeros.
cajero1 = Cajero("cajero1", 123456, "cajero1@correo.com")
cajero2 = Cajero("cajero2", 888888, "cajero2@correo.com")
cajero3 = Cajero("cajero3", 565656, "cajero3@correo.com")
cajero4 = Cajero("cajero4", 100123, "cajero4@correo.com")

# Creación de administrador y se agregar los cajeros a la base de datos
admin = Admin("admin", "password_admin", "admin@correo.com")
admin.agregar_cajero(cajero1)
admin.agregar_cajero(cajero2)
admin.agregar_cajero(cajero3)
admin.agregar_cajero(cajero4)

# Creación de productos.
p1 = Producto(1, "dona", 5_000, 15, "C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\static\\images\\dona.png")
p2 = Producto(2, "late", 2_500, 10, "C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\static\\images\\late.png")
p3 = Producto(3, "brownie", 5_000, 10, "C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\static\\images\\brownie.png")

# Se agregan los productos a la base de datos.
admin.agregar_producto(p1)
admin.agregar_producto(p2)
admin.agregar_producto(p3)

# Creación de compras.
compra1 = [[2, 1, "dona", 5_000], [1, 2, "late", 2_500]]
compra2 = [[1, 2, "late", 2_500], [3, 10, "brownie", 5_000]]
compra3 = [[5, 2, "late", 2_500], [3, 1, "dona", 5_000]]

# Creación de ventas.
venta1 = Venta("admin", "10/12/2020", str(compra1), "cliente1", 12_500)
venta2 = Venta("admin", "10/12/2020", str(compra2), "cliente2", 17_500)
venta3 = Venta("admin", "10/12/2020s", str(compra3), "cliente3",  27_500)

# Registro de ventas creadas en la base de datos.
admin.registrar_venta(venta1)
admin.registrar_venta(venta2)

# Creación de producto ya existente para actualizar su precio.
p4 = Producto(2, "late", 3_500, 10, "C:\\Uni Norte\\Retos\\Proyecto-Cafeteria-Brioche\\app\\static\\images\\late.png")
admin.actualizar_producto(p4)

# Venta registrada por cajero.
cajero2.registrar_venta(venta3)
