#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
from turtlesim.srv import Spawn
def turtle_spawn():
    rospy.init_node('new_turtle')# ROS node initialization
    rospy.wait_for_service('/spawn')# Wait/spawn service
    try:
        new_turtle = rospy.ServiceProxy('/spawn', Spawn)
        response = new_turtle(2.0, 2.0, 0.0, "turtle2")# Enter request data
        return response.name
    except rospy.ServiceException as e:
        print ("failed to call service : %s")
if __name__ == "__main__":
    #Call the service and display the call results
    print ("a new turtle named %s." %(turtle_spawn()))