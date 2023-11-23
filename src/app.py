from functools import wraps
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session
import database as dbase  
from usuario import Usuario
from bson import ObjectId, json_util

db = dbase.dbConnection()

app = Flask(__name__)
app.secret_key ="SoloGamers@123"

# Función para verificar si el usuario está autenticado
def verificar_autenticacion(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'us' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))  # Redirigir a la página de inicio de sesión si el usuario no está autenticado
    return wrapper

#Rutas de la aplicación
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index')
@verificar_autenticacion
def index():
    users = db['Situaciones']
    situacionesReceived = users.find()
    return render_template('index.html', situaciones=situacionesReceived)

@app.route('/registro')
def registro():
    return render_template('registro.html')

############# INICIO DE SESION ###############
@app.route('/login', methods=['POST'])
def login():
    users = db['Usuarios']
    nombre = request.form['nombre']
    print("nombre:",nombre)
    correo = request.form['correo']
    print(correo)
    password = request.form['password']
    print(password)

    # Verificar las credenciales del usuario en la base de datos
    us = users.find_one({'nombre': nombre, 'correo': correo, 'password': password})
    print("us:", us)
    if us:
        session['us'] = nombre
        session['us'] = correo
        session['us'] = password  # Iniciar sesión
        return redirect(url_for('index'))  # Redirigir al menú después del inicio de sesión exitoso
    
    return "Credenciales inválidas"  # Mensaje de error si las credenciales son incorrectas

################ USUARIOS ###############
#Method Post
@app.route('/usuarios', methods=['POST'])
def usuarios():
    if request.method == 'POST':
        users = db['Usuarios']

        if request.headers['Content-Type'] == 'application/json':
            # Si la solicitud es JSON
            nombre = request.json.get('nombre')
            edad = request.json.get('edad')
            correo = request.json.get('correo')
            password = request.json.get('password')
        else:
            # Si la solicitud es form data
            nombre = request.form.get('nombre')
            edad = request.form.get('edad')
            correo = request.form.get('correo')
            password = request.form.get('password')

        if nombre and edad and correo and password:
            usuario = Usuario(nombre, edad, correo, password)

            # Verificar si el correo o el nombre ya existen en la base de datos.
            existe_usuario = users.find_one({'$or': [{'nombre': nombre}, {'correo': correo}]})
            if existe_usuario:
                return 'El nombre de usuario o correo ya están registrados'
            else:
                users.insert_one(usuario.toDBCollection())
                response = jsonify({
                    'nombre': nombre,
                    'edad': edad,
                    'correo': correo,
                    'password': password
                })
                return redirect(url_for('home'))  # Redirigir a la página principal o a donde desees
        else:
            return 'Datos incorrectos: el nombre, correo o contraseña no cumplen los requisitos'

    return render_template('login.html')
    
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

############################################
################ LOCALIDADES ###############

@app.route('/localidades', methods=['POST'])
def create_localidad():
    localidades = db['Localidades']
    codigo = request.json['codigo']
    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']

    if codigo and descripcion and ubicacion:
        id = localidades.insert_one(
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
    localidades = db['Localidades']
    found_localidades = localidades.find()
    response = json_util.dumps(found_localidades)
    return Response(response, mimetype='application/json')


@app.route('/localidades/<id>', methods=['GET'])
def get_localidad(id):
    localidades = db['Localidades']
    localidad_get = localidades.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(localidad_get)
    return Response(response, mimetype="application/json")


@app.route('/localidades/<id>', methods=['PUT'])
def update_localidad(id):
    localidades = db['Localidades']
    codigo = request.json['codigo']
    descripcion = request.json['descripcion']
    ubicacion = request.json['ubicacion']

    if codigo and descripcion and ubicacion:
        localidades.update_one({'_id': ObjectId(id)}, {'$set': {
            'codigo': codigo,
            'descripcion': descripcion,
            'ubicacion': ubicacion
        }})
        response = jsonify({'mensaje': 'Localidad ' + id + ' se actualizó correctamente'})
        return response


@app.route('/localidades/<id>', methods=['DELETE'])
def delete_localidad(id):
    localidades = db['Localidades']
    localidades.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Localidad ' + id + ' ha sido eliminada exitosamente.'})
    return response


########### Señales de Tránsito ###############
@app.route('/senales', methods=['POST'])
def create_senal():
    localidades = db['Localidades']
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    aplicacion = request.json['aplicacion']

    if nombre and descripcion and aplicacion:
        id = localidades.insert_one(
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
    senales = db['Senales']
    senales_get = senales.find()
    response = json_util.dumps(senales_get)
    return Response(response, mimetype='application/json')


@app.route('/senales/<id>', methods=['GET'])
def get_senal(id):
    senales = db['Senales']
    senal = senales.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(senal)
    return Response(response, mimetype="application/json")


@app.route('/senales/<id>', methods=['PUT'])
def update_senal(id):
    senales = db['Senales']
    nombre = request.json['nombre']
    descripcion = request.json['descripcion']
    aplicacion = request.json['aplicacion']

    if nombre and descripcion and aplicacion:
        senales.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'descripcion': descripcion,
            'aplicacion': aplicacion
        }})
        response = jsonify({'mensaje': 'Señal de Tránsito ' + id + ' se actualizó correctamente'})
        return response

