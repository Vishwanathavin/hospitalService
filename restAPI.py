# coding: utf-8
import json
from flask import Flask, render_template,request,jsonify
from flask_pymongo import PyMongo
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map, icons
import requests
import numpy
app = Flask(__name__, template_folder="templates")

# you can set key as config
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# you can also pass key here
# GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")


# Connect to database
app.config['MONGO_DBNAME'] = 'hospitalDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hospitalDB'
mongo = PyMongo(app)
@app.route('/')
def home():
	response = {'message': "Welcome to RESTAPI!"}
	return render_template('index.html')

@app.route("/input")
def getUserinputs():
    # get all the conditions. Read from file

    inpFilter = {
        'city': request.form.get('city'),
        'specializations': request.form.get('specializations'),
        # 'services_': request.form.get('services_')
    }
    print(inpFilter)
    # markerList =  mapview(inpFilter)
    return render_template('index.html')

def mapview(inpFilter):

    # Filter from database
    hospList = list(mongo.db.hospInfo.find({"$and":[{"specializations":{"$in":[inpFilter["specializations"]]}},{"city":inpFilter["city"]}]}))

    markerList = []
    for hosp in range(len(hospList)):

        # Get the LAT and LON
        lat=hospList[hosp]['location']['lat']
        lon = hospList[hosp]['location']['lng']
        markerList.append({"Lat":lat,"Lon":lon})
    #     marker = dict(
    #         {
    #             'icon':icons.alpha.H,
    #             'lat':  lat,
    #             'lng':  lon,
    #              'infobox': hospList[hosp]["hospital_private"]
    #         }
    #
    #     )
    #     markerList.append(marker)
    #
    #
    # lat, lng = getCityCoords(hospList)
    # trdmap = Map(
    #     identifier="trdmap",
    #     lat=lat,
    #     lng=lng,
    #
    #     markers=markerList
    #
    # )
    return markerList
    # return render_template('index.html', trdmap=trdmap)

def getCityCoords(hospList):
    lat = [hospList[hosp]['location']['lat'] for hosp in range(len(hospList))]
    lng = [hospList[hosp]['location']['lng'] for hosp in range(len(hospList))]
    print(lat,lng)
    sum_lat = numpy.sum(lat[:])
    sum_lng = numpy.sum(lng[:])
    # cityloc=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAUcvVet8YpEOZhlLmDzYBXPM2LD6jXRFU'%city).json()["results"][0]['geometry']['location']
    # lat,lng=cityloc['lat'],cityloc['lng']
    return sum_lat/len(hospList),sum_lng/len(hospList)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
