from bson import ObjectId
from flask import Flask, request,jsonify
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


app = Flask(__name__)

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["last-test"]



@app.route("/")
def show():
    datos = list(db.users.find())
    
    for i in datos:
        i["_id"] = str(i["_id"])
    
    return jsonify({"msg":datos})
    
    
@app.route("/add", methods=["POST"])
def add():
    
    data = request.get_json()
    nombre = data["nombre"]

    if nombre:
        db.users.insert_one({"nombre":nombre}) 
        return jsonify({"msg":"añadido"})
    else:
        return jsonify({"msg":"añadido"})
    
@app.route("/edit/<string:id>", methods=["PUT"]) 
def edit(id):
    data = request.get_json()
    nombre = data["nombre"]
    
    if nombre:
        db.users.update_one({"_id":ObjectId(id)},{"$set":{"nombre":nombre}})
        return jsonify({"msg":"editado"})
    else:
        return jsonify({"msg":"no editado"})
    
@app.route("/delete/<string:id>", methods=["DELETE"])
def delete(id):
    
    user = db.users.delete_one({"_id":ObjectId(id)})
    if user:
        return jsonify({"msg":"eliminado"})
    else:
        return jsonify({"msg":"no eliminado"})
        
    
    
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")