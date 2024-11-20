import mysql.connector
import random

# Configuración de la conexión a MySQL
db = mysql.connector.connect(
    host="localhost",  # Cambiar a tu host si no es localhost
    user="root",       # Cambiar al usuario de tu base de datos
    password="curso",  # Cambiar a la contraseña de tu base de datos
    database="tienda_online"
)

cursor = db.cursor()

def crear_cliente():#con esta funcion vamos a agregar un cliente a nuestra base de datos 
    nombre = input("Ingrese el nombre del cliente: ")#pedimos que introduzca el nombre
    email = input("Ingrese el correo electrónico del cliente: ")#pedimos que introduzca el email
    telefono = input("Ingrese el número de teléfono del cliente: ")#pedimos que introduzca el numeir de telefono 
    cursor.execute(#con curso.excute lo que hacemos es acceder a la base de datos y ejecutar un select un inser into etc.. dependiendo con que lo llamemos
        "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",#en este caso hemos ejecutado un inser into para agregar tanto nombre,como email, como telefono                                                                   
        (nombre, email, telefono)#en todo el codigo que tiene que ver con mysql vemos %s esto nos indica la cantidad de columnas que tiene la tabla en este caso tres ponemos 3
    )
    db.commit()  # confirmar los cambios en la base de datos
    cliente_id = cursor.lastrowid  #curso.lastrowid es un atributo que tiene pyton que nos permite obtener el id del cliente en funcion de la fila en el que esta es decir si es primera fila sera 1

    print(f"Cliente registrado exitosamente con ID: {cliente_id}")#imprimos el id y el siguiente mensaeje
    return cliente_id  # devuelve el id del cliente registrado el cual no servira para trabajar mas tarde con el 

def mostrar_cliente_por_id():#mostraremos un cliente en funcion del id con el que se a registrado
    id_buscar = int(input("ingrese el ID del cliente que deseas buscar: "))#le pedimos el id del cliente en este caso con int delante porque se trata de un numero
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_buscar,))#este hace exactamente lo mismo que el de arriba pero en vez de un inser into un selct porque se lo hemos indicado 
    cliente = cursor.fetchone()#siempre se ponde detras del select para recoger los datos de la fila que estamos indicando 
    if cliente:#si el id que hemos metido pertenece a algun cliente mostraremos 
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}, Teléfono: {cliente[3]}")#imprimir id , nombre , telefono y email
    else:
        print("No se encontró un cliente con ese ID.")#si el id que ponemos no tiene asignado ningun cliente mostraremos esto 


def compra(productos, carrito, cliente_id):#la funcion de la compra en este caso metemos productos carrito y cliente dentro porque queremos indicar que se a comprado un producto,que se a actualizado el carrito y que se le guarda 
                                        #la compra al cliente en  su id 
    while True:#abrimos un bucle while el cual el cliente recorrera
        print('elige el numero de la opcion que deses realizar')
        opcion = input('¿quieres agregar un producto al carrito?\n\
                       1.si:\n\
                       2.no:\n\
                       3.ver Carrito:\n\
                       4.Finalizar Compra: ')#le mostramos un menu con 4 opciones en funcion de la que elija se mostrara una cosa o otra 
        if opcion == '1':#si elije 1
            print('Productos disponibles:')
            for i, producto in enumerate(productos, start=1):
                print(f"{i}.nombre {producto['nombre']} - precio: ${producto['precio']} - unidades: {producto['unidades']}")#con esto generamos un contador en el que la i es el numero 1 y se mostrara el diccionario de productos 
            try:#usamos un try para poder manipular posibles errores 
                seleccion = int(input('Seleccione el número de producto que desea comprar: ')) - 1#le pedimos que seleccione un numero el cual le restaremos uno porque nuestra lista inicia en o 
                if 0 <= seleccion < len(productos):#nos aseguramos que lo que se muestra existe 
                    cantidad = int(input(f"¿Cuántas unidades de {productos[seleccion]['nombre']} desea comprar? "))#y le preguntamos cuantas unidades quiere comprar
                    if cantidad > 0 and cantidad <= productos[seleccion]['unidades']:#si la cantidad establecida es corecta 
                        agregar_producto_al_carrito(carrito, productos[seleccion], cantidad)#mostramos la funcion agregar producto
                    else:
                        print("cantidad no válida no disponemos de tantas unidades")#si no se dispone de tantas unidades saltara este error para que la reduzca
                else:
                    print("Selección no válida. Por favor, elija un producto de la lista.")#si pide algo que no esta en lista
            except (ValueError, IndexError):
                print("Entrada no válida. Por favor, intente de nuevo.")# si elije una opcion del menu que no esta en el menu 
        elif opcion == '3':#si la opcion es 3 mostramos la siguiente funcion
            ver_carrito(carrito)
        elif opcion == '4':
            realizar_compra(cliente_id, carrito)
            carrito.clear()  # limpia el carrito después de finalizar la compra
            break
        elif opcion == '2':
            print("Operación finalizada.")
            break
        else:
            print("Opción no válida.")

