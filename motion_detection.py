# Stockton Hemming, Winter 2026
# ENGR 121
# 3/11/26
# this program determines if the module moves, and if it isn't then it will detect if there is motion around the sensor
# then if there is then it triggers the active buzzer 

from imu import MPU6050
from machine import I2C, Pin
import time



i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
mpu = MPU6050(i2c)

# while True:
#     print("x: %s, y: %s, z: %s"%(mpu.accel.x, mpu.accel.y, mpu.accel.z))
#     time.sleep(0.5)
#     print("A: %s, B: %s, Y: %s"%(mpu.gyro.x, mpu.gyro.y, mpu.gyro.z))
#     time.sleep(0.5)
    
import math #determining, but not direction
import time
import utime

pir_sensor = machine.Pin(14, machine.Pin.IN)

global timer_delay
timer_delay = utime.ticks_ms()
print("start")

def pir_in_high_level(pin):
    global timer_delay
    pir_sensor.irq(trigger=machine.Pin.IRQ_FALLING, handler=pir_in_low_level)
    intervals = utime.ticks_diff(utime.ticks_ms(), timer_delay)
    timer_delay = utime.ticks_ms()
    print("the dormancy duration is " + str(intervals) + "ms")

def pir_in_low_level(pin):
    global timer_delay
    pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_in_high_level)
    intervals2 = utime.ticks_diff(utime.ticks_ms(), timer_delay)
    timer_delay = utime.ticks_ms()
    print("the duration of work is " + str(intervals2) + "ms")


# Variables for oscilating orientation 
last_move_var = time.ticks_ms()
stationary_confirmed = False
threshold = 0.05  #(can adjust for a larger threshold)
Ms_delay = 1000   

#measures magnittude of the mvmnt of orientation
while True:
    ax, ay, az = mpu.accel.x, mpu.accel.y, mpu.accel.z
    magnitude = math.sqrt(ax**2 + ay**2 + az**2)
    
    if abs(magnitude - 1.0) > threshold:
        last_move_var = time.ticks_ms() # Reset the timer because it moved
        if stationary_confirmed:
            print("Orientation changed!")
            stationary_confirmed = False
    # measureing if the time is good enough for to be stationary 
    else:
        time_vs_mvmnt = time.ticks_diff(time.ticks_ms(), last_move_var)
        
        if time_vs_mvmnt > Ms_delay and not stationary_confirmed:
            print("Stationary confirmed")
            stationary_confirmed = True
            pir_sensor.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_in_high_level)
               
    time.sleep(0.05)

 

    
    
    
    