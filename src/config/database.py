from pymongo import MongoClient


MONGO_URI = 'mongodb+srv://jojeda:pepe1234@cluster0.gq5ex.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

myclient = MongoClient(MONGO_URI)  # myclient es el cluster
mydb = myclient['myFirstDatabase']  # Dentro del cluster creo la base de datos llamada myFirstDatabase
