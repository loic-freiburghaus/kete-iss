import requests
import json
from time import sleep
from math import radians, sqrt, cos
from geopy import distance

BASEURL = "https://api.n2yo.com/rest/v1/satellite/"

APIKEY = "&APIKEY=D3VQZD-CVXTLP-6G58TJ-4KB0"

NORAD = "25544"

EARTHRADIUS = 6367449

while True:

    #response = requests.get(BASEURL+"/positions/35932/47.36667/8.55/408/2"+APIKEY).json()

    response = requests.get(BASEURL+"/positions/"+NORAD+"/47.36667/8.55/408/2"+APIKEY).json()

    print(response)

    coords1 = (response["positions"][0]["satlatitude"], response["positions"][0]["satlongitude"])
    coords2 = (response["positions"][1]["satlatitude"], response["positions"][1]["satlongitude"])
    altitudeInMeters = response["positions"][0]["sataltitude"] * 1000

    distanceInMeters = distance.distance(coords1, coords2).km * 1000

    satelliteSpeedInKMH = ((distanceInMeters * (EARTHRADIUS + altitudeInMeters)) / EARTHRADIUS) * 3.6

    # print(f"KMH: {kmh}")
    # print(f"KMH Weltall: {distanceWeltall}")

    print(satelliteSpeedInKMH)
    sleep(2)