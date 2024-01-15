import pigpio as GPIO
from time import sleep


servoPin1 = 13
servoPin2 = 19
servoPin3 = 12
servoPin4 = 18


p = GPIO.pi()
p.set_PWM_frequency(servoPin1, 50)
p.set_PWM_range(servoPin1, 20000)
p.set_PWM_dutycycle(servoPin1, 0)

p.set_PWM_frequency(servoPin2, 50)
p.set_PWM_range(servoPin2, 20000)
p.set_PWM_dutycycle(servoPin2, 0)

p.set_PWM_frequency(servoPin3, 50)
p.set_PWM_range(servoPin3, 20000)
p.set_PWM_dutycycle(servoPin3, 0)

p.set_PWM_frequency(servoPin4, 50)
p.set_PWM_range(servoPin4, 20000)
p.set_PWM_dutycycle(servoPin4, 0)


def set_servo(pin, arg):
    value = 850 + int(arg)*10
    p.set_PWM_dutycycle(pin, value)

def set_4_servos(arg1, arg2, arg3, arg4):
    global servoPin1, servoPin2, servoPin3, servoPin4
    set_servo(servoPin1, arg1)
    set_servo(servoPin2, arg2)
    set_servo(servoPin3, arg3)
    set_servo(servoPin4, arg4)

def free_servos():
    p.set_PWM_dutycycle(servoPin1, 0)
    p.set_PWM_dutycycle(servoPin2, 0)
    p.set_PWM_dutycycle(servoPin3, 0)
    p.set_PWM_dutycycle(servoPin4, 0)

while 1:
    set_4_servos(90, 90, 90, 90)
    sleep(3)
    free_servos()
    set_4_servos(113, 120, 140, 95)
    sleep(3)
    free_servos()
    sleep(1)
free_servos()
p.stop()
print('end')