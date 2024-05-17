#!/usr/bin/env python3
# coding: utf-8

import rospy
import Arm_Lib
from math import pi
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

rospy.init_node('arm_publisher', anonymous=True)
pub = rospy.Publisher('/joint_states', JointState, queue_size=6)

# 로봇 팔의 5개 관절 이름 정의
joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'gripper']

# 관절 각도 초기화
joint1 = 0.0
joint2 = 0.0 
joint3 = 0.0
joint4 = 0.0
joint5 = 0.0
gripper = 0.0

# 관절 각도 변경 루프
rate = rospy.Rate(10) # 10Hz
while not rospy.is_shutdown():
    # 관절 각도 업데이트
    joint1 = 0.12
    joint2 = 0.22
    joint3 = 0.33
    joint4 = 0.24
    joint5 = -0.05
    gripper = 0.12
    
    # JointState 메시지 생성
    joint_state = JointState()
    joint_state.header = Header()
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name = joint_names
    joint_state.position = [joint1, joint2, joint3, joint4, joint5, gripper]
    
    # JointState 메시지 발행
    pub.publish(joint_state)
    
    rate.sleep()
