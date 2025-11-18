from counterfit_connection import CounterFitConnection
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5001)
adc = ADC()
relay = GroveRelay(66)

id = '9e9e2074-64b1-4dd2-8ee3-ad2ab0359a77'
client_name = id + 'soil_moisture_sensor_client'
client_telemetry_topic = id + '/telemetry'


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

while True:
    soil_moisture = adc.read(65)
    print("Soil moisture:", soil_moisture)
    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    time.sleep(10)
    if soil_moisture > 486:
        print("Soil Moisture is too low, turning relay on.")
        relay.on()
    else:
        print("Soil Moisture is ok, turning relay off.")
        relay.off()