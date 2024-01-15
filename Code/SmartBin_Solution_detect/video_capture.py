import numpy as np
import RPi.GPIO as GPIO
import cv2

cap = cv2.VideoCapture(0)
BTN1 = 36

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(BTN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start = False

# Define the codec and create VideoWriter objectX264
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    #frame = frame[150:, 150:-50]
    if ret==True:

        # write the flipped frame
        if start:
            out.write(frame)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
    if GPIO.input(BTN1) == GPIO.LOW:
        start = True
        print("Capuring")

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()