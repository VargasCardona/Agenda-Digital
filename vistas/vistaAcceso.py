import dearpygui.dearpygui as dpg
import daos.dao_cuenta as dao

dpg.create_context()

def iniciar_sesion():
    usuario = dpg.get_value("user")
    contrasenia = dpg.get_value("pass")
    cuenta = dao.obtener_cuenta(usuario)
    if cuenta == None:
        print("No se encontró el usuario")
        return
    if cuenta.contrasenia != contrasenia:
        print("Contraseña incorrecta")
        return
    print("si")

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
