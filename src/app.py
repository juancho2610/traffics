from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase  
from usuario import Usuario
from bson import ObjectId, json_util

db = dbase.dbConnection()

app = Flask(__name__)

#Rutas de la aplicación
@app.route('/')
def home():
    users = db['Usuarios']
    productsReceived = users.find()
    return render_template('index.html', users = productsReceived)

#Method Post
@app.route('/usuarios', methods=['POST'])
def addUser():
    users = db['Usuarios']
    
    if request.headers['Content-Type'] == 'application/json':
        # Si la solicitud es JSON
        nombre = request.json.get('nombre')
        edad = request.json.get('edad')
        correo = request.json.get('correo')
    else:
        # Si la solicitud es form data
        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        correo = request.form.get('correo')

    if nombre and edad and correo:
        usuario = Usuario(nombre, edad, correo)
        users.insert_one(usuario.toDBCollection())
        response = jsonify({
            'nombre' : nombre,
            'edad' : edad,
            'correo' : correo
        })
        return response
    else:
        return notFound()
    
#Method GET
@app.route('/usuarios', methods=['GET'])
def get_users():
    users_cursor = db['Usuarios'].find()
    print(users_cursor)
    users_list = list(users_cursor)
    print("users_list: ", users_list)
    # Excluye el campo '_id' de cada usuario
    for user in users_list:
        user.pop('_id', None)
    return jsonify({'usuarios': users_list})

#Method delete
@app.route('/delete/<string:usuario_id>')
def delete(usuario_id):
    users = db['Usuarios']
    users.delete_one({'_id' : ObjectId(usuario_id)})
    return redirect(url_for('home'))

#Method Put
@app.route('/edit/<string:usuario_id>', methods=['POST'])
def edit(usuario_id):
    users = db['Usuarios']
    nombre = request.form['nombre']
    edad = request.form['edad']
    correo = request.form['correo']

    if nombre and edad and correo:
        users.update_one({'_id' : usuario_id}, {'$set' : {'nombre' : nombre, 'edad' : edad, 'correo' : correo}})
        response = jsonify({'message' : 'Usuario ' + usuario_id + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

####################################
'''  
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
        'localidad': request.json['direccion']['localidad'],
        'barrio': request.json['direccion']['barrio'],
        'zona': request.json['direccion']['zona']
    }
    ubicacion = {
        'latitud': float(request.json['ubicacion']['latitud']),
        'longitud': float(request.json['ubicacion']['longitud'])
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
    nombre = request.json.get('nombre')
    tipo_actor_vial = request.json.get('tipo_actor_vial')
    
    direccion = request.json.get('direccion')
    if direccion:
        localidad = direccion.get('localidad')
        barrio = direccion.get('barrio')
        zona = direccion.get('zona')
    else:
        localidad = barrio = zona = None
    
    ubicacion = request.json.get('ubicacion')
    if ubicacion:
        latitud = ubicacion.get('latitud')
        longitud = ubicacion.get('longitud')
    else:
        latitud = longitud = None

    existencia_senales = request.json.get('existencia_senales', False)

    if nombre is not None and tipo_actor_vial is not None and (localidad is not None or barrio is not None or zona is not None) and (latitud is not None or longitud is not None):
        mongo.db.situaciones.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'tipo_actor_vial': tipo_actor_vial,
            'direccion': {
                'localidad': localidad,
                'barrio': barrio,
                'zona': zona
            },
            'ubicacion': {
                'latitud': latitud,
                'longitud': longitud
            },
            'existencia_senales': existencia_senales
        }})
        response = jsonify({'mensaje': 'Situación de Riesgo ' + id + ' se actualizó correctamente'})
        return response
    else:
        return jsonify({'mensaje': 'Información incompleta'})


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
    return response'''
####################################
if __name__ == '__main__':
    app.run(debug=True, port=5000)