class Localidad :
    def __init__(self, nombre, codigo, ubicacion):
        self.nombre = nombre
        self.codigo = codigo
        self.ubicacion = ubicacion

    def toDBCollection(self):
        situacion_dict = {
            'nombre' : self.nombre,
            'codigo': self.codigo,
            'ubicacion': self.ubicacion,
        }

        return situacion_dict