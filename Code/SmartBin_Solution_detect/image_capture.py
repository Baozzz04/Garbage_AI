import numpy as np
import RPi.GPIO as GPIO
import cv2
import time

def str_format(number):
    if (number < 10):
        return '000' + str(number)
    elif (number < 100):
        return '00' + str(number)
    elif (number < 1000):
        return '0' + str(number)
    else:
        return str(number)

cap = cv2.VideoCapture(0)
BTN1 = 36

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(BTN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

image_idx = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame = frame[150:, 150:-50]

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Display the resulting fram
    if GPIO.input(BTN1) == GPIO.LOW:
        image_idx += 1
        print("Image " + str(image_idx) + " captured.")
        cv2.imwrite('images/IMG_' + str_format(image_idx) + '.jpg', frame)
        time.sleep(0.25)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()