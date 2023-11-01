import modelos.persona as persona

class Cuenta(persona.Persona):
    def __init__(self, id: int, usuario: str, contrasenia: str, nombre_completo: str, cedula: int):
        super().__init__(id, nombre_completo)
        self.cedula = cedula
        self.usuario = usuario
        self.contrasenia = contrasenia

