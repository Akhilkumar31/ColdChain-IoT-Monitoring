import csv
import random
import time
from faker import Faker

fake = Faker()

with open('simulated_dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'Light', 'Latitude', 'Longitude', 'Status'])
    for _ in range(1000):
        timestamp = int(time.time())
        temperature = round(random.uniform(2.0, 8.0), 2)
        humidity = round(random.uniform(30.0, 50.0), 2)
        light = random.randint(0, 1023)
        latitude = fake.latitude()
        longitude = fake.longitude()
        status = 'OK' if temperature < 7 else 'ALERT'
        writer.writerow([timestamp, temperature, humidity, light, latitude, longitude, status])
        time.sleep(0.1)
