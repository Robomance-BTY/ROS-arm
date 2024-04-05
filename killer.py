#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)


def main():
    while True:
        Arm.Arm_serial_servo_write6(95, 109 ,50 ,37 ,89, 130, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(75, 50 ,77 ,50 ,89, 167, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(110, 109 ,50 ,37 ,89, 140, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(110, 50 ,65 ,50 ,89, 120, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(40, 109 ,50 ,37 ,89, 96, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(40, 50 ,65 ,50 ,89, 167, 500)
        time.sleep(0.5)
    
    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  # Release DOFBOT object
