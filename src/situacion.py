class Situacion:
    def __init__(self, localidad, tipo_actor_vial, direccion, ubicacion, existencia_senales):
        self.localidad = localidad
        self.tipo_actor_vial = tipo_actor_vial
        self.direccion = direccion
        self.ubicacion = ubicacion
        self.existencia_senales = existencia_senales

    def toDBCollection(self):
        return{
            'nombre': self.localidad,
            'tipo_actor_vial': self.tipo_actor_vial,
            'direccion': self.direccion,
            'ubicacion' : self.ubicacion,
            'existencia_senales': self.existencia_senales
        }