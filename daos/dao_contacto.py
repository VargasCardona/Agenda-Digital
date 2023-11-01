import modelos.contacto as contacto
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

def insertar(contacto: contacto.Contacto):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
    INSERT INTO contactos VALUES (0, {contacto.nombre_completo}, {contacto.telefono}, {contacto.id_cuenta})
    '''
    cursor.execute(query)

def actualizar(contacto: contacto.Contacto):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
    UPDATE contactos SET nombre = '{contacto.nombre_completo}', telefono = '{contacto.telefono}' WHERE id = {contacto.id}
    '''
    cursor.execute(query)

def eliminar(id):
    conexion = hacer_conexion()
    cursor = conexion.cursor()
    query = f'''
    DELETE FROM contactos WHERE id = {id}
    '''
    cursor.execute(query)

