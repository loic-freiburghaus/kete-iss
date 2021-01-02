#---------------KETE---------------
# producer_wiss/producer.py
# 02.01.2021
# Authors: Tina Messner, Sascha Sutter, Michael Ulrich, Loïc Freiburghaus
#
# Producer für die Where Is The ISS API.
#----------------------------------

import requests
from time import sleep
from kafka import KafkaProducer
import json

#Constant for API URL.
BASEURL = "https://api.wheretheiss.at/v1/satellites/25544"

#Creation of the Kafka Producer to port 9092 in JSON format.
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

#Infinite loop to get data from the n2yo API and sending it to kafka.
while True:

    #Requesting data from the Where Is The ISS API.
    response = requests.get(BASEURL).json()

    #Building the data JSON-object that is sent to kafka.
    data = {
            "name": response["name"],
            "id": response["id"],
            "velocity": float(response["velocity"]),
            "latitude": float(response["latitude"]),
            "longitude": float(response["longitude"]),
            "altitude": float(response["altitude"])    
        }

    #Send to the kafka producer on topic sat-data.
    producer.send('sat-data', data)
    
    #Wait 10 seconds until next call to the API.
    sleep(10)
