import dearpygui.dearpygui as dpg
import daos.dao_cuenta as dao_cuenta
import daos.dao_contacto as dao_contacto
import modelos.contacto as contacto

dpg.create_context()

def consultar_id():
    id_contacto = dpg.get_value("browse_id")
    try:
        contacto_consultado = dao_cuenta.consultar(id_contacto)
        dpg.set_value("contact_name", contacto_consultado.nombre())
        dpg.set_value("telephone_number", contacto_consultado.numero())
    except Exception as e:
        crear_notificacion(f"{e}")

def registrar_cuenta():
    cedula = dpg.get_value("cedula")
    full_name = dpg.get_value("full_name")   
    user_reg = dpg.get_value("user_registration")
    pass_reg = dpg.get_value("pass_registration")
    try:
        dao_cuenta.insertar(cedula, full_name, user_reg, pass_reg)
        crear_notificacion("Cuenta registrada")
        dpg.delete_item("register_window")
        dpg.configure_item("login_window", show=True)
    except Exception as e:
        crear_notificacion(f"{e}")

def registrar_contacto():
    contact = dpg.get_value("contact_name")
    telephone = dpg.get_value("telephone_number")   

    try:
        dao_cuenta.insertar(cedula, full_name, user_reg, pass_reg)
        crear_notificacion("Cuenta registrada")
        dpg.delete_item("register_window")
        dpg.configure_item("login_window", show=True)
    except Exception as e:
        crear_notificacion(f"{e}")

def cerrar_vista(item_tag):
    dpg.delete_item(item_tag)
    dpg.configure_item("login_window", show=True)

def crear_notificacion(mensaje: str):
       with dpg.window(label="Alerta", modal=True, show=True, tag="notificacion", pos=(620,300)):
           dpg.add_text(mensaje)
           dpg.add_separator()
           with dpg.group(horizontal=True):
              dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item("notificacion"))

def registro_cuenta():
    dpg.configure_item("login_window", show=False)
    with dpg.window(tag="register_window", label="Registro de cuenta", no_close=True, no_collapse=True, no_resize=True, width=281, height=250, pos=(620,300)):
      dpg.add_text("Cédula")
      dpg.add_input_text(tag="cedula", hint="Cédula", width=265)
      dpg.add_text("Nombre Completo")
      dpg.add_input_text(tag="full_name", hint="Nombre Completo", width=265)
      dpg.add_text("Nombre de Usuario")
      dpg.add_input_text(tag="user_registration", hint="Usuario", width=265)
      dpg.add_text("Contraseña")
      dpg.add_input_text(tag="pass_registration", hint="Contraseña", password=True, width=265)
      dpg.add_spacer(height=2)
      dpg.add_button(label="Registrar Cuenta", track_offset=0.5, callback=registrar_cuenta)

def iniciar_sesion():
    usuario = dpg.get_value("user")
    contrasenia = dpg.get_value("pass")
    cuenta = dao_cuenta.obtener_cuenta(usuario)

    if cuenta == None:
        crear_notificacion("Cuenta no encontrada")
        return
        
    if cuenta.contrasenia != contrasenia:
        crear_notificacion("Contraseña Incorrecta")
        return

    dpg.configure_item("login_window", show=False)
    print("si")
    with dpg.window(label=f"Agenda de {cuenta.usuario}", tag="user_view", no_close=True, no_collapse=True, no_resize=True, width=590, height=300, pos=(620,300)):
       with dpg.group(horizontal=True):
        with dpg.table(header_row=True, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True, width=300, height=200):
            dpg.add_table_column(label="Id")
            dpg.add_table_column(label="Nombre")
            dpg.add_table_column(label="Teléfono")
            
            contactos = dao_contacto.obtener_lista_contactos(cuenta.id)

            for contacto in contactos:
                with dpg.table_row():
                    dpg.add_text(f"{contacto.id}")
                    dpg.add_text(f"{contacto.nombre_completo}")
                    dpg.add_text(f"{contacto.telefono}")

        with dpg.group(horizontal=False):
          with dpg.group(horizontal=True):
              with dpg.group(horizontal=False):
                dpg.add_text("Buscar ID")
                dpg.add_input_text(tag="browse_id", hint="Ingrese un ID", width=185)
              with dpg.group(horizontal=False):
                dpg.add_spacer(height=19)
                dpg.add_button(label="Consultar", callback=cerrar_vista)
          dpg.add_text("Nombre Contacto")
          dpg.add_input_text(tag="contact_name", hint="Nombre Contacto", width=265)
          dpg.add_text("Numero Telefonico")
          dpg.add_input_text(tag="telephone_number", hint="Numero Telefonico", width=265)
          dpg.add_spacer(height=2)
          with dpg.group(horizontal=True):
           dpg.add_button(label="Registrar", callback=cerrar_vista)
           dpg.add_button(label="Editar", callback=cerrar_vista)
           dpg.add_button(label="Eliminar Contacto", callback=cerrar_vista)

       dpg.add_spacer(height=10)
       dpg.add_button(label="Cerrar Sesión", callback=lambda: (dpg.delete_item("user_view"), dpg.configure_item("login_window", show=True)))

with dpg.window(tag="login_window", label="Iniciar Sesión", no_close=True, no_collapse=True, no_resize=True, width=281, height=155, pos=(620,300)):
    dpg.add_text("Usuario")
    dpg.add_input_text(tag="user", hint="Usuario", width=265)
    dpg.add_text("Contraseña")
    dpg.add_input_text(tag="pass", hint="Contraseña", password=True, width=265)
    dpg.add_spacer(height=2)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Iniciar Sesión", track_offset=0.5, callback=iniciar_sesion, pos=(30, 125))
        dpg.add_spacer(width=7)
        dpg.add_button(label="Registrar", track_offset=0.5, callback=registro_cuenta)

dpg.create_viewport(title='Agenda Digital', width=1000, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
