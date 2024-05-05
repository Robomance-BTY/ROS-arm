#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)

def main():

    Arm.Arm_serial_servo_write6(95, 180, -5, 0, 0, 90, 1000)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(95, 180, -5, 0, 0, 180, 1000)
    
try :
    main()
except KeyboardInterrupt:
    print(" Program closed! ")
    pass

del Arm  # Release DOFBOT object
