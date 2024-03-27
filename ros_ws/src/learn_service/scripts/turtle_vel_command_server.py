#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This routine will execute the /turtle_command service, service data type std_srvs/Trigger
import rospy
import _thread,time
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
pubvel = False;
turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=8)
def pubvel_thread():
    while True:
        if pubvel:
            vel_msg = Twist()
            vel_msg.linear.x = 0.6
            vel_msg.angular.z = 0.8
            turtle_vel_pub.publish(vel_msg)
        time.sleep(0.1)
def pubvelCallback(req):
    global pubvel
    pubvel = bool(1-pubvel)
    rospy.loginfo("Do you want to publish the vel?[%s]", pubvel)# Show request data
    return TriggerResponse(1, "Change state!")# Feedback data
def turtle_pubvel_command_server():
    rospy.init_node('turtle_vel_command_server')# ROS node initialization
    # Create a server named /turtle_command and register the callback function pubvelCallback
    s = rospy.Service('/turtle_vel_command', Trigger, pubvelCallback)
    # Loop waiting for callback function
    print ("Ready to receive turtle_pub_vel_command.")
    _thread.start_new_thread(pubvel_thread, ())
    rospy.spin()
if __name__ == "__main__":
    turtle_pubvel_command_server()