#!/usr/bin/env python3
# coding: utf-8

import rospy
import Arm_Lib
from math import pi
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import time

rospy.init_node('arm_publisher', anonymous=True)
pub = rospy.Publisher('/joint_states', JointState, queue_size=6)

# 로봇 팔의 5개 관절 이름 정의
joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']

joint_states = {
    "stratch_arm" : [0.04, 0.66, -1.27, -0.91 , 0, -0.8],
    "hold_book" : [0.04, 0.66, -1.27, -0.91 , 0, 1],
    "withdraw" : [0.04, 1.55, -1.57, -1.57, 0, 1],
    "store_book" : [-1.53, -0.36, -1.29, -1.57, 0, 1],
    "put_book" : [-1.53, -0.36, -1.29, -1.57, 0, -0.8]
}

while not rospy.is_shutdown():
    # 관절 각도 업데이트
    
    # JointState 메시지 생성
    joint_state = JointState()
    joint_state.header = Header()
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name = joint_names
    joint_state.position = joint_states['stratch_arm']
    pub.publish(joint_state)
   


