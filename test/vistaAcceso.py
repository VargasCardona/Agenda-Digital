import dearpygui.dearpygui as dpg
import mysql.connector as sql

dpg.create_context()

def iniciar_sesion():
    usuario = dpg.get_value("user")
    contrasenia = dpg.get_value("pass")
    query = f"SELECT * FROM cuentas WHERE usuario = '{usuario}'"
    conexion = sql.connect(host="localhost", user="root", password="", database="agenda_digital")
    cursor = conexion.cursor()
    cursor.execute(query)
    lista = cursor.fetchone()
    if lista == None:
        print("No se encontró el usuario")
        return
    if lista[2] != contrasenia:
        print("Contraseña incorrecta")
        return
    print("si")
    print(lista)

with dpg.window(tag="Primary Window"):
    dpg.add_text("Agenda Digital")
    dpg.add_input_text(tag="user", label="Usuario", hint="Usuario")
    dpg.add_input_text(tag="pass", label="Contraseña", hint="Contraseña", password=True)
    iniciar = dpg.add_button(label="Iniciar Sesión")
    dpg.set_item_callback(iniciar, iniciar_sesion)

dpg.create_viewport(title='Agenda Digital', width=500, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
