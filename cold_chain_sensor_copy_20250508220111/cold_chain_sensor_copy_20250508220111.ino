#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <TinyGPSPlus.h>
#include <HardwareSerial.h>
#include <time.h>

// -------------------- WiFi Credentials --------------------
const char* ssid = "Suddhalagudi";
const char* password = "wifikavala";

// -------------------- MQTT Broker (HiveMQ Cloud) --------------------
const char* mqtt_server = "709f4a6d34fb4b1c96197e61530f885c.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "Akhil";
const char* mqtt_pass = "Akhil@2001";
const char* mqtt_topic = "cold_chain_data";

// -------------------- Pin Definitions --------------------
#define DHTPIN 4
#define DHTTYPE DHT11
#define LDRPIN 2               // DO pin from LDR → GPIO2 (D2)
#define RXPin 15               // GPS TX → ESP32 RX (D15)
#define TXPin 13               // GPS RX ← ESP32 TX (D13)

// -------------------- Sensor & MQTT Objects --------------------
DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial gpsSerial(2); // UART2 for GPS
WiFiClientSecure espClient;
PubSubClient client(espClient);

// -------------------- Setup --------------------
void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, RXPin, TXPin);
  dht.begin();
  pinMode(LDRPIN, INPUT);  // Set LDR digital pin

  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");

  // Sync time for TLS validation
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("⏳ Syncing time");
  while (time(nullptr) < 100000) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" ✅ Time synced");

  // Setup secure connection
  espClient.setInsecure(); // WARNING: For testing only; use certs in production
  client.setServer(mqtt_server, mqtt_port);
  client.setBufferSize(1024); // For large payloads

  reconnect();
}

// -------------------- MQTT Reconnect --------------------
void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_pass)) {
      Serial.println("✅ MQTT connected");
    } else {
      Serial.print("❌ failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// -------------------- Main Loop --------------------
void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  // Read DHT11
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("⚠️ Failed to read from DHT sensor");
    return;
  }

  // Read LDR (digital)
  int light = digitalRead(LDRPIN);
  Serial.print("🌞 LDR Digital Value: ");
  Serial.println(light);  // Expect 0 = bright, 1 = dark

  // Read GPS
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }
  float latitude = gps.location.isValid() ? gps.location.lat() : 0.0;
  float longitude = gps.location.isValid() ? gps.location.lng() : 0.0;

  // Build JSON payload
  String payload = "{";
  payload += "\"temperature\":" + String(temperature, 2) + ",";
  payload += "\"humidity\":" + String(humidity, 2) + ",";
  payload += "\"light\":" + String(light) + ",";
  payload += "\"latitude\":" + String(latitude, 6) + ",";
  payload += "\"longitude\":" + String(longitude, 6) + ",";
  payload += "\"timestamp\":" + String((int)time(nullptr));
  payload += "}";

  // Publish to MQTT
  Serial.println("📤 Publishing: " + payload);
  client.publish(mqtt_topic, payload.c_str());

  delay(2500); // ⏱️ Reduced interval: 2.5 seconds
}
