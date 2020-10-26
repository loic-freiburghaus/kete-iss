import sys
import json
from kafka import KafkaConsumer
from influxdb import InfluxDBClient
client = InfluxDBClient(host='influxdb', port=8086, database='iss')
client.create_database('iss')
#client.create_retention_policy("standard", "1d", 1, default=True, shard_duration="1d")

# consumer = KafkaConsumer('iss',
#                          bootstrap_servers=['kafka:9092'],
#                          group_id='my-group',
#                          value_deserializer=lambda m: json.loads(m.decode('utf-8')))

#consumer = KafkaConsumer('iss', bootstrap_servers=['kafka:9092'],auto_offset_reset='earliest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

#consumer = KafkaConsumer('iss', bootstrap_servers=['kafka:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer = KafkaConsumer('iss', bootstrap_servers=['kafka:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

#consumer = KafkaConsumer('sample')
#for message in consumer:
#    print (message)

for message in consumer:

    print('got message!')
    print(message)
    data = [
        {
            "measurement": "wtiss",
            "tags": {
                "satellite": message.value["name"]
            },
            "fields": {
                "velocity": message.value["velocity"],
                "latitude": message.value["latitude"],
                "longitude": message.value["longitude"]
            },
        },
    ]

    client.write_points(data, database="iss", time_precision='ms', protocol='json')