import requests
from time import sleep
from kafka import KafkaProducer
import json
from geopy import distance

BASEURL = "https://api.n2yo.com/rest/v1/satellite/"

APIKEY = "&APIKEY=D3VQZD-CVXTLP-6G58TJ-4KB0"

NORAD = "25544"

OBSERVER_LATITUDE = 47.36667
OBSERVER_LONGITUDE = 8.55
OBSERVER_ALTITUDE = 400

EARTHRADIUS = 6367449

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:

    response = requests.get(BASEURL+"/positions/"+NORAD+"/"+OBSERVER_LATITUDE+"/"+OBSERVER_LONGITUDE+"/"+OBSERVER_ALTITUDE+"/2"+APIKEY).json()

    coords1 = (response["positions"][0]["satlatitude"], response["positions"][0]["satlongitude"])
    coords2 = (response["positions"][1]["satlatitude"], response["positions"][1]["satlongitude"])
    altitudeInMeters = response["positions"][0]["sataltitude"] * 1000

    distanceInMeters = distance.distance(coords1, coords2).km * 1000

    satelliteSpeedInKMH = ((distanceInMeters * (EARTHRADIUS + altitudeInMeters)) / EARTHRADIUS) * 3.6

    data = {
            "name": response["info"]["satname"],
            "id": response["info"]["satid"],
            "velocity": float(satelliteSpeedInKMH),
            "latitude": float(response["positions"][0]["satlatitude"]),
            "longitude": float(response["positions"][0]["satlongitude"]),
            "altitude": float(response["positions"][0]["sataltitude"])
        }


    producer.send('sat-data', data)
    
    sleep(10)
