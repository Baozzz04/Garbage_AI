import cv2
import numpy as np

from config import *

from object_detector import ObjectDetect
from mqtt_service import MqttService
from lcd import PCD8544

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import json

from utils import visualization_utils as vis_util

robot_status = 'ready'

def on_mqtt_message(client, userdata, message):
    global robot_status
    status = str(message.payload.decode("utf-8"))
    robot_status = status

if __name__ == '__main__':
    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX

    object_detector = ObjectDetect()
    mqtt = MqttService()
    lcd = PCD8544()

    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 1
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        t1 = cv2.getTickCount()
        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)

        frame = frame[150:, 150:-50]
        
        (boxes, scores, classes, num) = object_detector.detect(frame)
        
        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            object_detector.category_index,
            use_normalized_coordinates=True,
            line_thickness=3,
            min_score_thresh=0.70)

        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        
        # xu ly du lieu sau khi detect duoc 
        if len(classes[0]) > 0:
            if scores[0][0] > 0.5:
                data = {
                    'id': int(classes[0][0]),
                    'rect': {
                        'x1': float(boxes[0][0][1]),
                        'y1': float(boxes[0][0][0]),
                        'x2': float(boxes[0][0][3]),
                        'y2': float(boxes[0][0][2])
                    }
                }

                if int(classes[0][0]) == 1:
                    lcd.draw_text("Bottle", (30, 20))    
                elif int(classes[0][0]) == 2:
                    lcd.draw_text("Nylon", (30, 20)) 
                else:
                    lcd.draw_text("Scrap Paper", (10, 20))   
                check = True
                for i in range(5):
                    if scores[0][i] > 0.5 and int(classes[0][0]) == 4:
                        check = False
                        break
                if check:
                    mqtt.publish(OBJECT_DETECT_TOPIC, json.dumps(data)) 

            else:
                lcd.draw_text(" ", (10, 20))  
                data = {
                    'id': 0
                }

                mqtt.publish(OBJECT_DETECT_TOPIC, json.dumps(data))                

        # All the results have been drawn on the frame, so it's time to display
        cv2.imshow('Object detector', frame)
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        
        rawCapture.truncate(0)
        
    camera.close()

    cv2.destroyAllWindows()