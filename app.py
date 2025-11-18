import json
import time
import paho.mqtt.client as mqtt
import threading

id = '9e9e2074-64b1-4dd2-8ee3-ad2ab0359a77'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/command'
client_name = id + 'soil_moisture_sensor_server'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

water_time = 5
wait_time = 20

def send_relay_command(client, state):
    command = {'relay_on': state}
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
    mqtt_client.unsubscribe(client_telemetry_topic)
    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)
    time.sleep(wait_time)
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    if payload['soil_moisture'] > 486:
        threading.Thread(target=control_relay, args=(client,)).start()

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
