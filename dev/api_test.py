from apiclient import APIClient

baseURL = "https://api.n2yo.com/rest/v1/satellite/"

#https://api.n2yo.com/rest/v1/satellite/tle/25544&

apiKey = "&apiKey=D3VQZD-CVXTLP-6G58TJ-4KB0"

class MyClient(APIClient):

    def iss(self):
        url = baseURL + "tle/25544" + apiKey
        return self.get(url)

    def add_customer(self, customer_info):
        url = "http://example.com/customers"
        return self.post(url, data=customer_info)

client = MyClient()
#client.add_customer({"name": "John Smith", "age": 28})
issInfos = client.iss()

print(issInfos)