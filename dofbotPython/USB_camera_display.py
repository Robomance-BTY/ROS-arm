import cv2
import time

def main():
    image = cv2.VideoCapture(0)  # 카메라 열기

    while True:
        ret, frame = image.read()  # 프레임 읽기
        cv2.imshow('frame', frame)  # 프레임 표시

        # 'q' 키를 누르면 프로그램 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)  # 10ms 대기

    image.release()  # 카메라 닫기
    cv2.destroyAllWindows()  # 창 닫기

if __name__ == "__main__":
    main()