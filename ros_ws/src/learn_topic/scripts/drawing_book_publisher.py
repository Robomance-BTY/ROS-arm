#!/usr/bin/env python3
#coding=utf-8

import time
import rospy
from std_msgs.msg import String
from Arm_Lib import Arm_Device

def drawing_book(arm):
    arm.Arm_serial_servo_write6(90, 172, 16, 12, 90, 90, 800)
    time.sleep(1)
    arm.Arm_serial_servo_write6(90, 90, 38, 62, 90, 90, 800)
    time.sleep(2)

def linear_publisher():
    rospy.init_node('linear_publisher', anonymous=True)
    pub = rospy.Publisher('/move', String, queue_size=6)
    rate = rospy.Rate(1)  # 1 message per second
    while not rospy.is_shutdown():
        pub.publish("go")  # Publish the message
        rate.sleep()  # Wait for the specified rate

if __name__ == '__main__':
    try:
        Arm = Arm_Device()
        time.sleep(0.1)
        drawing_book(Arm)
        linear_publisher()
    except rospy.ROSInterruptException:
        pass
    finally:
        del Arm  # Release DOFBOT object
