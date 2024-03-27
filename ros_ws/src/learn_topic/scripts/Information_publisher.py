#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from learn_topic.msg import Information #Import custom msg
def information_publisher():
    rospy.init_node('information_publisher', anonymous=True)# ROS node initialization
    # Create a Publisher and publish a topic named /company_info. The message type is learn_topic::Information and the queue length is 6.
    info_pub = rospy.Publisher('/company_info', Information, queue_size=6)
    rate = rospy.Rate(10) #Set the loop frequency
    while not rospy.is_shutdown():
    # Initialize messages of type learn_topic::Information
        info_msg = Information()
        info_msg.company = "Yahboom";
        info_msg.city = "Shenzhen";
        info_pub.publish(info_msg)# Release the news
        rospy.loginfo("This is %s in %s.", info_msg.company, info_msg.city)# Print release message
        rate.sleep()# Delay according to cycle frequency
if __name__ == '__main__':
    try:
        information_publisher()
    except rospy.ROSInterruptException:
        pass