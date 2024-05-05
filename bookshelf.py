#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)

def stretch_arm(arm):
    arm.Arm_serial_servo_write6(95, 50, 47, 78, 90, 90, 800)
    time.sleep(2)

def hold_book(arm):
    arm.Arm_serial_servo_write6(95, 50, 47, 78, 90, 128, 800)
    time.sleep(2)

def withdraw(arm):
    arm.Arm_serial_servo_write6(95, 180, 0, 0, 90, 128, 800)
    time.sleep(2)

def main():

    stretch_arm(Arm)
    hold_book(Arm)
    withdraw(Arm)
    Arm.Arm_serial_servo_write6(-3,110 , 56, 7, 81, 128, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(-3,88 , 11, 3, 81, 128, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(-3,76 , 11, 9, 81, 128, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(-3,76 , 11, 9, 81, 90, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(-3,110 , 56, 7, 81, 128, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(95, 180, -5, 0, 0, 90, 1000)
    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  # Release DOFBOT object
