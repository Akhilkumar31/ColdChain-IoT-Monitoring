Team Members: Akhil Kumar Puri, Abhinav Rao Veeramalla
# 🧊 Cold Chain IoT Monitoring System

An end-to-end IoT solution for real-time monitoring of temperature-sensitive goods such as vaccines, food, or pharmaceuticals. This system uses an ESP32 microcontroller, various sensors, MQTT for secure cloud transmission, InfluxDB for time-series data storage, and Grafana for real-time visualization.

---

## 📦 Project Structure

```
│
├── bridge_script/
│ └── mqtt_to_influxdb.py # Python script to receive MQTT and write to InfluxDB
│
├── cold_chain_sensor_copy_20250508220111/
│ └── cold_chain_sensor_copy_20250508220111.ino # Arduino sketch for ESP32
│
├── dashboard/
│ └── Cold Chain Monitoring-1746755953723.json # Grafana dashboard export
│
├── mqtt_publisher/
│ ├── influxdb_config.env # InfluxDB connection configuration
│ └── mqtt_publisher.py # Script to publish MQTT messages (testing/simulation)
│
├── simulated_data/
│ └── generate_simulated_data.py # Script to generate test sensor data
│
├── telegraf.conf # Telegraf config for MQTT-to-InfluxDB pipeline
├── README.md # This file

---

## 📡 Hardware Used

| Component | Description |
|----------|-------------|
| ESP32 Dev Board | Central IoT controller |
| DHT11 Sensor | Temperature and humidity sensing |
| LDR (Digital) | Detects light exposure indicating container opening |
| GPS Module (NEO-6M) | Captures latitude and longitude of the shipment |

---

## 🔁 Data Workflow

1. ESP32 collects sensor data every 2.5 seconds
2. Data is structured into JSON:
```json
{
  "temperature": 24.5,
  "humidity": 68,
  "light": 1,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": 1746499505
}
```
3. Sent via MQTT over TLS to HiveMQ Cloud
4. Python script subscribes to MQTT topic and inserts data into **InfluxDB**
5. Grafana visualizes real-time environmental data

---

## 🛠️ Software Stack

| Layer | Tools/Tech |
|-------|------------|
| Microcontroller | ESP32 + Arduino IDE |
| Messaging | MQTT (HiveMQ Cloud Broker) |
| Cloud & Storage | InfluxDB (local or cloud) |
| Visualization | Grafana |
| Backend Script | Python + Paho MQTT Client |
| Optional | Telegraf (MQTT to InfluxDB bridge) |


## 🚀 Getting Started

### ESP32 Code
- Upload `cold_chain_sensor_copy_20250508220111.ino` to your ESP32 via Arduino IDE
- Ensure libraries:
  - `DHT`, `TinyGPSPlus`, `WiFi`, `PubSubClient`

### Python MQTT Subscriber
```bash
pip install paho-mqtt influxdb
python mqtt_influx_connection.py
```

---

## 🔐 MQTT Broker Setup

- Broker: `HiveMQ Cloud`
- Port: `8883`
- Use TLS connection with username and password authentication
- Topic: `cold_chain_data`

---

## 📽️ Project Video

▶️ **Unlisted YouTube Demo**: [Watch the presentation](https://www.youtube.com/watch?v=HS00AN6d8OA)

---

## 👥 Contributors

- [Akhil Kumar Puri] – Sensor Integration & Microcontroller Code, Presentation
- [Abhinav Rao Veeramalla] – Cloud Integration, Python & Grafana, Testing, Debugging,

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
