import json
import time
import threading

import RPi.GPIO as GPIO

from mqtt_service import MqttService
from nrf24l01 import NRF24L01
from arm_controller import ArmController

from config import *

rf24 = NRF24L01()
mqtt = MqttService()
arm = ArmController()

robot = False

trashbin = False

def button_press():
    global trashbin
    trashbin = not trashbin
    if trashbin:
        for _ in range(3):
            rf24.write(b'11')
            rf24.write(b'21')
            rf24.write(b'31')
            time.sleep(0.1)
    else:
        for _ in range(3):
            rf24.write(b'10')
            rf24.write(b'20')
            rf24.write(b'30')
            time.sleep(0.1)

def control_arm(data):
    global robot
    
    robot = True
    for _ in range(3):
        rf24.write(bytes(str(data['id']), 'utf8') + b'1')
        time.sleep(0.1)
        
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
    
    for _ in range(3):
        rf24.write(bytes(str(data['id']), 'utf8') + b'0')
        time.sleep(0.1)
        
    robot = False

def on_mqtt_message(client, userdata, message):    
    json_str = str(message.payload.decode("utf-8"))
    data = json.loads(json_str)
    
    print(data)
    
    if robot == False:
        thread = threading.Thread(target=control_arm, args=(data,))
        thread.start()
    
if __name__ == '__main__':
    mqtt.subscribe(on_mqtt_message)
    
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    
    mqtt.client.loop_start()

    while True:
        if GPIO.input(BTN) == GPIO.LOW:
            button_press()
            time.sleep(0.25)
        
    
    
    