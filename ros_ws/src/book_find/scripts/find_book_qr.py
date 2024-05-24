#!/usr/bin/env python3
#coding=utf-8

import rospy
import actionlib
import math
import time
import cv2
import imutils
import argparse
from imutils.video import VideoStream
from pyzbar import pyzbar
from book_find.msg import FindBookAction, FindBookFeedback, FindBookResult
from std_msgs.msg import String

class BookServer:
    def __init__(self):
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)
        self.server = actionlib.SimpleActionServer('book_action', FindBookAction, self.execute_callback, False)
        self.server.start()
        
    def publish_order(self):
        order_msg = rospy.get_param("/service_server/book_storage")
        pub.publish(order_msg)


    def execute_callback(self, goal):
        rospy.loginfo(f"bookname is {goal.book_name}, book storage is {goal.book_storage}")
        rospy.set_param('/service_server/book_storage', goal.book_storage)
        feedback = FindBookFeedback()
        detect_book = False
        distance_count = 0
        while not rospy.is_shutdown():
            frame = self.vs.read()
            frame = imutils.resize(frame, width=600)
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                if barcode.data.decode("utf-8") == goal.book_name:
                    target_found = True
                    (x, y, w, h) = barcode.rect
                    frame_height, frame_width, _ = frame.shape
                    section_width = frame_width // 6  # 전체 폭을 7분할
                    # 7분할 선을 그리기 위한 반복문
                    for i in range(1, 6):
                        line_x = i * section_width
                        # 세로선 그리기 (시작점, 끝점, 색상(BGR), 두께)
                        cv2.line(frame, (line_x, 0), (line_x, frame_height), (0, 255, 0), 2)

                    # QR 코드 중심점 계산
                    barcode_center_x = x + w // 2

                    # 3번째 선의 x 좌표
                    third_line_x = 3 * section_width

                    # 3번째 선과 QR 코드 중심점 사이의 거리 계산
                    distance_to_third_line = (barcode_center_x - third_line_x)

                    if distance_to_third_line <= -71 and distance_to_third_line >= -79:  # QR 코드가 3번째 선 위에 있으면
                        feedback.distance = distance_to_third_line  # 3번째 선까지의 거리를 feedback으로 설정
                        self.server.publish_feedback(feedback)
                        distance_count += 1
                        # if distance_count >15:
                        time.sleep(3)
                        self.publish_order()
                        result = FindBookResult()
                        result.arrived = True 
                        self.server.set_succeeded(result)
                        return  
                    else:
                            distance_count = 0
                            feedback.distance = distance_to_third_line  # 3번째 선까지의 거리를 feedback으로 설정
                            self.server.publish_feedback(feedback)

            if self.server.is_preempt_requested():
                self.server.set_preempted()
                return 

            #cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cv2.destroyAllWindows()
                self.vs.stop()
                break

        cv2.destroyAllWindows()
        self.vs.stop()
        

if __name__ == '__main__':
    rospy.init_node('find_book_action_server')
    pub = rospy.Publisher('order', String, queue_size=10)
    server = BookServer()
    rospy.spin()
