import requests
from time import sleep
from influxdb import InfluxDBClient

baseURL = "https://api.n2yo.com/rest/v1/satellite/"

apiKey = "&apiKey=D3VQZD-CVXTLP-6G58TJ-4KB0"

client = InfluxDBClient(host='influxdb', port=8086, username='admin', password='admin', database="iss", pool_size=50)

client.create_database("iss")

client.create_retention_policy("standard", "1d", 1, default=True, shard_duration="1d")

while True:
#responseTLE = requests.get(baseURL + "tle/25544" + apiKey)
#print(responseTLE.json())

#responseVisualPasses = requests.get(baseURL + "visualpasses/25544/47.36667/8.55/500/8/1" + apiKey)
#print(responseVisualPasses.json())

    iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    print(iss)

    data = [
        {
            "measurement": "wtiss",
            "tags": {
                "satellite": iss["name"]
            },
            "fields": {
                "velocity": iss["velocity"],
                "latitude": iss["latitude"],
                "longitude": iss["longitude"]
            },
        },
    ]

    client.write_points(data, database="iss", time_precision='ms', protocol='json')

    sleep(10)

