#! /usr/bin/env python
import rospy
import actionlib
from book_find.msg import FindBookAction, FindBookGoal

client = None

def feedback_cb(feedback):
    rospy.loginfo('distance: %f' % feedback.distance)

def book_client():
    global client
    client = actionlib.SimpleActionClient('book_action', FindBookAction)
    client.wait_for_server()

    goal = FindBookGoal(book_name='book1', book_storage="book_storage2")
    

    client.send_goal(goal, feedback_cb=feedback_cb)

    client.wait_for_result()
    rospy.loginfo(client.get_state())
    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('mobility')
        result = book_client()
        if result:
            rospy.loginfo('is arrived: %s' % result.arrived)
        else:
            rospy.loginfo('Goal was cancelled or failed to execute.')
    except rospy.ROSInterruptException:
        pass
