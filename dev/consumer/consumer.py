import json
from kafka import KafkaConsumer
from influxdb import InfluxDBClient

DB = "satellites"

client = InfluxDBClient(host='influxdb', port=8086, database=DB)
client.create_database(DB)
#client.create_retention_policy("standard", "1d", 1, default=True, shard_duration="1d")

consumer = KafkaConsumer('sat-data', bootstrap_servers=['kafka:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:

    #print('got message!')
    #print(message)
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

    client.write_points(data, database=DB, time_precision='ms', protocol='json')