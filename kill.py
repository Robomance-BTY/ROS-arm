#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)


def main():
    while True:
        Arm.Arm_serial_servo_write6(95, 109 ,50 ,37 ,89, 167, 500)
        time.sleep(0.5)
        Arm.Arm_serial_servo_write6(95, 109 ,50 ,5 ,89, 167, 500)
        time.sleep(0.5)
    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  # Release DOFBOT object
