#! /usr/bin/env python
import rospy
import actionlib
from book_find.msg import FindBookAction, FindBookFeedback, FindBookResult

class BookServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('book_action', FindBookAction, self.execute, False)
        self.server.start()
    
    def execute(self, goal):
        rospy.loginfo(goal.book_name)
        feedback = FindBookFeedback()
        
       
        feedback.distance = 10.0
        for i in range(10):
     
            feedback.distance -= 1.0
 
            self.server.publish_feedback(feedback)
            rospy.sleep(1)
                        

            if self.server.is_preempt_requested():
                self.server.set_preempted()
                return

      
        result = FindBookResult(arrived='Yes')
        self.server.set_succeeded(result)

if __name__ == '__main__':
    rospy.init_node('book_server')
    server = BookServer()
    rospy.spin()
