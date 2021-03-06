#---------------KETE---------------
# consumer/consumer.py
# 02.01.2021
# Authors: Tina Messner, Sascha Sutter, Michael Ulrich, Loïc Freiburghaus
#
# Consumer Script that consumes data from kafka and puts it in the InfluxDB database.
#----------------------------------

import json
from kafka import KafkaConsumer
from influxdb import InfluxDBClient
from time import sleep

#Constant for the name of the database.
DB = "satellites"

#Creation of the InfluxDB Client and of the database.
client = InfluxDBClient(host='influxdb', port=8086, database=DB)
client.create_database(DB)
#Automatically delete data from the database after 1 day.
client.create_retention_policy("standard", "1d", 1, default=True, shard_duration="1d")

#Wait until kafka is ready
consumerNotRunning = True
while consumerNotRunning:
    try:
        #Create the kafka consumer on port 9092 for topic sat-data. Consuming JSON data.
        consumer = KafkaConsumer('sat-data', bootstrap_servers=['kafka:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumerNotRunning = False
    except:
        print("Error at creating kafka consumer")
        sleep(1)

#For each incoming message
for message in consumer:

    #Extract data from the incoming message and create a JSON data object to insert into InfluxDB.
    data = [
        {
            "measurement": "satellites",
            "tags": {
                "satellite": message.value["name"]
            },
            "fields": {
                "id": message.value["id"],
                "velocity": message.value["velocity"],
                "latitude": message.value["latitude"],
                "longitude": message.value["longitude"],
                "altitude": message.value["altitude"]
            },
        },
    ]

    #Write JSON data object into InfluxDB
    client.write_points(data, database=DB, time_precision='ms', protocol='json')