import requests
from time import sleep
from influxdb import InfluxDBClient
from kafka import KafkaProducer
import json

baseURL = "https://api.n2yo.com/rest/v1/satellite/"

apiKey = "&apiKey=D3VQZD-CVXTLP-6G58TJ-4KB0"

#producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

#producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#producer.send('iss', b'Hello, World!')
#producer.send('sample', key=b'message-two', value=b'This is Kafka-Python')

while True:
#responseTLE = requests.get(baseURL + "tle/25544" + apiKey)
#print(responseTLE.json())

#responseVisualPasses = requests.get(baseURL + "visualpasses/25544/47.36667/8.55/500/8/1" + apiKey)
#print(responseVisualPasses.json())

    iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    #print(iss)

    producer.send('iss', iss)
    #producer.send('iss', {'topic' : 'hey'})
    #producer.send('iss', b'Hello, World!')
    print("sent")
    #producer.send('iss', value={"iss": "iss"})
    #producer.send('iss', iss["velocity"])

    sleep(10)

