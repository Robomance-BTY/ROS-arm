import cv2
import numpy as np

def resize_image(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# USB 카메라에서 영상 캡처 시작
cap = cv2.VideoCapture(0)

# QR 코드 검출을 위한 QRCodeDetector 객체 생성
qrDecoder = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        print("카메라를 시작할 수 없습니다.")
        break

    # 이미지 확대하기 (예: 2배 확대)
    frame_resized = resize_image(frame, 1)
    
    # 확대된 이미지에서 QR 코드 검출
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(frame_resized)
    if len(data) > 0:
        print("Decoded Data : {}".format(data))
        # 검출된 QR 코드 주변에 사각형 그리기
        if bbox is not None:
            n = len(bbox)
            for j in range(n):
                cv2.line(frame_resized, tuple(bbox[j][0]), tuple(bbox[(j+1) % n][0]), (255,0,0), 3)

        # 확대된 이미지와 QR 코드 검출 결과 표시
        cv2.imshow("QR Code Detection", frame_resized)
    else:
        cv2.imshow("QR Code Detection", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 메모리를 해제하고 모든 창을 닫습니다.
cap.release()
cv2.destroyAllWindows()
