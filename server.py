import flask
import math
from math import sin, cos, sqrt, atan2, radians
from flask_pymongo import PyMongo
from pymongo import MongoClient
import time
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import json
from geopy import distance
from geopy import Point

#mongodb+srv://eugenetan:<password>@backend-serv.wnkwk.gcp.mongozdb.net/<dbname>?retryWrites=true&w=majority

app = flask.Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://eugenetan:Swimming1337@backend-serv.wnkwk.gcp.mongodb.net/server-gsd?retryWrites=true&w=majority"
app.config['MONGO_DBNAME'] = 'server-gsd'
app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app)
db = mongo.db
col = mongo.db['server-gsd']
uuid = mongo.db['data']
fivesec = mongo.db['future_5']
tensec = mongo.db['future_10']
fifteensec = mongo.db['future_15']
thirtysec = mongo.db['future_30']



print ("MongoDB Database:", mongo.db)

STOP_LIGHT = True

def distance_from(point1: Point, point2: Point):
    result = distance.distance(point1, point2).ft
    print(result)
    return result

def proximity_check(point1: Point, point2: Point):
    distance = distance_from(point1, point2)
    if distance <= 50:
        return True
    else:
        return False

def stop_light_check(point1: Point):
    pass
    

def ideal_next_position(point1: Point, rbearing: float, speed: float, time: float):
    #time_s = 1 #next position (realtime)
    displacement = float(speed) * time
    #fix next coordinate position
    displacement = displacement / 1000

    radian_bearing = math.radians(rbearing)
    print(radian_bearing)
    radius_Earth = 6371.1
    rdistance = displacement / radius_Earth

    lat1 = math.radians(point1.latitude)
    lon1 = math.radians(point1.longitude)

    lat2 = math.asin(math.sin(lat1)*math.cos(rdistance) + math.cos(lat1)*math.sin(rdistance)*math.cos(radian_bearing))
    lon2 = lon1 + math.atan2(math.sin(radian_bearing)*math.sin(rdistance)*math.cos(lat1),math.cos(rdistance)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
  
    new_coord = Point(lat2, lon2)
    return new_coord

    #finish calculating the distance with point

    #15 seperate future collections
    # 1 minute, 5 min, 
    # introduce delays/obstacles

@app.route("/", methods=['GET','POST'])
def dinput():
    data = request.get_json()
    latitude = (float)(data['Latitude'])
    print(latitude)
    longitude = (float)(data['Longitude'])
    print(longitude)
    unique_uid = (str)(data['UUID'])
    print(unique_uid)
    speed = (str)(data['Speed'])
    print(speed)
    item = Point(latitude, longitude)
    print(item)
    uuid.update({'UUID': unique_uid}, {'$set': {'latitude': latitude, 'longitude': longitude, 'speed': speed}}, upsert=True)

    dummy_bearing = 90.000

    five_sec_pos = ideal_next_position(item, dummy_bearing, speed, 5.0)
    #print("Latitude: " + str(five_sec_pos.latitude) + " Longitude: " + str(five_sec_pos.longitude))
    fivesec.update({'UUID': unique_uid}, {'$set': {'latitude': five_sec_pos.latitude, 'longitude': five_sec_pos.longitude, 'speed': speed}}, upsert=True)

    ten_sec_pos = ideal_next_position(item, dummy_bearing, speed, 10.0)
    tensec.update({'UUID': unique_uid}, {'$set': {'latitude': five_sec_pos.latitude, 'longitude': five_sec_pos.longitude, 'speed': speed}}, upsert=True)

    fifteen_sec_pos = ideal_next_position(item, dummy_bearing, speed, 15.0)
    fifteensec.update({'UUID': unique_uid}, {'$set': {'latitude': five_sec_pos.latitude, 'longitude': five_sec_pos.longitude, 'speed': speed}}, upsert=True)

    thirty_sec_pos = ideal_next_position(item, dummy_bearing, speed, 30.0)
    thirtysec.update({'UUID': unique_uid}, {'$set': {'latitude': five_sec_pos.latitude, 'longitude': five_sec_pos.longitude, 'speed': speed}}, upsert=True)

    for x in uuid.find({'UUID': { '$ne': unique_uid}}):
        print(x)
        other_coord = Point(x['latitude'], x['longitude'])
        value = proximity_check(item, other_coord)

    x = col.insert_one(data)
    
    return str(value)

@app.route("/distance", methods=['GET', 'POST'])
def dcalc():
    pass

if __name__== '__main__':
    app.run(debug=True)