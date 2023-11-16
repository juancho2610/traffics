class Usuario:
    def __init__(self, nombre, edad, correo):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo

    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'edad': self.edad,
            'correo': self.correo
        }