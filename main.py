# coding: utf-8

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import requests
import numpy
app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# you can also pass key here
GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")


@app.route("/")
def mapview():
    return "< h1 style = 'color:blue' > Howdy ! < / h1 >"
    # hospList= getHospitalcoords('Chennai')
    #
    # markerList = []
    # for hosp in range(len(hospList)):
    #     print (hospList[hosp]['location']['lat'],hospList[hosp]['location']['lng'])
    #
    #     lat=hospList[hosp]['location']['lat']
    #     lon = hospList[hosp]['location']['lng']
    #     marker = dict(
    #         {
    #             'icon':icons.alpha.B,
    #             'lat':  lat,
    #             'lng':  lon,
    #             # 'infobox': "Hello I am < b style='color:green;'>B< / b >!"
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
    #     # markers=[
    #     #     {
    #     #         'icon': icons.images.icon7,
    #     #         'lat':  lat,
    #     #         'lng':  lng,
    #     #         'infobox': "Hello I am < b style='color:green;'>B< / b >!"
    #     #     }
    #     # ]
    # )
    # return render_template('example.html', trdmap=trdmap)
    # return

def getCityCoords(hospList):
    lat = [hospList[hosp]['location']['lat'] for hosp in range(len(hospList))]
    lng = [hospList[hosp]['location']['lng'] for hosp in range(len(hospList))]
    print(lat,lng)
    sum_lat = numpy.sum(lat[:])
    sum_lng = numpy.sum(lng[:   ])
    # cityloc=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAUcvVet8YpEOZhlLmDzYBXPM2LD6jXRFU'%city).json()["results"][0]['geometry']['location']
    # lat,lng=cityloc['lat'],cityloc['lng']
    return sum_lat/len(hospList),sum_lng/len(hospList)

def getHospitalcoords(city):

    hosptialInfo = requests.get('https://api.data.gov.in/resource/b4d77a09-9cdc-4a5b-b900-8fddb78f3cbe?format=json&api-key=579b464db66ec23bdd000001475eae9e22084c274825b6facbddcb05&filters[city]=%s&limit=100'%city).json()['records']
    hospList=[]
    for hosp in range(len(hosptialInfo)):
        hospName=hosptialInfo[hosp]['hospital_private']
        address = hosptialInfo[hosp]['contact_details'].split(', ')
        print (address)
        contactDetails=address[address.index(city)-1]
        address = hospName+' '+contactDetails
        hosploc = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAUcvVet8YpEOZhlLmDzYBXPM2LD6jXRFU' % address).json()[
            "results"][0]['geometry']['location']
        hospList.append(dict({"name":hospName,"location":hosploc}))

    return hospList
if __name__ == "__main__":
    app.run(host='0.0.0.0')
