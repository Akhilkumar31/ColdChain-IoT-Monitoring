import time
import json
import random
import ssl
import os
from faker import Faker
from decimal import Decimal
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve and debug MQTT configuration
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT_ENV = os.getenv("MQTT_PORT")
MQTT_PORT = int(MQTT_PORT_ENV) if MQTT_PORT_ENV else 8883
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "cold_chain_data")

# Debug prints
print("\n--- MQTT Configuration ---")
print("📡 MQTT_BROKER:", MQTT_BROKER)
print("🔢 MQTT_PORT:", MQTT_PORT)
print("👤 MQTT_USERNAME:", MQTT_USERNAME)
print("📨 MQTT_TOPIC:", MQTT_TOPIC)
print("---------------------------\n")

# Initialize Faker
fake = Faker()

# Fix Decimal serialization
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Define MQTT callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Successfully connected to MQTT Broker!")
    else:
        print(f"❌ Connection failed with code {rc}")

# Create and configure MQTT client
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.tls_insecure_set(False)

# Connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        # Generate data
        data = {
            "temperature": round(random.uniform(2.0, 8.0), 2),
            "humidity": round(random.uniform(30.0, 50.0), 2),
            "light": random.randint(0, 1023),
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "timestamp": int(time.time())
        }

        # Serialize JSON safely
        payload = json.dumps(data, default=decimal_default)

        # Publish
        result = client.publish(MQTT_TOPIC, payload)
        status = result[0]

        if status == mqtt.MQTT_ERR_SUCCESS:
            print(f"📤 Published to {MQTT_TOPIC} → {payload}")
        else:
            print("⚠️ Failed to publish. Retrying...")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n⛔ Publishing stopped by user.")

finally:
    client.loop_stop()
    client.disconnect()
    print("🔌 Disconnected from MQTT Broker.")
