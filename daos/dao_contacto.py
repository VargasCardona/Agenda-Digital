import modelos.contacto as contacto
import excepciones.excepciones as excepciones
import mysql.connector as sql

def hacer_conexion():
    return sql.connect(host="localhost", user="root", password="", database="agenda_digital")

def obtener_lista_contactos(id_cuenta_activa):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM contactos as c WHERE id_cuenta = '{id_cuenta_activa}'")
    lista_contactos = []
    for args in cursor.fetchall():
        id, nombre_completo, telefono, id_cuenta = args
        lista_contactos.append(contacto.Contacto(id, nombre_completo, telefono, id_cuenta))
    return lista_contactos

def consultar(id: str, id_cuenta_activa: str):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM contactos WHERE id = {id} AND id_cuenta = {id_cuenta_activa}")
    contactos = cursor.fetchall()
    if len(contactos) < 1:
        raise excepciones.ContactoNoEncontradoException()
    id, nombre_completo, telefono, id_cuenta = contactos[0]
    return contacto.Contacto(id, nombre_completo, telefono, id_cuenta)

def insertar(nombre_completo: str, telefono: str, id_cuenta: str):
    if nombre_completo == "" or telefono == "":
        raise excepciones.CamposVaciosException()
    if telefono.isnumeric() == False:
        raise excepciones.TelefonoInvalidoException()
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
INSERT INTO contactos VALUES (0, '{nombre_completo}', {telefono}, {id_cuenta})
    '''
    cursor.execute(query)
    conexion.commit()

def actualizar(nombre_completo: str, telefono: str, id: str, id_cuenta: str):
    if nombre_completo == "" or telefono == "" or id == "":
        raise excepciones.CamposVaciosException()
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

def eliminar(id: str, id_cuenta: str):
    if id == "":
        raise excepciones.CamposVaciosException()
    consultar(id, id_cuenta)
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
DELETE FROM contactos WHERE id = '{id}'
    '''
    cursor.execute(query)
    conexion.commit()
