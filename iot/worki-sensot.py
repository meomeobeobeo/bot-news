from machine import Pin , PWM
import network
import time
from umqtt.simple import MQTTClient
import ujson
import dht

# Device setup
DEVICE_ID = "wokwi001"

# WiFi setup
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# MQTT setup
MQTT_BROKER = 'a3c184df230e474d8fe284f800b9c429.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
CLIENT_ID = DEVICE_ID
MQTT_USER = 'law'
MQTT_PASSWORD = 'law30102001'

# Topics
MQTT_TELEMETRY_TOPIC = "iot/telemetry"
MQTT_CONTROL_TOPIC = "iot/control"
MQTT_NOTIFY_TOPIC = "iot/notify"

# DHT Sensor Setup
DHT_PIN = Pin(15)
dht_sensor = dht.DHT22(DHT_PIN)

# LED/LAMP Setup
RED_LED = Pin(12, Pin.OUT)
BLUE_LED = Pin(13, Pin.OUT)
FLASH_LED = Pin(2, Pin.OUT)
RED_LED.on()
BLUE_LED.on()



# Constants
FREQUENCY = 1000  # Frequency of the tone in Hz
BUZZER_PIN = 21
LED_PIN = 27



# Initialize tone pin as PWM
BUZZER = PWM(Pin(BUZZER_PIN), freq=FREQUENCY)
BUZZER.duty(0)



def runBuzzer():
    BUZZER.duty(512)  # Set duty cycle to 50% (range: 0-1023)
    time.sleep(1)  # Tone duration
        
        # Stop tone
    BUZZER.duty(0)  # Set duty cycle to 0 to stop tone
    time.sleep(1)  # Pause duration
        
        # Toggle LED
    RED_LED.on()  # Turn on the LED 
    time.sleep(1)  # Keep the LED on for a second
    RED_LED.off()  # Turn off the LED




# Method for handling received messages
def did_receive_callback(topic, message):
    print("\n\nDATA RECEIVED!...\ntopic = {0} , message = {1}".format(topic.decode(), message.decode()))

# Connect to WiFi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        time.sleep(1)
    
    print('WiFi connected:', wlan.ifconfig())

# Connect to MQTT Broker
def connect_mqtt():
    client = MQTTClient(
        client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        ssl=True,
        ssl_params={'server_hostname': MQTT_BROKER}
    )
    
    try:
        client.connect()
        print('Connected to MQTT broker')
    except Exception as e:
        print('Failed to connect to MQTT broker:', e)
        return None
    
    return client

# Create JSON data with temperature and humidity
def create_dht_json_sensor_data(temperature, humidity):
    data = {
        'temperature': temperature,
        'humidity': humidity
    }
    json_data = ujson.dumps(data)
    return json_data

# Publish data to MQTT broker
def publish_data(client, topic, temperature, humidity):
    json_data = create_dht_json_sensor_data(temperature, humidity)
    client.publish(topic, json_data)
    print('Published data:', json_data)

def publish_notify(client , topic , message):
    json_data = ujson.dumps({
        'message' : message,
        'code' : 400
        
    })

    client.publish(topic , json_data)
    print("Publish data with topic:::  " + topic + ":::::" )

def devide_control(message , topic):
    dic_message = ujson.loads(message)
    print(dic_message['code'])
    code = dic_message['code']
    # code 302 turn on fuacet
    # code 200 turn on blue_led
    # code 201 turn off blue_led
    if code == 200:
        BLUE_LED.on()
    elif code == 201:
        BLUE_LED.off()
    else :
        print("Unknown command")





# Subscribe to a topic and print received data
def on_message(topic, msg):
    print('Received message:', msg.decode(), 'from topic:', topic.decode())
    if topic.decode() == MQTT_CONTROL_TOPIC:
       devide_control(msg.decode() , topic.decode())



def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    client = connect_mqtt()
    
    if client:
        # Set callback for received messages
        client.set_callback(on_message)
        client.subscribe(MQTT_CONTROL_TOPIC)
        
        # Initialize previous temperature and humidity
        prev_temperature = None
        prev_humidity = None
        
        try:
             while True:
                dht_sensor.measure()
                temperature = dht_sensor.temperature()
                humidity = dht_sensor.humidity()
                
                # Check if temperature or humidity has changed
                if temperature != prev_temperature or humidity != prev_humidity:
                    publish_data(client, MQTT_TELEMETRY_TOPIC, temperature, humidity)
                    prev_temperature = temperature
                    prev_humidity = humidity
                
                # Check if temperature exceeds threshold
                if temperature > 60:
                    runBuzzer()
                    publish_notify(client , MQTT_NOTIFY_TOPIC , "High temperatures pose a risk of fire")
                
                client.check_msg()
                time.sleep(2)  # Adjust the delay as needed
                
        except KeyboardInterrupt:
            print('Interrupted')
        finally:
            client.disconnect()
            print('Disconnected from MQTT broker')
    else:
        print('MQTT client connection failed')

# Run the main function
if __name__ == '__main__':
    main()
