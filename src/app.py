from flask import Flask , request, jsonify, Response , render_template
from flask_pymongo import PyMongo
from bson import json_util
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_URI']='mongodb+srv://juan:123@cluster0.3hzfhvm.mongodb.net/?retryWrites=true&w=majority'
#mongodb+srv://juan:123@cluster0.3hzfhvm.mongodb.net/?retryWrites=true&w=majority

mongo = PyMongo(app)

############### USUARIOS ###############

@app.route('/usuarios', methods=['POST'])
def create_user():
    # Receiving data
    nombre = request.json['nombre']
    edad = request.json['edad']
    correo = request.json['correo']
    telefono = request.json['telefono']
    direccion = request.json['direccion']

    print(request.json)
    
    if nombre and edad and correo and telefono and direccion:
        id = mongo.db.usuarios.insert_one(
            {'nombre': nombre, 'edad' : edad, 'correo': correo, 'telefono': telefono, 'direccion': direccion}
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'edad' : edad,
            'correo': correo,
            'telefono': telefono,
            'direccion': direccion
        }
        return response
    else:
        {'message': 'received'}
    
    return {'message': 'received'}

@app.route('/usuarios', methods=['GET'])
def get_users():
    users = mongo.db.usuarios.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/usuarios/<id>', methods=['GET'])
def get_user(id):
    usuario = mongo.db.usuarios.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(usuario)
    return Response(response, mimetype="application/json")

@app.route('/usuarios/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.usuarios.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'usuario' + id + 'ha sido eliminado exitosamente.'})
    return response

@app.route('/usuarios/<id>', methods = ['PUT'])
def update_user(id):
    nombre = request.json['nombre']
    edad = request.json['edad']
    correo = request.json['correo']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    
    if nombre and edad and correo and telefono and direccion:
        mongo.db.usuarios.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'edad': edad,
            'correo': correo,
            'telefono': telefono,
            'direccion': direccion
        }})
        response = jsonify({'mensaje': 'usuario' + id + 'se actualizado correctamente'})
        return response
    
################ LOCALIDADES ###############

@app.route('/localidades', methods=['POST'])
def create_localidad():
    codigo = request.json['codigo']
    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']

    if codigo and descripcion and ubicacion:
        id = mongo.db.localidades.insert_one(
            {'codigo': codigo, 'descripcion': descripcion, 'ubicacion': ubicacion}
        )
        response = {
            'id': str(id),
            'codigo': codigo,
            'descripcion': descripcion,
            'ubicacion': ubicacion
        }
        return response
    else:
        return {'message': 'Información incompleta'}


@app.route('/localidades', methods=['GET'])
def get_localidades():
    localidades = mongo.db.localidades.find()
    response = json_util.dumps(localidades)
    return Response(response, mimetype='application/json')


@app.route('/localidades/<id>', methods=['GET'])
def get_localidad(id):
    localidad = mongo.db.localidades.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(localidad)
    return Response(response, mimetype="application/json")


@app.route('/localidades/<id>', methods=['PUT'])
def update_localidad(id):
    codigo = request.json['codigo']
    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']

    if codigo and descripcion and ubicacion:
        mongo.db.localidades.update_one({'_id': ObjectId(id)}, {'$set': {
            'codigo': codigo,
            'descripcion': descripcion,
            'ubicacion': ubicacion
        }})
        response = jsonify({'mensaje': 'Localidad ' + id + ' se actualizó correctamente'})
        return response


@app.route('/localidades/<id>', methods=['DELETE'])
def delete_localidad(id):
    mongo.db.localidades.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Localidad ' + id + ' ha sido eliminada exitosamente.'})
    return response


########### Señales de Tránsito ###############
@app.route('/senales', methods=['POST'])
def create_senal():
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    aplicacion = request.json['aplicacion']

    if nombre and descripcion and aplicacion:
        id = mongo.db.senales.insert_one(
            {'nombre': nombre, 'descripcion': descripcion, 'aplicacion': aplicacion}
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'descripcion': descripcion,
            'aplicacion': aplicacion
        }
        return response
    else:
        return {'message': 'Información incompleta'}


@app.route('/senales', methods=['GET'])
def get_senales():
    senales = mongo.db.senales.find()
    response = json_util.dumps(senales)
    return Response(response, mimetype='application/json')


@app.route('/senales/<id>', methods=['GET'])
def get_senal(id):
    senal = mongo.db.senales.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(senal)
    return Response(response, mimetype="application/json")


@app.route('/senales/<id>', methods=['PUT'])
def update_senal(id):
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    aplicacion = request.json['aplicacion']

    if nombre and descripcion and aplicacion:
        mongo.db.senales.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'descripcion': descripcion,
            'aplicacion': aplicacion
        }})
        response = jsonify({'mensaje': 'Señal de Tránsito ' + id + ' se actualizó correctamente'})
        return response

