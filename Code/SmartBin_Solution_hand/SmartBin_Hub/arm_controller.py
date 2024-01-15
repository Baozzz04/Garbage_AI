import pigpio
from time import sleep
import math

from config import *

class ArmController:
    
    def __init__(self):
        self.pi = pigpio.pi()
        
        self.servoPos = {}
        self.servoPos[str(SERVO1)] = 0
        self.servoPos[str(SERVO2)] = 0
        self.servoPos[str(SERVO3)] = 0
        self.servoPos[str(SERVO4)] = 0
        
        self.originState(False)
        
    def pulse2Angle(self, pulse):
        return -0.1 * pulse + 240
    
    def angle2Pulse(self, angle):
        return round(-10 * angle + 2400)
        
    def moveArmTo(self, a, b):
        a -= 85
        b -= 80

        servo1Angle = 2 * (math.atan2(270*a - math.sqrt(-pow(a, 4) - 2*pow(a, 2)*pow(b, 2) + 79668*pow(a, 2) - pow(b, 4) +79668 * pow(b, 2) - 11451456), pow(a, 2) + pow(b, 2) + 270 * b - 3384));
        servo2Angle = 2 * (math.atan2(294*b - math.sqrt(-pow(a, 4) - 2*pow(a, 2)*pow(b, 2) + 79668*pow(a, 2) - pow(b, 4) +79668 * pow(b, 2) - 11451456), pow(a, 2) + pow(b, 2) + 294 * a + 3384));
        servo1Angle = self.pulse2Angle(844) - servo1Angle / math.pi * 180;
        servo2Angle = self.pulse2Angle(1765) - servo2Angle / math.pi * 180;
        
        self._setGpio(SERVO3, self.angle2Pulse(servo2Angle), step=20)
        self._setGpio(SERVO2, self.angle2Pulse(servo1Angle), step=20)
        
            
    def pick(self, id, rect):
        distance = -333.333 * (rect['x1'] + rect['x2']) / 2 + 396.666
        if distance < 18:
            return
        
        a = distance - 85
        b = 30 - 80
        
        if -pow(a, 4) - 2*pow(a, 2)*pow(b, 2) + 79668*pow(a, 2) - pow(b, 4) +79668 * pow(b, 2) - 11451456 < 0:
            return
        
        self._setGpio(SERVO1, 2400, step=20)
        self._setGpio(SERVO4, 2000, False)
        self._setGpio(SERVO2, 800, step=20)
        self._setGpio(SERVO3, 1100, step=20)
        self._setGpio(SERVO2, 1100, step=20)
        self._setGpio(SERVO3, 770, step=20)
        self._setGpio(SERVO2, 1300, step=20)

        sleep(0.25)
        self.moveArmTo(distance, 30)
        
        sleep(0.5)
        self._setGpio(SERVO4, 800, False, release=False)
        
        sleep(0.5)
        self._setGpio(SERVO2, 700, step=20)
        self._setGpio(SERVO3, 1750, step=20)
        
            
    def originState(self, smooth = True):
        self._setGpio(SERVO4, 900, smooth, step=20)
        self._setGpio(SERVO2, 600, smooth, step=20)
        self._setGpio(SERVO3, 1500, smooth, step=20)
        self._setGpio(SERVO1, 1500, smooth, step=20)
        
        
    def moveToTrashBin1(self):
        self._setGpio(SERVO1, 500, step=20)
        self._setGpio(SERVO3, 1500)
        self._setGpio(SERVO2, 900)
        sleep(0.5)
        self._setGpio(SERVO4, 1500, False)
        sleep(0.2)
        self._setGpio(SERVO4, 900, False)
            
    def moveToTrashBin2(self):
        self._setGpio(SERVO1, 950, step=20)
        self._setGpio(SERVO3, 1600)
        self._setGpio(SERVO2, 900)
        sleep(0.5)
        self._setGpio(SERVO4, 1500, False)
        sleep(0.2)
        self._setGpio(SERVO4, 900, False)
        
    def moveToTrashBin3(self):
        self._setGpio(SERVO1, 1300, step=20)
        self._setGpio(SERVO3, 1700)
        self._setGpio(SERVO2, 1100)
        sleep(0.5)
        self._setGpio(SERVO4, 1500, False)
        sleep(0.2)
        self._setGpio(SERVO4, 900, False)
        
        
    def _setGpio(self, pin, pulse_width, smooth = True, step = 10, release = True):
        if pulse_width < 500 or pulse_width > 2500:
            return
        if smooth:
            pulse = self.servoPos[str(pin)]
            if pulse < pulse_width:
                while pulse < pulse_width:
                    pulse = pulse + step
                    self.pi.set_servo_pulsewidth(pin, pulse)
                    sleep(0.02)
            else:
                while pulse > pulse_width:
                    pulse = pulse - step
                    self.pi.set_servo_pulsewidth(pin, pulse)
                    sleep(0.02)

            self.pi.set_servo_pulsewidth(pin, pulse_width)
            sleep(0.02)
            
            self.servoPos[str(pin)] = pulse_width
            if release:
                self.pi.set_servo_pulsewidth(pin, 0)
            
        else:
            self.pi.set_servo_pulsewidth(pin, pulse_width)
            sleep_time = abs(self.servoPos[str(pin)] - pulse_width) / 1000 * 1.0
            sleep(sleep_time)
            self.servoPos[str(pin)] = pulse_width
            
            if release:
                self.pi.set_servo_pulsewidth(pin, 0)