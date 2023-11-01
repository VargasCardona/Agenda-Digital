import modelos.cuenta as cuenta
import mysql.connector as sql

def hacer_conexion():
    return sql.connect(host="localhost", user="root", password="", database="agenda_digital")

def obtener_lista_cuentas():
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cuentas")
    lista_cuentas = []
    for args in cursor.fetchall():
        id, user, password, nombre_completo, cedula = args
        lista_cuentas.append(cuenta.Cuenta(id, user, password, nombre_completo, cedula))
    return lista_cuentas

def obtener_cuenta(usuario: str):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM cuentas WHERE usuario = '{usuario}'")
    id, user, password, nombre_completo, cedula = cursor.fetchone()
    return cuenta.Cuenta(id, user, password, nombre_completo, cedula)
