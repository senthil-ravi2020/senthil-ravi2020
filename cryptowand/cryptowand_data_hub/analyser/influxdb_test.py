from datetime import datetime


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "5Tp3wHcAE9SCSReFWMubX8We4G6x_PfOf9lI36UdR4AQoz8fFQrUXyFbVjix-PSPgrKza_l0FwD37O7FvW2eNg=="
org = "Cryptowand"
bucket = "cryptos"

client = InfluxDBClient(url="http://localhost:8086", token=token)

client.create_database('cryptowand')
client.get_list_database()