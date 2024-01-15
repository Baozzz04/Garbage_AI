# sudo pigpiod
import pigpio as GPIO
from guizero import App, Slider, TextBox, Text, PushButton

p = GPIO.pi()
servoPin1 = 13
servoPin2 = 19
servoPin3 = 12
servoPin4 = 18

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

s1 = 0
s2 = 0
s3 = 0
s4 = 0

def slider_changed1(slider_value):
    global s1
    s1 = slider_value
def slider_changed2(slider_value):
    global s2
    s2 = slider_value
def slider_changed3(slider_value):
    global s3
    s3 = slider_value
def slider_changed4(slider_value):
    global s4
    s4 = slider_value

def set_servo1():
    value = 850 + int(s1)*10;
    p.set_PWM_dutycycle(servoPin1, value)
def set_servo2():
    value = 850 + int(s2)*10;
    p.set_PWM_dutycycle(servoPin2, value)
def set_servo3():
    value = 850 + int(s3)*10;
    p.set_PWM_dutycycle(servoPin3, value)
def set_servo4():
    value = 850 + int(s4)*10;
    p.set_PWM_dutycycle(servoPin4, value)

def increase_s1():
    global s1
    s1 = int(s1)+1
    if s1 > 180 : s1 = 180
    slider1.value = str(s1)
    set_servo1()
def increase_s2():
    global s2
    s2 = int(s2)+1
    if s2 > 180 : s2 = 180
    slider2.value = str(s2)
    set_servo2()
def increase_s3():
    global s3
    s3 = int(s3)+1
    if s3 > 180 : s3 = 180
    slider3.value = str(s3)
    set_servo3()
def increase_s4():
    global s4
    s4 = int(s4)+1
    if s4 > 180 : s4 = 180
    slider4.value = str(s4)
    set_servo4()

def decrease_s1():
    global s1
    s1 = int(s1)-1
    if s1 < 0 : s1 = 0
    slider1.value = str(s1)
    set_servo1()
def decrease_s2():
    global s2
    s2 = int(s2)-1
    if s2 < 0 : s2 = 0
    slider2.value = str(s2)
    set_servo2()
def decrease_s3():
    global s3
    s3 = int(s3)-1
    if s3 < 0 : s3 = 0
    slider3.value = str(s3)
    set_servo3()
def decrease_s4():
    global s4
    s4 = int(s4)-1
    if s4 < 0 : s4 = 0
    slider4.value = str(s4)
    set_servo4()

def resetFunc():
    global s1, s2, s3, s4
    s1 = 90
    slider1.value = str(s1)
    set_servo1()
    s2 = 90
    slider2.value = str(s2)
    set_servo2()
    s3 = 90
    slider3.value = str(s3)
    set_servo3()
    s4 = 90
    slider4.value = str(s4)
    set_servo4()

app = App(layout ="grid", width=500, height=350)

text1 = Text(app, "Servo 1", grid = [0, 0])
increase1 = PushButton(app, command = increase_s1, text="+", grid=[2, 1])
slider1 = Slider(app, command=slider_changed1, width = 360,start= 0, end =180, grid=[1,1])
decrease1 = PushButton(app, command = decrease_s1, text="-", grid=[0, 1])

text2 = Text(app, "Servo 2", grid = [0, 2])
increase2 = PushButton(app, command = increase_s2, text="+", grid=[2, 3])
slider2 = Slider(app, command=slider_changed2, width = 360,start= 0, end =180, grid=[1,3])
decrease2 = PushButton(app, command = decrease_s2, text="-", grid=[0, 3])

text3 = Text(app, "Servo 3", grid = [0, 4])
increase3 = PushButton(app, command = increase_s3, text="+", grid=[2, 5])
slider3 = Slider(app, command=slider_changed3, width = 360,start= 0, end =180, grid=[1,5])
decrease3 = PushButton(app, command = decrease_s3, text="-", grid=[0, 5])

text4 = Text(app, "Servo 4", grid = [0, 6])
increase4 = PushButton(app, command = increase_s4, text="+", grid=[2, 7])
slider4 = Slider(app, command=slider_changed4, width = 360,start= 0, end =180, grid=[1,7])
decrease4 = PushButton(app, command = decrease_s4, text="-", grid=[0, 7])

slider1.when_left_button_released = set_servo1
slider2.when_left_button_released = set_servo2
slider3.when_left_button_released = set_servo3
slider4.when_left_button_released = set_servo4

reset = PushButton(app, command= resetFunc, text="Reset", grid=[1, 8])

def endProgram():
    p.set_PWM_dutycycle(servoPin1, 0)
    p.set_PWM_dutycycle(servoPin2, 0)
    p.set_PWM_dutycycle(servoPin3, 0)
    p.set_PWM_dutycycle(servoPin4, 0)
    p.stop()
    
app.on_close(endProgram())

app.display()