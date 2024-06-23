# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


# Define the MQTT settings
MQTT_BROKER = 'a3c184df230e474d8fe284f800b9c429.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
CLIENT_ID = 'bot_server'  # Replace 'your_device_id' with your actual DEVICE_ID
MQTT_USER = 'law'
MQTT_PASSWORD = 'law30102001'

# Topics
MQTT_TELEMETRY_TOPIC = "iot/telemetry"
MQTT_CONTROL_TOPIC = "iot/control"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe(MQTT_TELEMETRY_TOPIC)
        else:
            print(f"Connect failed with code {rc}")

    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT , 60)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(MQTT_TELEMETRY_TOPIC, "Hello hihihihi")
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{MQTT_TELEMETRY_TOPIC}`")
        else:
            print(f"Failed to send message to topic {MQTT_TELEMETRY_TOPIC}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
