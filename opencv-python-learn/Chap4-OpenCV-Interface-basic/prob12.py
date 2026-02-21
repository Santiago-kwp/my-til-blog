import numpy as np
import cv2

def onChange(value):                # 트랙바 콜백 함수
    global image, original, title             # 전역 변수 참조

    print("추가 화소값:", value)
    image[:] = original + value
    cv2.imshow(title, image)

# 원본 영상 (검정색)
original = np.zeros((300, 500), np.uint8)
image = original.copy()

title = 'Trackbar Event'
cv2.imshow(title, image)

# 트랙바: 0 ~ 255범위
cv2.createTrackbar('Brightness', title, 0, 255, onChange) # 트랙바 콜백함수 등록


while True:
    # 특수키(방향 키 등)를 입력받기 위해 waitKeyEx 사용
    key = cv2.waitKeyEx(0)

    # 현재 트랙바 값 읽기
    pos = cv2.getTrackbarPos('Brightness', title)
    if key == 27: # ESC 키 -> 종료
        break
    elif key == 2424832: # 왼쪽 화살표 (mac은 81),
        if pos > 0:
            cv2.setTrackbarPos('Brightness', title, pos - 1)
    elif key == 2555904: # 오른쪽 화살표 (mac은 83)
        if pos < 255:
            cv2.setTrackbarPos('Brightness', title, pos + 1)


cv2.waitKey(0)
cv2.destroyAllWindows()