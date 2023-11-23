class Usuario:
    def __init__(self, nombre, edad, correo, password):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.password = password

    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'edad': self.edad,
            'correo': self.correo,
            'password' : self.password
        }