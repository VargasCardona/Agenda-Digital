import modelos.cuenta as cuenta
import excepciones.excepciones_cuenta as excepciones
import mysql.connector as sql

def obtener_lista_cuentas():
    conexion = sql.connect(host="localhost", user="root", password="", database="agenda_digital")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cuentas")
    lista_cuentas = []
    for args in cursor.fetchall():
        id, user, password, nombre_completo, cedula = args
        lista_cuentas.append(cuenta.Cuenta(id, user, password, nombre_completo, cedula))
    return lista_cuentas

def obtener_cuenta(id: str, busqueda_cedula = False):
    tipo = "cedula" if busqueda_cedula else "usuario"
    conexion = sql.connect(host="localhost", user="root", password="", database="agenda_digital")
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM cuentas WHERE {tipo} = '{id}'")
    usuarios = cursor.fetchall()
    if len(usuarios) < 1:
        return None
    id, user, password, nombre_completo, cedula = usuarios[0]
    return cuenta.Cuenta(id, user, password, nombre_completo, cedula)

def insertar(cedula, full_name, user, password):
    if cedula == "" or full_name == "" or user == "" or password == "":
        raise excepciones.CamposVaciosException()
    if cedula.isnumeric() == False:
        raise excepciones.CedulaInvalidaException()
    if obtener_cuenta(cedula, True) != None:
        raise excepciones.CedulaEnUsoException()
    if obtener_cuenta(user) != None:
        raise excepciones.CuentaEnUsoException()

    conexion = sql.connect(host="localhost", user="root", password="", database="agenda_digital")
    cursor = conexion.cursor()

    cursor.execute(f"INSERT INTO cuentas VALUES (0, '{user}', '{password}', '{full_name}', '{cedula}')")
    conexion.commit()
