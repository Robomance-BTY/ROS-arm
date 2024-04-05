#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)


def main():
    Arm.Arm_serial_servo_write6(90, 172 ,16 ,12 ,90, 90, 800)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(90 ,90, 38, 62, 90,90, 800)
    time.sleep(2)
    Arm.Arm_serial_servo_write6(90 ,161, 21, 15, 90,90, 800)
    time.sleep(2)
    Arm.Arm_serial_servo_write6(90 ,90, 90, 90, 90,90, 800)
    time.sleep(2)
    Arm.Arm_serial_servo_write6(180 ,90, 90, 90, 90,90, 800)
    time.sleep(2)
    Arm.Arm_serial_servo_write6(180 ,90, 5, 5, 90, 90, 800)

try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  # Release DOFBOT object
