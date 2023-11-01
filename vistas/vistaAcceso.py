import dearpygui.dearpygui as dpg
import daos.dao_cuenta as dao_cuenta
import daos.dao_contacto as dao_contacto
import modelos.contacto as contacto

dpg.create_context()

def cerrar_vista():
    dpg.delete_item("user_view")
    dpg.configure_item("login_window", show=True)

def iniciar_sesion():
    usuario = dpg.get_value("user")
    contrasenia = dpg.get_value("pass")
    cuenta = dao_cuenta.obtener_cuenta(usuario)
    if cuenta == None:
        print("No se encontró el usuario")
        return
    if cuenta.contrasenia != contrasenia:
        print("Contraseña incorrecta")
        return
    
    with dpg.window(tag="user_view", no_close=True, no_collapse=True, no_resize=True, width=300, height=300):
        dpg.configure_item("login_window", show=False)
        dpg.add_text(f"Usuario: {cuenta.usuario}")

        with dpg.table(header_row=True, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True):
            dpg.add_table_column(label="Nombre")
            dpg.add_table_column(label="Teléfono")
            
            contactos = dao_contacto.obtener_lista_contactos(cuenta.id)

            for contacto in contactos:
                with dpg.table_row():
                    dpg.add_text(f"{contacto.nombre_completo}")
                    dpg.add_text(f"{contacto.telefono}")

        dpg.add_spacer(height=10)
        dpg.add_button(label="Cerrar Sesión", callback=cerrar_vista)

with dpg.window(tag="login_window", label="Iniciar Sesión", no_close=True, no_collapse=True, no_resize=True, width=280, height=155):
    dpg.add_text("Usuario")
    dpg.add_input_text(tag="user", hint="Usuario", width=265)
    dpg.add_text("Contraseña")
    dpg.add_input_text(tag="pass", hint="Contraseña", password=True, width=265)
    dpg.add_spacer(height=2)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Iniciar Sesión", track_offset=0.5, callback=iniciar_sesion, pos=(30, 125))
        dpg.add_spacer(width=7)
        dpg.add_button(label="Registrar", track_offset=0.5, callback=iniciar_sesion)

dpg.create_viewport(title='Agenda Digital', width=500, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
#dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
