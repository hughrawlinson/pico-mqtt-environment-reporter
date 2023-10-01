# mip install hts221
# mip install umqtt.simple

import json
import secrets
import time

import machine
import network
from hts221 import HTS221
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PW)
print("Connecting")
while not wlan.isconnected():
    pass
print("Connected to WLAN")


def i2c_scan():
    sda = machine.Pin(8)
    scl = machine.Pin(9)
    i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

    devices = i2c.scan()

    if len(devices) == 0:
        return "No i2c device !"
    else:
        dev = [hex(device) for device in devices]
        print(dev)
        return dev

def get_env():
    sda = machine.Pin(secrets.I2C_SDA_PIN)
    scl = machine.Pin(secrets.I2C_SCL_PIN)
    i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

    sensor = HTS221(i2c)
    time.sleep_ms(10)
    return {
        "temperature": sensor.temperature(),
        "humidity": sensor.humidity()
    }


def mqtt_connect():
    client = MQTTClient(
        secrets.MQTT_CLIENT_ID,
        secrets.MQTT_HOST,
        keepalive=3600,
        user=secrets.MQTT_USER,
        password=secrets.MQTT_PASS,
    )
    client.connect()
    client.publish("office/environment/available", "online", retain=True)
    while True:
        time.sleep_ms(5000)
        try:
            result = json.dumps(i2c_scan())
            print(result)
            client.publish(secrets.MQTT_TOPIC, json.dumps(result), retain=True)
        except OSError as e:
            print(e)
            raise e


while True:
    try:
        mqtt_connect()
    except Exception as e:
        print(e)
