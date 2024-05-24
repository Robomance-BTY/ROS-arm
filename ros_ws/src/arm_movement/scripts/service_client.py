#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import time
from std_msgs.msg import String
from Arm_Lib import Arm_Device
from arm_movement.srv import MoveLinear
from sensor_msgs.msg import JointState

def dofbot_move(dofbot_position):
    joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']
    joint_state = JointState()

    joint_states = {
        "stratch_arm" : [0.04, 0.66, -1.27, -0.91 , 0, -0.8],
        "hold_book" : [0.04, 0.66, -1.27, -0.91 , 0, 1.2],
        "withdraw" : [0.04, 1.55, -1.57, -1.57, 0, 1.2],
        "store_book_start" : [-1.53, 0., -1.42, -1.57, 0, 1.2],
        "store_book_end" : [-1.53, -0.36, -1.29, -1.57, 0, 1.2],
        "put_book" : [-1.53, -0.36, -1.29, -1.57, 0, -0.8],
        "reset" : [0.04, 1.55, -1.57, -1.57, -1.57, 1.4]
    }

    joint_state.name = joint_names
    joint_state.position = joint_states[dofbot_position]
    dofbot_joint_pub.publish(joint_state)
    time.sleep(2)

    return


def linear_publisher():
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

def draw_book():
    dofbot_move("stratch_arm")
    success, message = move_linear_client("drawing_book_forward")
    if success:
        rospy.loginfo("Service call was successful. %s", message)
        dofbot_move("hold_book")
        success, message = move_linear_client("drawing_book_backward")
        if success:
            dofbot_move("withdraw")   
    else:
        rospy.logwarn("Service call failed. %s", message)

def arm_order_callback(order):
    rospy.loginfo("receivedata %s", order)
    draw_book()
    move_linear_client(order.data)
    dofbot_move("store_book_start")
    dofbot_move("store_book_end")
    dofbot_move("put_book")
    dofbot_move("reset")
    move_linear_client("reset")
    
    

def topic_listener():
    rospy.Subscriber('order', String, arm_order_callback)

if __name__ == "__main__":
    try:
        rospy.init_node('robot_arm')
        dofbot_joint_pub = rospy.Publisher('/joint_states', JointState, queue_size=6)
        pub = rospy.Publisher('/move', String, queue_size=6)

        topic_listener()
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
    
