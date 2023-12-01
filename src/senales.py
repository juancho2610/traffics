class Senales:
    def __init__(self, nombre, descripcion, aplicacion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.aplicacion = aplicacion

    def toDBCollection(self):
        situacion_dict = {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'aplicacion': self.aplicacion,
        }

        return situacion_dict