import json
import time
import threading

from mqtt_service import MqttService
from nrf24l01 import NRF24L01
from arm_controller import ArmController

from config import *

rf24 = NRF24L01()
mqtt = MqttService()
arm = ArmController()

robot_status = 0

def control_arm(data):
    global robot_status
    
    robot_status = 1
    
    rf24.write(bytes(str(data['id']), 'utf8') + b'1')
    if data['id'] == 1:
        arm.pick(data['id'], data['rect'])
        arm.moveToTrashBin1()
    elif data['id'] == 2:
        arm.pick(data['id'], data['rect'])
        arm.moveToTrashBin2()
    elif data['id'] == 3:
        arm.pick(data['id'], data['rect'])
        arm.moveToTrashBin3()
     
    time.sleep(0.5)
    
    arm.originState()
    
    rf24.write(bytes(str(data['id']), 'utf8') + b'0')
    
    robot_status = 0

def on_mqtt_message(client, userdata, message):    
    json_str = str(message.payload.decode("utf-8"))
    data = json.loads(json_str)
    
    print(data)
    
    if robot_status == 0:
        thread = threading.Thread(target=control_arm, args=(data,))
        thread.start()
    
if __name__ == '__main__':
    mqtt.subscribe(on_mqtt_message)
    
    mqtt.client.loop_forever()
    
    
    