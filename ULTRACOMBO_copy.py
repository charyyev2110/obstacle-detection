
import machine
from imu import MPU6050
from machine import I2C, Pin

import math #determining mag., but not direction
import time
import utime

from machine import Pin,SPI,PWM
import framebuf
import machine
import utime
import random
import math

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
mpu = MPU6050(i2c)

#pins for passive buzzer
passive_pwm = machine.PWM(machine.Pin(15))

#pins for active buzzer
active_buzzer = machine.Pin(13, machine.Pin.OUT)

#pins for pir
pir_sensor = machine.Pin(14, machine.Pin.IN)

#pins for ultrsonic sensor
TRIG = machine.Pin(17,machine.Pin.OUT)
ECHO = machine.Pin(16,machine.Pin.IN)


timer_delay = utime.ticks_ms()
print("start")

#ultrasonic sensor def
def distance():
    ""
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(100)
    TRIG.low()
    while not ECHO.value():
        pass
    time1 = time.ticks_us()
    while ECHO.value():
        pass
    time2 = time.ticks_us()
    during = time.ticks_diff(time2,time1)
    return during * 340 / 2 / 10000


def pir_in_high_level(pin): #modified from sunfounder 
    global timer_delay
    global intervals
    pir_sensor.irq(trigger=machine.Pin.IRQ_FALLING, handler=pir_in_low_level)
    intervals = utime.ticks_diff(utime.ticks_ms(), timer_delay)
    timer_delay = utime.ticks_ms()
    #print("the dormancy duration is " + str(intervals) + "ms")


def pir_in_low_level(pin): #modified from sunfounder 
    global intervals2
    global timer_delay
    pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_in_high_level)
    intervals2 = utime.ticks_diff(utime.ticks_ms(), timer_delay)
    timer_delay = utime.ticks_ms()
    #++print("the duration of work is " + str(intervals2) + "ms")
  #  print(type(intervals2))

#pir_in_low_level(pir_sensor)

#calling functions to trigger pir before loop
pir_in_low_level(pir_sensor)
pir_in_high_level(pir_sensor)

def tone(pin,frequency,duration): #modified from Sunfounder
    pin.freq(frequency)
    pin.duty_u16(30000)
    utime.sleep_ms(duration)
    pin.duty_u16(0)
    
    

#--- screen set up---

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 161 # This number was not expected?
        self.height = 130
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36);
        self.write_data(0x70);
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);

            #sleep out
        self.write_cmd(0x11);
        #DEV_Delay_ms(120);

        #Turn on the LCD display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xf1)        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xf1)        
        self.write_cmd(0x2C)       
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
  
pwm = PWM(Pin(BL))
pwm.freq(1000)

pwm.duty_u16(32768) # max 65535
LCD = LCD_1inch8()
# Background colour is BLACK
LCD.fill(0x0) # BLACK
LCD.show()
# ============= END OF SCREEN DRIVER & SETUP ==================


def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour

def frame (d):
    LCD.fill(0)
    for j in range (10, 130, 10):
        LCD.hline (1, j, 160, colour (255, 255, 255))
    for i in range (10, 160, 10):
        LCD.vline (i, 1, 160, colour (255,255,255))
#         for i in range (161):
#             LCD.pixel (i,j, colour (255,255,255))
    LCD.text ("200 cm", 110, 3, colour (255,0,0))
    LCD.text ("30 cm", 118, 113, colour (255,0,0))
    if d < 400:
        x = d/200 *125
        #print (d, x)
        LCD.text ("X", 80, 125-int(x), colour(255,255,0))
    else:
        time.sleep (0.1)
    LCD.show()
    

# Variables for oscilating accelerometer orientation 
stationary_confirmed = False
threshold = 0.09  #(can adjust for a larger threshold)
last_move_var = time.ticks_ms()

Ms_delay = 100   

#measures magnittude of the mvmnt of orientation
while True:
    #|PIR|
    frame (distance())
    ax, ay, az = mpu.accel.x, mpu.accel.y, mpu.accel.z
    magnitude = math.sqrt(ax**2 + ay**2 + az**2)
   
    utime.sleep(1)
    if abs(magnitude - 1.0) > threshold:
        last_move_var = time.ticks_ms() # Reset the timer because it moved
    # |Accelerometer|
        if stationary_confirmed:
            print("Orientation changed!")
            stationary_confirmed = False
            
    # measureing the time in relation to if the accel. is stationary
    elif abs(magnitude - 1.0) < threshold:
        time_vs_mvmnt = time.ticks_diff(time.ticks_ms(), last_move_var)
       # print (time_vs_mvmnt, time.ticks_ms(), last_move_var)
        
        if time_vs_mvmnt > Ms_delay and not stationary_confirmed:
            print("Stationary confirmed")
            stationary_confirmed = True
            pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_in_low_level)
          
        #|PIR|Passive Buzzer|
        if intervals > 3000:
            print("motion detected")

            tone(passive_pwm,440,250) #start of passive buzzer 
            utime.sleep_ms(500)
            tone(passive_pwm,494,250)
            utime.sleep_ms(500)
            tone(passive_pwm,523,250)
            
    dis = distance()
    if dis > 400:
        time.sleep(0.1)
    if 40 < dis < 400:
        delay = max(dis / 500, 0.05)   # closer = smaller delay
        active_buzzer.value(1)
        time.sleep(0.1)
        active_buzzer.value(0)
        time.sleep(delay)
    elif dis <= 40:
       delay = max(dis / 300, 0.05)   # closer = smaller delay
       active_buzzer.value(1)
       time.sleep(0.05)
       active_buzzer.value(0)
       time.sleep(delay)







    
#     
#    



