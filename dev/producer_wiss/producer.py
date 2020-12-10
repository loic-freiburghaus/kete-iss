import requests
from time import sleep
from kafka import KafkaProducer
import json

baseURL = "https://api.wheretheiss.at/v1/satellites/25544"

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:

    response = requests.get(baseURL).json()

    data = {
            "name": response["name"],
            "id": response["id"],
            "velocity": float(response["velocity"]),
            "latitude": float(response["latitude"]),
            "longitude": float(response["longitude"]),
            "altitude": float(response["altitude"])    
        }

    producer.send('sat-data', data)

    sleep(10)
