import flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json

#mongodb+srv://eugenetan:<password>@backend-serv.wnkwk.gcp.mongozdb.net/<dbname>?retryWrites=true&w=majority

app = flask.Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://eugenetan:Swimming1337@backend-serv.wnkwk.gcp.mongodb.net/server-gsd?retryWrites=true&w=majority"
app.config['MONGO_DBNAME'] = 'server-gsd'
app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app)
db = mongo.db
col = mongo.db['server-gsd']
print ("MongoDB Database:", mongo.db)
#print ("MondoDB Collection:", col)

@app.route("/", methods=['POST'])
def dinput():

    data = request.get_json()
    x = col.insert_one(data)
    return 'Wow!'

@app.route("/distance", methods=['GET', 'POST'])
def dcalc():
    pass

if __name__== '__main__':
    app.run(debug=True)