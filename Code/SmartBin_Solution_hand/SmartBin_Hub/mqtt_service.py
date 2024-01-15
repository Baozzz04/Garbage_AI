import paho.mqtt.client as mqtt
from config import *

class MqttService:

    def __init__(self):
        self.client = mqtt.Client("P")
        self.client.connect(BROCKER_ADDRESS)

    def subscribe(self, func):
        self.client.subscribe(OBJECT_DETECT_TOPIC)
        self.client.on_message = func
        
    def publish(self, topic, data):
        self.client.publish(topic, data)
