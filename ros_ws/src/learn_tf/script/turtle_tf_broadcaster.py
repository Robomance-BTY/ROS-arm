#!/usr/bin/env python
# -*- coding: utf-8 -*-
import roslib
roslib.load_manifest('learn_tf')
import rospy
import tf
import turtlesim.msg
def handle_turtle_pose(msg, turtlename):
    br = tf.TransformBroadcaster()#Define a tf broadcast
    #tf transformation between broadcast world and input named turtle
    br.sendTransform((msg.x, msg.y, 0),tf.transformations.quaternion_from_euler(0, 0, msg.theta),rospy.Time.now(),turtlename,"world")
if __name__ == '__main__':
    rospy.init_node('turtle1_turtle2_tf_broadcaster')#Initialize ros node
    turtlename = rospy.get_param('~turtle',"turtle_name") #Get the turtle's name from the parameter server
    #Subscribe/pose topic data, which is the turtle’s pose information
    rospy.Subscriber('/%s/pose' % turtlename,turtlesim.msg.Pose,handle_turtle_pose,turtlename)
    rospy.spin()