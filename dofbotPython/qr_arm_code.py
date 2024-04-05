# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()  # USB 웹캠 카메라 사용시
# vs = VideoStream(usePiCamera=True).start()     # 파이 카메라 사용시
time.sleep(2.0)

# define the target region (center fifth of the frame horizontally)
frame_width = vs.read().shape[1]
target_left = frame_width // 5
target_right = target_left * 4

# variable to track if target is reached
target_reached = False

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 600 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode
        (x, y, w, h) = barcode.rect

        # calculate the center of the bounding box
        barcode_center_x = x + w // 2
        barcode_center_y = y + h // 2

        # calculate the distance to the target region
        distance_to_target = abs(barcode_center_x - (target_right + target_left) // 2)

        # calculate which segment the barcode is in
        segment_width = frame_width // 5
        segment = barcode_center_x // segment_width

        # draw the barcode bounding box and data on the frame
        if barcode.data.decode("utf-8") == "book2" and segment == 2 and not target_reached:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color for "book2" barcode in the third segment
            cv2.putText(frame, "Target reached", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            target_reached = True
            target_reached_time = time.time()  # Record the time when target is reached
        elif barcode.data.decode("utf-8") == "book2" and segment == 2:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red color for "book2" barcode in the third segment
            cv2.putText(frame, "Target reached", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif barcode.data.decode("utf-8") == "book2":
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color for other barcodes
            cv2.putText(frame, "Target detected", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(f"Distance to target: {distance_to_target:.2f}")

    # Move the arm 1 second after target is reached
    if target_reached and time.time() - target_reached_time >= 1:
        # Move the arm
        Arm.Arm_serial_servo_write6(90, 172, 16, 12, 90, 90, 800)
        time.sleep(1)
        Arm.Arm_serial_servo_write6(90, 90, 38, 62, 90, 90, 800)
        time.sleep(2)
        Arm.Arm_serial_servo_write6(90, 161, 21, 15, 90, 90, 800)
        time.sleep(2)
        Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 800)
        time.sleep(2)
        Arm.Arm_serial_servo_write6(180, 90, 90, 90, 90, 90, 800)
        time.sleep(2)
        Arm.Arm_serial_servo_write6(180, 90, 5, 5, 90, 90, 1500)
        time.sleep(2)
        target_reached = False  # Reset target reached flag
        break

    # show the output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
del Arm  # Release DOFBOT object
