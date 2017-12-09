# Get the data from the URL to the database and add lat lon to it
import pymongo
import requests

# import numpy as np
import json

def database():
    try:
        conn = pymongo.MongoClient()
        print("Connected successfully!!!")
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
    hospDatabase = conn['hospitalDB']

    hosptialInfo = json.load(open('./data/APIData.json'))['records']

    for hosp in hosptialInfo:
        hosp["ID"] = 'ID_'+ '%04d'%hosptialInfo.index(hosp)

        for col in ['services_','specializations']:
            hosp[col]=hosp[col].split()

        hospName = hosp['hospital_private']
        print(hosp['ID'],hospName)
        address = hosp['contact_details'].split(',')
        address=[val.strip() for val in address ]
        if(hosp['city'] in address):
            contactDetails = address[address.index(hosp['city']) - 1]
            address = hospName + ' ' + contactDetails
            hosploc = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAUcvVet8YpEOZhlLmDzYBXPM2LD6jXRFU' % address).json()[
            "results"]
            if len(hosploc)>0:
                hosp["location"] =  hosploc[0]['geometry']['location']
        hospDatabase.hospInfo.update({"_id": hosp["ID"]}, {'$set': hosp}, upsert=True)

    message = {"message": "Hello Vishwa"}
    return

database()
