#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from turtlesim.msg import Pose
def poseCallback(msg):
    rospy.loginfo("Turtle pose: x:%0.3f, y:%0.3f", msg.x, msg.y)
def turtle_pose_subscriber():
    rospy.init_node('turtle_pose_subscriber', anonymous=True)# ROS node initialization
    # Create a Subscriber, subscribe to the topic named /turtle1/pose, and register the callback function poseCallback
    rospy.Subscriber("/turtle1/pose", Pose, poseCallback)
    rospy.spin()# Loop waiting for callback function
if __name__ == '__main__':
    turtle_pose_subscriber()