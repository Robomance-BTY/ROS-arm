#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from learn_topic.msg import Information #Import custom msg
def CompanyInfoCallback(msg):
    rospy.loginfo("company: name:%s city:%s ", msg.company, msg.city)#Print subscription received information
def Infomation_subscriber():
    rospy.init_node('Infomation_subscriber', anonymous=True)# ROS node initialization
    #Create a Subscriber, subscribe to the topic named /company_info, and register the callback function personInfoCallback
    rospy.Subscriber("/company_info", Information, CompanyInfoCallback)
    rospy.spin()# Loop waiting for callback function
if __name__ == '__main__':
    Infomation_subscriber()