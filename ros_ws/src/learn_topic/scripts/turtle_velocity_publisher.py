#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This routine will publish to the turtle1/cmd_vel topic, message type geometry_msgs::Twist
import rospy
from geometry_msgs.msg import Twist
def turtle_velocity_publisher():
    rospy.init_node('turtle_velocity_publisher', anonymous=True) # ROS node initialization
    # Create a small turtle speed publisher and publish a topic named /turtle1/cmd_vel. The message type is geometry_msgs::Twist, and 8 represents the message queue length.
    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=8)
    rate = rospy.Rate(10) #Set the frequency of the loop
    while not rospy.is_shutdown():
        # Initialize geometry_msgs::Twist type message
        turtle_vel_msg = Twist()
        turtle_vel_msg.linear.x = 0.8
        turtle_vel_msg.angular.z = 0.6
        # release the news
        turtle_vel_pub.publish(turtle_vel_msg)
        rospy.loginfo("linear is :%0.2f m/s, angular is :%0.2f rad/s",
        turtle_vel_msg.linear.x, turtle_vel_msg.angular.z)
        rate.sleep()# Delay according to cycle frequency
if __name__ == '__main__':
    try:
        turtle_velocity_publisher()
    except rospy.ROSInterruptException:
        pass