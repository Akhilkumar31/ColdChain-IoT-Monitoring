import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

MQTT_BROKER = "709f4a6d34fb4b1c96197e61530f885c.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "akhilkumar312001"
MQTT_PASSWORD = "Akhil@2001"
MQTT_TOPIC = "iot/sensor"

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    mqtt_client.subscribe(MQTT_TOPIC)

def on_message(mqtt_client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        point = Point("cold_chain_data") \
            .field("temperature", data["temperature"]) \
            .field("humidity", data["humidity"]) \
            .field("light", data["light"]) \
            .field("latitude", float(data["latitude"])) \
            .field("longitude", float(data["longitude"])) \
            .time(data["timestamp"])
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Data written to InfluxDB: {data}")
    except Exception as e:
        print(f"Error: {e}")

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
