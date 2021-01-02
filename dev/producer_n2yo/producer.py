#---------------KETE---------------
# producer_n2yo/producer.py
# 02.01.2021
# Authors: Tina Messner, Sascha Sutter, Michael Ulrich, Loïc Freiburghaus
#
# Producer für die N2YO API.
#----------------------------------

import requests
from time import sleep
from kafka import KafkaProducer
import json
from geopy import distance

#Constants for URL, API-Key, NORAD ID, Obeserver Coordinates and radius of the earth.
BASEURL = "https://api.n2yo.com/rest/v1/satellite/"

APIKEY = "&APIKEY=D3VQZD-CVXTLP-6G58TJ-4KB0"

NORAD = "25544"

OBSERVER_LATITUDE = 47.36667
OBSERVER_LONGITUDE = 8.55
OBSERVER_ALTITUDE = 400

EARTHRADIUS = 6367449

#Creation of the Kafka Producer to port 9092 in JSON format.
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

#Infinite loop to get data from the n2yo API and sending it to kafka.
while True:
    #Requesting data from the n2yo-API.
    #Requests two positions one second apart to be able to calculate the speed.
    response = requests.get(BASEURL+"/positions/"+NORAD+"/"+OBSERVER_LATITUDE+"/"+OBSERVER_LONGITUDE+"/"+OBSERVER_ALTITUDE+"/2"+APIKEY).json()

    #Extracting coordinates and altitude from the response.
    coords1 = (response["positions"][0]["satlatitude"], response["positions"][0]["satlongitude"])
    coords2 = (response["positions"][1]["satlatitude"], response["positions"][1]["satlongitude"])
    altitudeInMeters = response["positions"][0]["sataltitude"] * 1000

    #Calculating the distance between two coordinates of the satellite.
    distanceInMeters = distance.distance(coords1, coords2).km * 1000

    #With the calculated distance, calculate the speed of the satellite.
    satelliteSpeedInKMH = ((distanceInMeters * (EARTHRADIUS + altitudeInMeters)) / EARTHRADIUS) * 3.6

    #Building the data JSON-object that is sent to kafka.
    data = {
            "name": response["info"]["satname"],
            "id": response["info"]["satid"],
            "velocity": float(satelliteSpeedInKMH),
            "latitude": float(response["positions"][0]["satlatitude"]),
            "longitude": float(response["positions"][0]["satlongitude"]),
            "altitude": float(response["positions"][0]["sataltitude"])
        }

    #Send to the kafka producer on topic sat-data.
    producer.send('sat-data', data)
    
    #Wait 10 seconds until next call to the API.
    sleep(10)
