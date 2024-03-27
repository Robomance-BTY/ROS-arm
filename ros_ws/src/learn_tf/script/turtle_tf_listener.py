#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')#Initialize ros node
    listener = tf.TransformListener()#Initialize a listener
    rospy.wait_for_service('spawn')
    #Call the service to spawn another turtle turtle2
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(8, 6, 0, 'turtle2')
    #Declare a publisher to publish the speed of turtle2
    turtle_vel = rospy.Publisher('turtle2/cmd_vel',geometry_msgs.msg.Twist,queue_size=1)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
        #Find tf changes between turtle2 and turtle1
            (trans,rot) = listener.lookupTransform('/turtle2', '/turtle1',rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException,tf.ExtrapolationException):
            continue
    #Through mathematical calculations, calculate the linear velocity and angular velocity, and then publish them
        angular = 6.0 * math.atan2(trans[1], trans[0])
        linear = 0.8 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)
        rate.sleep()