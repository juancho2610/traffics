class Situacion:
    def __init__(self, localidad, barrio, descripcion, fecha, tipo_actor_vial, direccion, ubicacion, existencia_senales, funcional=None, senal_propuesta=None, argumento=None):
        self.localidad = localidad
        self.barrio = barrio
        self.descripcion = descripcion
        self.fecha = fecha
        self.tipo_actor_vial = tipo_actor_vial
        self.direccion = direccion
        self.ubicacion = ubicacion
        self.existencia_senales = existencia_senales
        self.funcional = funcional
        self.senal_propuesta = senal_propuesta
        self.argumento = argumento

    def toDBCollection(self):
        situacion_dict = {
            'localidad': self.localidad,
            'barrio': self.barrio,
            'descripcion': self.descripcion,
            'fecha': self.fecha,
            'tipo_actor_vial': self.tipo_actor_vial,
            'direccion': self.direccion,
            'ubicacion': self.ubicacion,
            'existencia_senales': self.existencia_senales,
        }

        if self.existencia_senales:
            situacion_dict['funcional'] = self.funcional

        if not self.funcional:
            situacion_dict['senal_propuesta'] = self.senal_propuesta
            situacion_dict['argumento'] = self.argumento

        return situacion_dict
