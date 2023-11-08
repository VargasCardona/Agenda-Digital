class CamposVaciosException(Exception):
    def __init__(self, message="Llene todos los campos"):
        super().__init__(message)

class CedulaInvalidaException(Exception):
    def __init__(self, message="La cédula debe ser un número"):
        super().__init__(message)

class CedulaEnUsoException(Exception):
    def __init__(self, message="La cédula se encuentra en uso"):
        super().__init__(message)

class CuentaEnUsoException(Exception):
    def __init__(self, message="La cuenta se encuentra en uso"):
        super().__init__(message)

class TelefonoInvalidoException(Exception):
    def __init__(self, message="El teléfono debe ser un número"):
        super().__init__(message)

class ContactoNoEncontradoException(Exception):
    def __init__(self, message="El contacto no fue encontrado"):
        super().__init__(message)