@app.route('/senales/<id>', methods=['DELETE'])
def delete_senal(id):
    senales = db['Senales']
    senales.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Señal de Tránsito ' + id + ' ha sido eliminada exitosamente.'})
    return response

############### Situaciones de Riesgo #################
@app.route('/situaciones', methods=['POST'])
def registrar_situacion():
    situaciones = db['Situaciones']
    
    ####### POSTMAN #######
    if request.headers['Content-Type'] == 'application/json':
        # Si la solicitud es JSON, se mantiene la lógica anterior
        localidad = request.json['localidad']
        tipo_actor_vial = request.json['tipo_actor_vial']
        direccion = request.json['direccion']
        ubicacion = {
            'latitud': float(request.json['ubicacion']['latitud']),
            'longitud': float(request.json['ubicacion']['longitud'])
        }
        existencia_senales = request.json.get('existencia_senales', False)
        response = {
            'id': str(id),
            'localidad': localidad,
            'tipo_actor_vial': tipo_actor_vial,
            'direccion': direccion,
            'ubicacion': ubicacion,
            'existencia_senales': existencia_senales
        }
        return response
    ######### FORM ##########
    else:
        # Si la solicitud es form data, se adaptan los campos del formulario HTML
        localidad = request.form['localidad']
        tipo_actor_vial = request.form['tipo_actor_vial']
        direccion = request.form['direccion']
        ubicacion = {
            'latitud': float(request.form['latitud']),
            'longitud': float(request.form['longitud'])
        }
        existencia_senales = request.form.get('existencia_senales', False)

        if localidad and tipo_actor_vial and direccion and ubicacion:
            id = situaciones.insert_one(
                {
                    'localidad': localidad,
                    'tipo_actor_vial': tipo_actor_vial,
                    'direccion': direccion,
                    'ubicacion': ubicacion,
                    'existencia_senales': existencia_senales
                }
            )
            return redirect(url_for('index'))  # Redirige al index después de la inserción exitosa
        else:
            return {'message': 'Información incompleta'}


@app.route('/situaciones', methods=['GET'])
def get_situaciones():
    situaciones = db['Situaciones']
    situaciones_get = situaciones.find()
    response = json_util.dumps(situaciones_get)
    return Response(response, mimetype='application/json')


@app.route('/situaciones/<id>', methods=['GET'])
def get_situacion(id):
    situaciones = db['Situaciones']
    situaciones_get = situaciones.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(situaciones_get)
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
        situaciones = db['Situaciones']
        situaciones.update_one({'_id': ObjectId(id)}, {'$set': {
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
    situaciones = db['Situaciones']
    situaciones.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Situación de Riesgo ' + id + ' ha sido eliminada exitosamente.'})
    return response

########## Estadísticas de Seguridad Vial ################
@app.route('/estadisticas', methods=['POST'])
def create_estadistica():
    estadisticas= db['Estadisticas']
    contenido = request.json['contenido']
    tipo_estadistica = request.json['tipo_estadistica']
    responsable = request.json.get('responsable', None)
    fecha = request.json.get('fecha', None)

    if contenido and tipo_estadistica:
        id = estadisticas.insert_one(
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
    estadisticas= db['Estadisticas']
    estadisticas = estadisticas.find()
    response = json_util.dumps(estadisticas)
    return Response(response, mimetype='application/json')

@app.route('/estadisticas/<id>', methods=['GET'])
def get_estadistica(id):
    estadisticas= db['Estadisticas']
    estadisticas_get = estadisticas.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(estadisticas_get)
    return Response(response, mimetype="application/json")

@app.route('/estadisticas/<id>', methods=['PUT'])
def update_estadistica(id):
    estadisticas= db['Estadisticas']
    contenido = request.json['contenido']
    tipo_estadistica = request.json['tipo_estadistica']
    responsable = request.json.get('responsable', None)
    fecha = request.json.get('fecha', None)

    if contenido and tipo_estadistica:
        estadisticas.update_one({'_id': ObjectId(id)}, {'$set': {
            'contenido': contenido,
            'tipo_estadistica': tipo_estadistica,
            'responsable': responsable,
            'fecha': fecha
        }})
        response = jsonify({'mensaje': 'Estadística de Seguridad Vial ' + id + ' se actualizó correctamente'})
        return response

@app.route('/estadisticas/<id>', methods=['DELETE'])
def delete_estadistica(id):
    estadisticas= db['Estadisticas']
    estadisticas.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensaje': 'Estadística de Seguridad Vial ' + id + ' ha sido eliminada exitosamente.'})
    return response

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('us', None)
    return redirect(url_for('home')) 

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

##########################################
if __name__ == '__main__':
    app.run(debug=True, port=5000)