def realizar_compra(cliente_id, carrito):
    if not carrito:#si no hay nada en el carrito 
        print("el carrito está vacío.")
        return

    total = sum(p['precio'] * c for p, c in carrito)#el total es el precio del producto por la cantidad de unidades que haya en el carrito
    productos = "; ".join([f"{p['nombre']} x{c}" for p, c in carrito])#los productos que haya en el carrito

    # Insertar pedido en la base de datos
    cursor.execute(#usamos la misma funcion para realizar un inser into en nuestra base de datos
        "INSERT INTO pedidos (id_cliente, productos, total) VALUES (%s, %s, %s)",
        (cliente_id, productos, total)
    )
    db.commit()#guardamos lo realizado

    pedido_id = cursor.lastrowid#creamos un id del pedido
    print(f"Compra registrada exitosamente con el número de pedido: {pedido_id}")#mostramos el id creado

# Función para seguir un pedido desde MySQL
def seguimiento_pedido(numero_pedido):
    cursor.execute("SELECT * FROM pedidos WHERE id_pedido = %s", (numero_pedido,))
    pedido = cursor.fetchone()
    if not pedido:
        print(f"No se encontró un pedido con el número {numero_pedido}.")
    else:
        print(f"Detalles del pedido {numero_pedido}:")#mostramos los detalles 
        print(f"ID Cliente: {pedido[1]}")
        print(f"Productos: {pedido[2]}")
        print(f"Total: {pedido[3]}")



# Función para agregar un producto al carrito
def agregar_producto_al_carrito(carrito, producto, cantidad):
    if cantidad <= producto["unidades"]:#comprobar si la cantidad deseada es menor o igual al numero de unidades del inventario 
        carrito.append((producto, cantidad))#el carrito es donde se encuentran las cosas y el append para agregar un nuevo elemento a la fila 
        producto["unidades"] -= cantidad#una vez realizada la compra que baje el numero de unidades del inventario 
    else:
        print(f"no hay suficientes unidades de {producto['nombre']}.")#muestra que no se dispone de tantas unidades 

# Función para mostrar el carrito
def ver_carrito(carrito):
    total = 0#hacemos una variable
    print('Productos en el carrito:')
    for producto, cantidad in carrito:#cuando el producto se encuentre en el carrito 
        print(f"Nombre: {producto['nombre']}, Precio: ${producto['precio']}, Cantidad: {cantidad}")#mostraremos el nombre,el precio, y la cantidad 
        total += producto["precio"] * cantidad#aqui decimos que el precio final va a ser = al precio del producto x la cantidad que el cliente haya seleccionado 
    print(f"Total: ${total}")#imprimimos el total
    return total#devuelve el precio total el cual nos servira para trabjar mas tarde 

def mostrar_informacion_clientes():
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    if not resultados:
        print("No hay clientes registrados.")
    else:
        print("Clientes registrados:")
        for cliente in resultados:
            print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Email: {cliente[2]}, Teléfono: {cliente[3]}")
