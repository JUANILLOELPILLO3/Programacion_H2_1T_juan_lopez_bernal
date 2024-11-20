import mysql.connector
def conexion():
# Configuración de la conexión a MySQL
    db = mysql.connector.connect(
        host="localhost",  # Cambiar a tu host si no es localhost
        user="root",       # Cambiar al usuario de tu base de datos
        password="curso",  # Cambiar a la contraseña de tu base de datos
        database="tienda_online"
    )

    cursor = db.cursor()