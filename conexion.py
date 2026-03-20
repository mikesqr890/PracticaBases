import mysql.connector
from datetime import datetime

try: 
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="9696",
        database="tiendasql")
    
    if conexion.is_connected():
        print("Conexión exitosa a la tiendaMysql")

except Exception as e:
    print(f"Error al conectar a la tiendaMysql: {e}")

cursor = conexion.cursor()

# ---------------- CLIENTES ----------------
def registrar_cliente(cursor, conexion):
    nombre = input("Nombre: ")
    telefono = input("Telefono: ")
    correo = input("Correo: ")

    sql = "INSERT INTO clientes (nombreCliente, telefono, correo) VALUES (%s, %s, %s)"
    valores = (nombre, telefono, correo)

    cursor.execute(sql, valores)
    conexion.commit()

    print("Cliente registrado")


# ---------------- PRODUCTOS ----------------
def registrar_producto(cursor, conexion):
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    sql = "INSERT INTO productos (nombreProducto, precio, stock) VALUES (%s, %s, %s)"
    valores = (nombre, precio, stock)

    cursor.execute(sql, valores)
    conexion.commit()

    print("Producto registrado")


# ---------------- VENTAS ----------------
def registrar_venta(cursor, conexion):
    print("\n--- REGISTRAR VENTA ---")

    # Mostrar clientes
    cursor.execute("SELECT idCliente, nombreCliente FROM clientes")
    clientes = cursor.fetchall()

    print("\nClientes disponibles:")
    for c in clientes:
        print(f"ID: {c[0]} - Nombre: {c[1]}")

    # Mostrar productos
    cursor.execute("SELECT idProducto, nombreProducto FROM productos")
    productos = cursor.fetchall()

    print("\nProductos disponibles:")
    for p in productos:
        print(f"ID: {p[0]} - Producto: {p[1]}")

    # Pedir datos
    id_cliente = int(input("\nIngrese ID del cliente: "))
    id_producto = int(input("Ingrese ID del producto: "))
    cantidad = int(input("Cantidad: "))

    # Validar fecha
    while True:
        fecha_input = input("Fecha (YYYY-MM-DD) o ENTER para hoy: ")
        try:
            if fecha_input == "":
                fecha = datetime.today().date()
            else:
                fecha = datetime.strptime(fecha_input, "%Y-%m-%d").date()
            break
        except:
            print("Formato incorrecto. Usa YYYY-MM-DD")

    # INSERT 1: ventas (SIN idProducto)
    sql = "INSERT INTO ventas (idCliente, fecha, cantidad) VALUES (%s, %s, %s)"
    valores = (id_cliente, fecha, cantidad)

    cursor.execute(sql, valores)
    conexion.commit()

    # Obtener id de la venta creada
    id_venta = cursor.lastrowid

    # INSERT 2: ventaproducto
    sql_vp = "INSERT INTO ventaproducto (idVenta, idProducto) VALUES (%s, %s)"
    valores_vp = (id_venta, id_producto)

    cursor.execute(sql_vp, valores_vp)
    conexion.commit()

    print("Venta registrada correctamente")


# ---------------- CONSULTA ----------------
def mostrar_ventas(cursor):
    print("\n--- LISTADO DE VENTAS ---")

    cursor.execute("""
    SELECT c.nombreCliente, p.nombreProducto, v.fecha, v.cantidad
    FROM ventas v
    JOIN clientes c ON v.idCliente = c.idCliente
    JOIN ventaproducto vp ON v.idVenta = vp.idVenta
    JOIN productos p ON vp.idProducto = p.idProducto
    """)

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("No hay ventas registradas")
    else:
        print("\nCliente | Producto | Fecha | Cantidad")
        print("-" * 50)
        for fila in resultados:
            print(f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}")


# ---------------- MENÚ ----------------
while True:
    print("\n--- MENÚ ---")
    print("1. Registrar cliente")
    print("2. Registrar producto")
    print("3. Registrar venta")
    print("4. Ver ventas")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_cliente(cursor, conexion)

    elif opcion == "2":
        registrar_producto(cursor, conexion)

    elif opcion == "3":
        registrar_venta(cursor, conexion)

    elif opcion == "4":
        mostrar_ventas(cursor)

    elif opcion == "5":
        print("Saliendo...")
        break

    else:
        print("Opción inválida")

cursor.close()
conexion.close()