@app.route('/senales/<id>', methods=['DELETE'])
def delete_senal(id):
    mongo.db.senales.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Señal de Tránsito ' + id + ' ha sido eliminada exitosamente.'})
    return response

############### Situaciónes de Riesgo #################
@app.route('/situaciones', methods=['POST'])
def registrar_situacion():
    nombre = request.json['nombre']
    tipo_actor_vial = request.json['tipo_actor_vial']
    direccion = {
        'localidad': request.json['localidad'],
        'barrio': request.json['barrio'],
        'zona': request.json['zona']
    }
    ubicacion = {
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    }
    existencia_senales = request.json.get('existencia_senales', False)

    if nombre and tipo_actor_vial and direccion and ubicacion:
        id = mongo.db.situaciones.insert_one(
            {
                'nombre': nombre,
                'tipo_actor_vial': tipo_actor_vial,
                'direccion': direccion,
                'ubicacion': ubicacion,
                'existencia_senales': existencia_senales
            }
        )
        response = {
            'id': str(id),
            'nombre': nombre,
            'tipo_actor_vial': tipo_actor_vial,
            'direccion': direccion,
            'ubicacion': ubicacion,
            'existencia_senales': existencia_senales
        }
        return response
    else:
        return {'message': 'Información incompleta'}


@app.route('/situaciones', methods=['GET'])
def get_situaciones():
    situaciones = mongo.db.situaciones.find()
    response = json_util.dumps(situaciones)
    return Response(response, mimetype='application/json')


@app.route('/situaciones/<id>', methods=['GET'])
def get_situacion(id):
    situacion = mongo.db.situaciones.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(situacion)
    return Response(response, mimetype="application/json")

@app.route('/situaciones/<id>', methods=['PUT'])
def update_situacion(id):
    nombre = request.json['nombre']
    tipo_actor_vial = request.json['tipo_actor_vial']
    direccion = {
        'localidad': request.json['localidad'],
        'barrio': request.json['barrio'],
        'zona': request.json['zona']
    }
    ubicacion = {
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    }
    existencia_senales = request.json.get('existencia_senales', False)

    if nombre and tipo_actor_vial and direccion and ubicacion:
        mongo.db.situaciones.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'tipo_actor_vial': tipo_actor_vial,
            'direccion': direccion,
            'ubicacion': ubicacion,
            'existencia_senales': existencia_senales
        }})
        response = jsonify({'mensaje': 'Situación de Riesgo ' + id + ' se actualizó correctamente'})
        return response

@app.route('/situaciones/<id>', methods=['DELETE'])
def delete_situacion(id):
    mongo.db.situaciones.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Situación de Riesgo ' + id + ' ha sido eliminada exitosamente.'})
    return response

########## Estadísticas de Seguridad Vial ################
@app.route('/estadisticas', methods=['POST'])
def create_estadistica():
    contenido = request.json['contenido']
    tipo_estadistica = request.json['tipo_estadistica']
    responsable = request.json.get('responsable', None)
    fecha = request.json.get('fecha', None)

    if contenido and tipo_estadistica:
        id = mongo.db.estadisticas.insert_one(
            {
                'contenido': contenido,
                'tipo_estadistica': tipo_estadistica,
                'responsable': responsable,
                'fecha': fecha
            }
        )
        response = {
            'id': str(id),
            'contenido': contenido,
            'tipo_estadistica': tipo_estadistica,
            'responsable': responsable,
            'fecha': fecha
        }
        return response
    else:
        return {'message': 'Información incompleta'}

@app.route('/estadisticas', methods=['GET'])
def get_estadisticas():
    estadisticas = mongo.db.estadisticas.find()
    response = json_util.dumps(estadisticas)
    return Response(response, mimetype='application/json')

@app.route('/estadisticas/<id>', methods=['GET'])
def get_estadistica(id):
    estadistica = mongo.db.estadisticas.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(estadistica)
    return Response(response, mimetype="application/json")

@app.route('/estadisticas/<id>', methods=['PUT'])
def update_estadistica(id):
    contenido = request.json['contenido']
    tipo_estadistica = request.json['tipo_estadistica']
    responsable = request.json.get('responsable', None)
    fecha = request.json.get('fecha', None)

    if contenido and tipo_estadistica:
        mongo.db.estadisticas.update_one({'_id': ObjectId(id)}, {'$set': {
            'contenido': contenido,
            'tipo_estadistica': tipo_estadistica,
            'responsable': responsable,
            'fecha': fecha
        }})
        response = jsonify({'mensaje': 'Estadística de Seguridad Vial ' + id + ' se actualizó correctamente'})
        return response

@app.route('/estadisticas/<id>', methods=['DELETE'])
def delete_estadistica(id):
    mongo.db.estadisticas.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Estadística de Seguridad Vial ' + id + ' ha sido eliminada exitosamente.'})
    return response

if __name__ == '__main__':
    app.run(debug=True)