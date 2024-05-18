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

    def execute_callback(self, goal):
        rospy.loginfo(f"bookname is {goal.book_name}, book storage is {goal.book_storage}")
        rospy.set_param('/service_server/book_storage', goal.book_storage)
        feedback = FindBookFeedback()
        detect_book = False

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
                    
                    # QR 코드 중심점 계산
                    barcode_center_x = x + w // 2
                    barcode_center_y = y + h // 2

                    # 프레임 중심점 계산
                    frame_center_x = frame_width // 2
                    frame_center_y = frame_height // 2

                    # QR 코드와 프레임 중심점 사이의 각도 계산
                    angle = math.atan2(barcode_center_y - frame_center_y, barcode_center_x - frame_center_x) * 180 / math.pi

                    # 각도 정보를 문자열로 변환하여 프레임에 표시
                    angle_text = f"Angle: {angle:.2f} degrees"
                    cv2.putText(frame, angle_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

                    # 7분할 선을 그리기 위한 반복문
                    for i in range(1, 6):
                        line_x = i * section_width
                        # 세로선 그리기 (시작점, 끝점, 색상(BGR), 두께)
                        cv2.line(frame, (line_x, 0), (line_x, frame_height), (0, 255, 0), 2)

                    # 3번째 선과 QR 코드 중심점 사이의 거리 계산
                    distance_to_third_line = barcode_center_x - 3 * section_width

                    if distance_to_third_line < 1 and distance_to_third_line > -1:  # QR 코드가 3번째 선 위에 있으면
                        result = FindBookResult()
                        result.arrived = True
                        self.server.set_succeeded(result)
                        pub = rospy.Publisher('/order', String, queue_size=6)
                        order_msg = rospy.get_param("/service_server/book_storage")
                        pub.publish(order_msg)
                        return
                    else:
                        feedback.distance = distance_to_third_line  # 3번째 선까지의 거리를 feedback으로 설정
                        self.server.publish_feedback(feedback)

            if self.server.is_preempt_requested():
                self.server.set_preempted()
                return 

            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cv2.destroyAllWindows()
                self.vs.stop()
                break

        cv2.destroyAllWindows()
        self.vs.stop()

if __name__ == '__main__':
    rospy.init_node('find_book_action_server_node')
    server = BookServer()
    rospy.spin()
