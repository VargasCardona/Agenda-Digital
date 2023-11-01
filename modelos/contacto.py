import modelos.persona as persona

class Contacto(persona.Persona):
    def __init__(self, id: int, nombre_completo: str, telefono: int, id_cuenta: int):
        super().__init__(id, nombre_completo)
        self.telefono = telefono
        self.id_cuenta = id_cuenta
