#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import time
from std_msgs.msg import String
from Arm_Lib import Arm_Device
from arm_movement.srv import MoveLinear

Arm = Arm_Device()

def stretch_arm(arm):
    arm.Arm_serial_servo_write6(90, 90, 38, 62, 90, 90, 800)
    time.sleep(1)

def hold_book(arm):
    arm.Arm_serial_servo_write6(90, 90, 38, 62, 90, 174, 800)
    time.sleep(1)

def withdraw(arm):
    arm.Arm_serial_servo_write6(90, 180, 0, 0, 90, 174, 800)
    time.sleep(1)

def linear_publisher():
    rospy.init_node('linear_publisher', anonymous=True)
    pub = rospy.Publisher('/move', String, queue_size=6)
    rate = rospy.Rate(1)  # 1 message per second
    while not rospy.is_shutdown():
        pub.publish("go")  # Publish the message
        rate.sleep()  # Wait for the specified rate


def move_linear_client(command):
    rospy.wait_for_service('move_linear_service')
    try:
        move_linear = rospy.ServiceProxy('move_linear_service', MoveLinear)
        resp = move_linear(command)
        return resp.success, resp.message
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

def callback(data):
    stretch_arm(Arm)
    success, message = move_linear_client("drawing_book_forward")
    if success:
        rospy.loginfo("Service call was successful. %s", message)
        hold_book(Arm)
        success, message = move_linear_client("drawing_book_backward")
        if success:
            withdraw(Arm)     
    else:
        rospy.logwarn("Service call failed. %s", message)

def topic_listener():
    rospy.Subscriber('order', String, callback)

if __name__ == "__main__":
    try:
        rospy.init_node('move_book_client')
        topic_listener()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
    finally:
        del Arm  # Release DOFBOT object
    
