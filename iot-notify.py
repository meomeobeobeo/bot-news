import logging
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from getnews import getNewsVNEXPRESS, getNewsDANTRI
import paho.mqtt.client as mqtt
import time
import requests
import json


base_url = 'https://api.telegram.org/bot7267663893:AAF3MHBcO77P4MiUpjRFtHDZdFhBONTmfIg/sendMessage?chat_id=-4205017972&text='






# Define the MQTT settings
MQTT_BROKER = 'a3c184df230e474d8fe284f800b9c429.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
CLIENT_ID = 'bot_server'  # Replace 'your_device_id' with your actual DEVICE_ID
MQTT_USER = 'law'
MQTT_PASSWORD = 'law30102001'

# Topics
MQTT_TELEMETRY_TOPIC = "iot/telemetry"
MQTT_CONTROL_TOPIC = "iot/control"
MQTT_NOTIFY_TOPIC = "iot/notify"

# TELEGRAM CHAT ID
TELEGRAM_CHAT_ID = '4205017972'


# Configure logging to save errors to a file with timestamp
logging.basicConfig(
    filename='log.txt',
    level=logging.ERROR
)

# Create a custom logging formatter to include the timestamp
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create a FileHandler with the custom formatter
file_handler = logging.FileHandler('log.txt')
file_handler.setFormatter(formatter)

# Add the FileHandler to the root logger
logging.getLogger().addHandler(file_handler)

# Telegram bot command handler
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(f'Xin chào {update.effective_user.first_name}')
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")
        
 
async def turnon_faucet(update: Update, context: ContextTypes.DEFAULT_TYPE , client ) -> None:
    try:
        client.publish(MQTT_CONTROL_TOPIC, json.dumps({'message': 'turn_on_faucet' , 'code' : 302 }))
        
        await update.message.reply_text(f'Bật vòi nước thành công')
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")

async def turnon_blue_led(update: Update, context: ContextTypes.DEFAULT_TYPE , client ) -> None:
    try:
        client.publish(MQTT_CONTROL_TOPIC, json.dumps({'message': 'turn_on_blue_led' , 'code' : 200 }))
        
        await update.message.reply_text(f'Bật led xanh thành công')
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")
        
async def turnoff_blue_led(update: Update, context: ContextTypes.DEFAULT_TYPE , client ) -> None:
    try:
        client.publish(MQTT_CONTROL_TOPIC, json.dumps({'message': 'turn_off_blue_led' , 'code' : 201 }))
        
        await update.message.reply_text(f'Tắt led xanh thành công')
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")

def check_topic_message(topic, message):
    if topic == MQTT_NOTIFY_TOPIC:
        print("notify hihihihihihi:::::::::::::::")
        print(f"Received notification: {message}")
        dict_message = json.loads(message)
        print(dict_message)
        requests.get(base_url + dict_message['message'])
        
    elif topic == MQTT_TELEMETRY_TOPIC:
        print(f"Received telemetry: {message}")
    elif topic == MQTT_CONTROL_TOPIC:
        print(f"Received control: {message}")
    else:
        print(f"Received message: {message} on topic: {topic}")

# MQTT connection setup
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            client.subscribe(MQTT_NOTIFY_TOPIC)  # Subscribe to the topic on successful connection
            client.subscribe(MQTT_TELEMETRY_TOPIC)  # Subscribe to the topic on successful connection
            
        else:
            print(f"Connect failed with code {rc}")

    def on_message(client, userdata, msg):
        # print(f"Received message: {msg.topic} {msg.payload.decode()}")
        check_topic_message(msg.topic, msg.payload.decode())

    def on_publish(client, userdata, mid):
        print(f"Message published with mid: {mid}")

    def on_subscribe(client, userdata, mid, granted_qos):
        print(f"Subscribed with mid: {mid} and QoS: {granted_qos}")

    try:
        # Create an MQTT client instance
        client = mqtt.Client(CLIENT_ID)

        # Set the username and password
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        # Configure TLS/SSL
        client.tls_set()

        # Assign the callback functions
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_publish = on_publish
        client.on_subscribe = on_subscribe

        # Connect to the broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)

        # Start the MQTT client loop to process network traffic and dispatch callbacks
        client.loop_start()

        print("MQTT client setup and connection successful")
        return client

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# Main function
def main():
    # Connect to MQTT broker
    client = connect_mqtt()

    # Create Telegram bot application
    app = ApplicationBuilder().token("7267663893:AAF3MHBcO77P4MiUpjRFtHDZdFhBONTmfIg").build()
    
    # Add command handler for /hello command
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("faucet_on", lambda update, context: turnon_faucet(client=client, update=update, context=context)))
    app.add_handler(CommandHandler("blueled_on", lambda update, context: turnon_blue_led(client=client, update=update, context=context)))
    app.add_handler(CommandHandler("blueled_off", lambda update, context: turnoff_blue_led(client=client, update=update, context=context)))
    
    
    

    if client is not None:
        # Publish a message to the telemetry topic
        client.publish(MQTT_TELEMETRY_TOPIC, "Hello from MQTT telemetry")

    # Start the Telegram bot polling
    app.run_polling()

    # Ensure MQTT client continues running
    while True:
        time.sleep(1)

# Call main function
if __name__ == '__main__':
    main()
