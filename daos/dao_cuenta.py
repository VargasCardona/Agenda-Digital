import modelos.cuenta as cuenta
import excepciones.excepciones as excepciones
import mysql.connector as sql

def hacer_conexion():
    return sql.connect(host="localhost", user="root", password="", database="agenda_digital")

def validar_campos_vacios(funcion):
    def decorador(*args):
        for arg in args:
            if arg == "":
                raise excepciones.CamposVaciosException()
        return funcion(*args)    
    return decorador

def obtener_lista_cuentas():
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cuentas")
    lista_cuentas = []
    for args in cursor.fetchall():
        id, user, password, nombre_completo, cedula = args
        lista_cuentas.append(cuenta.Cuenta(id, user, password, nombre_completo, cedula))
    return lista_cuentas

def obtener_cuenta(id: str, busqueda_cedula = False):
    tipo = "cedula" if busqueda_cedula else "usuario"
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM cuentas WHERE {tipo} = '{id}'")
    usuarios = cursor.fetchall()
    if len(usuarios) < 1:
        raise excepciones.CuentaNoEncontradaException()
    id, user, password, nombre_completo, cedula = usuarios[0]
    return cuenta.Cuenta(id, user, password, nombre_completo, cedula)

@validar_campos_vacios
def iniciar_sesion(usuario: str, contrasena: str):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM cuentas WHERE usuario = '{usuario}'")
    usuarios = cursor.fetchall()
    if len(usuarios) < 1:
        raise excepciones.CuentaNoEncontradaException()
    id, user, password, nombre_completo, cedula = usuarios[0]
    if contrasena != password:
        raise excepciones.ContrasenaIncorrectaException()
    return cuenta.Cuenta(id, user, password, nombre_completo, cedula)

@validar_campos_vacios
def insertar(cedula, full_name, user, password):
    if cedula.isnumeric() == False:
        raise excepciones.CedulaInvalidaException()
    try:
        obtener_cuenta(cedula, True)
        raise excepciones.CedulaEnUsoException()
    except excepciones.CuentaNoEncontradaException as e:
        pass
    try:
        obtener_cuenta(user)
        raise excepciones.CuentaEnUsoException()
    except excepciones.CuentaNoEncontradaException as e:
        pass 

    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"INSERT INTO cuentas VALUES (0, '{user}', '{password}', '{full_name}', '{cedula}')")
    conexion.commit()
