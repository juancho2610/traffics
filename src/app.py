from flask import Flask , request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/trafficProyect'

mongo = PyMongo(app)

@app.route('/usuarios', methods=['POST'])
def create_user():
    # Receiving data
    nombre = request.json['nombre']
    edad = request.json['edad']
    correo = request.json['correo']
    telefono = request.json['telefono']
    direccion = request.json['direccion']
    
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
    print(id)
    return 'received'

if __name__ == "__main__":
    app.run(debug=True)