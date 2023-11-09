import modelos.contacto as contacto
import excepciones.excepciones as excepciones
import mysql.connector as sql
import random

def hacer_conexion():
    return sql.connect(host="localhost", user="root", password="", database="agenda_digital")

def crear_identificador():
    retorno = random.randint(100, 999)
    try:
        consultar_general(str(retorno))
        return crear_identificador()
    except Exception as e:
        return retorno

def validar_campos_vacios(funcion):
    def decorador(*args):
        for arg in args:
            if arg == "":
                raise excepciones.CamposVaciosException()
        return funcion(*args)    
    return decorador

def obtener_lista_contactos(id_cuenta_activa):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM contactos as c WHERE id_cuenta = '{id_cuenta_activa}'")
    lista_contactos = []
    for args in cursor.fetchall():
        id, nombre_completo, telefono, id_cuenta = args
        lista_contactos.append(contacto.Contacto(id, nombre_completo, telefono, id_cuenta))
    return lista_contactos

@validar_campos_vacios
def consultar(id: str, id_cuenta_activa: str):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM contactos WHERE id = {id} AND id_cuenta = {id_cuenta_activa}")
    contactos = cursor.fetchall()
    if len(contactos) < 1:
        raise excepciones.ContactoNoEncontradoException()
    id, nombre_completo, telefono, id_cuenta = contactos[0]
    return contacto.Contacto(id, nombre_completo, telefono, id_cuenta)

def consultar_general(id: str):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM contactos WHERE id = {id}")
    contactos = cursor.fetchall()
    if len(contactos) < 1:
        raise excepciones.ContactoNoEncontradoException()
    id, nombre_completo, telefono, id_cuenta = contactos[0]
    return contacto.Contacto(id, nombre_completo, telefono, id_cuenta)

@validar_campos_vacios
def insertar(nombre_completo: str, telefono: str, id_cuenta: str):
    if telefono.isnumeric() == False:
        raise excepciones.TelefonoInvalidoException()
    id = crear_identificador()
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
INSERT INTO contactos VALUES ({id}, '{nombre_completo}', {telefono}, {id_cuenta})
    '''
    cursor.execute(query)
    conexion.commit()

@validar_campos_vacios
def actualizar(nombre_completo: str, telefono: str, id: str, id_cuenta: str):
    if telefono.isnumeric() == False:
        raise excepciones.TelefonoInvalidoException()
    consultar(id, id_cuenta)
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
UPDATE contactos SET nombre = '{nombre_completo}', telefono = {telefono} WHERE id = {id}
    '''
    cursor.execute(query)
    conexion.commit()

@validar_campos_vacios
def eliminar(id: str, id_cuenta: str):
    consultar(id, id_cuenta)
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
DELETE FROM contactos WHERE id = '{id}'
    '''
    cursor.execute(query)
    conexion.commit()
