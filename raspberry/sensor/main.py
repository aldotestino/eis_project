import requests
import schedule
import time
import Adafruit_DHT
from bmpsensor import BMP180
from datetime import datetime

ALTITUDE = 232

DHT11_PIN = 17
API_URL = "http://localhost:8080/api/data"

bmp180 = BMP180(0x77)

temperatures = []
humidities = []
pressures = []

def pressure_to_sealevel(pressure, altitutde):
    return pressure / pow(1 - (altitutde / 44330.0), 5.255)

def measure():
    global temperatures
    global humidities
    global pressures
    dt = datetime.now().isoformat()[:-3]+'Z'
    humidity, temperature, pressure = None, None, None
    while humidity is None or temperature is None:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_PIN, retries=2, delay_seconds=1)
    while pressure is None:
        pressure = round(pressure_to_sealevel(bmp180.get_pressure(), ALTITUDE) / 100, 1)
    print(f"{dt}: {temperature}°C, {humidity}%, {pressure}hPA")
    temperatures.append(temperature)
    humidities.append(humidity)
    pressures.append(pressure)


def save_data():
    global temperatures
    global humidities
    global pressures
    dt = datetime.now().isoformat()[:-3]+'Z'
    result = requests.post(API_URL, json={
        "timestamp": dt,
        "temperature": sum(temperatures) / len(temperatures),
        "humidity": sum(humidities) / len(humidities),
        "pressure": sum(pressures) / len(pressures)
    })
    temperatures = []
    humidities = []
    if result.status_code == 201:
        print(f"Record created: {result.json()}")

measure()

schedule.every(5).minutes.do(measure)
schedule.every().hour.at(":00").do(save_data)

while True:
    schedule.run_pending()
    time.sleep(1)