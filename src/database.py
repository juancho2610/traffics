from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://daniel:123@cluster0.wviqym6.mongodb.net'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        #conectar a la base de datos especificada
        db = client["TrafficDB"] 
    except ConnectionError:
        print('Error de conexión con la base de datos de arquitecturas')
    return db
