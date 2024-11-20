import mysql.connector
import funciones as pr#importamos el archhivo de funciones
import conexionmysql as er #importamos el archivo conexion


er.conexion()#llamamos la funcion


productos = [#definimos que son los productos
    {"nombre": "camiseta", "precio": 10.0, "unidades": 100},
    {"nombre": "gorra", "precio": 8.0, "unidades": 50},
    {"nombre": "calcetines", "precio": 5.0, "unidades": 100},
    {"nombre": "abrigo", "precio": 80.0, "unidades": 50},
    {"nombre": "zapatillas", "precio": 60.0, "unidades": 100},
    {"nombre": "pantalones", "precio": 20.0, "unidades": 50},
    {"nombre": "sudadera", "precio": 30.0, "unidades": 75},
]

carrito = []
cliente_id = None

# Menú principal
while True:#creamos el menu 
    print(
        "A continuación, selecciona una de las opciones:\n\
         1. Crear un nuevo cliente\n\
         2. Ver clientes existentes\n\
         3. Buscar cliente\n\
         4. Realizar una compra\n\
         5. Seguimiento de una compra\n\
         6. Salir"
    )
    opcion = int(input("Elige una opción: "))
   
    if opcion == 1:
        cliente_id = pr.crear_cliente()
    elif opcion == 2:
        pr.mostrar_informacion_clientes()
    elif opcion == 3:
        pr.mostrar_cliente_por_id()
    elif opcion == 4:
        if cliente_id:
            pr.compra(productos, carrito, cliente_id)
        else:
            print("Debe registrar un cliente antes de realizar una compra.")
    elif opcion == 5:
        numero_pedido = int(input("Ingrese el número de pedido: "))
        pr.seguimiento_pedido(numero_pedido)
    elif opcion == 6:
        print("Gracias por su visita. ¡Hasta pronto!")
        break
