import mysql.connector as sql

def hacer_conexion():
    conexion = sql.connect(host="localhost", user="root", password="", database="agenda_digital")
    return conexion.cursor()
