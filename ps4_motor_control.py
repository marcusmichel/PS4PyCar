import RPi.GPIO as GPIO
from time import sleep
from pyPS4Controller.controller import Controller

# Pins for Motor Driver Inputs 
Motor1A = 24
Motor1B = 23
Motor1E = 25
pin = 12
 
GPIO.setmode(GPIO.BCM)

def setup():
    GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

def loop():
    # Going forwards
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    sleep(5)
    # Going backwards
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
 
    sleep(5)
    # Stop
    GPIO.output(Motor1E,GPIO.LOW)

    destroy()
    
def forwards():
    # Going forwards
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
def backwards():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)  
    
def stop():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
def turn():
    GPIO.PWM(PWM0,50).ChangeDutyCycle(90)
        
def turn_back():
    GPIO.PWM(PWM0,50).ChangeDutyCycle(duty)
    sleep(1)
    duty = duty - 2

def destroy():  
    GPIO.cleanup()

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        
    def on_x_press(self):
       # Going forwards
        forwards()
        print("forwards")

    def on_x_release(self):
        stop()
        print("stop")
    
    def on_circle_press(self):
        backwards()
        print("backwards")
    
    def on_circle_release(self):
        stop()
        print("stop")
    
    def on_triangle_press(self):
        p.ChangeDutyCycle(12)
    
    def on_triangle_release(self):
        p.ChangeDutyCycle(7)
    
    def on_square_press(self):
        p.ChangeDutyCycle(2)
    
    def on_square_release(self):
        p.ChangeDutyCycle(7)
        
    def on_L3_left(self, value):
        print("Left! {}".format(value))
        print(int(-5/32767.0 * value + 7))
        p.ChangeDutyCycle(int(5/-32767.0 * value + 7))
        
    def on_L3_right(self, value):
        print("Right! {}".format(value))
        print(int(-5/32767.0 * value + 7))
        p.ChangeDutyCycle(int(-5/32767.0 * value + 7))
        
    def on_L3_at_rest(self):
        print("Resting")
        p.ChangeDutyCycle(7)
        
    def on_left_arrow_press(self):
        p.ChangeDutyCycle(12)
        
    def on_left_right_arrow_release(self):
        p.ChangeDutyCycle(7)
        
    def on_right_arrow_press(self):
        p.ChangeDutyCycle(2)
        
    def on_right_arrow_release(self):
        p.ChangeDutyCycle(7)


if __name__ == '__main__':     # Program start from here
    setup()
     
    GPIO.setup(pin,GPIO.OUT)
    p = GPIO.PWM(pin,50)
    p.start(7)

    try:
        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller.listen()
    except KeyboardInterrupt:
        destroy()
        p.stop()
        
