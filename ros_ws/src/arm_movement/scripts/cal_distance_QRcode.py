#!/usr/bin/env python3
#coding=utf-8

import time
import rospy
from std_msgs.msg import Bool, Float32
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import cv2
import math

global stop_command, distance_info
stop_command = False
distance_info = 0.0

def camera_node():
    global stop_command, distance_info
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                    help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())

    # 카메라 초기화
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    
    # 토픽 발행 준비
    stop_pub = rospy.Publisher('/stop_command', Bool, queue_size=1)
    distance_pub = rospy.Publisher('/distance_info', Float32, queue_size=1)
    
    # 프레임 처리 루프
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        
        # QR 코드 인식
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            
            # QR 코드 중심점 계산
            barcode_center_x = x + w // 2
            barcode_center_y = y + h // 2
            
            # 화면 중심점 계산
            frame_height, frame_width, _ = frame.shape
            screen_center_x = frame_width // 2
            screen_center_y = frame_height // 2
            
            # QR 코드 발견 시 정지 명령 발행
            if barcode.data.decode("utf-8") == "book2":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Target reached", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # 2초 후에 정지 명령 및 거리 정보 발행
                time.sleep(2.0)
                stop_command = True
                stop_pub.publish(stop_command)
                distance = math.sqrt((barcode_center_x - screen_center_x)**2 + (barcode_center_y - screen_center_y)**2)
                distance_info = distance
                distance_pub.publish(distance_info)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Target detected", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # 화면 출력
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
        
        # 'q' 키 입력 시 종료
        if key == ord("q"):
            break
    


    

    # 정리
    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    try:
        rospy.init_node('camera_node', anonymous=True)
        camera_node()
    except rospy.ROSInterruptException:
        pass
    finally:
        pass
