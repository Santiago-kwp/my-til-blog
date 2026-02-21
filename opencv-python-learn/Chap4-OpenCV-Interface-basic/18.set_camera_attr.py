import cv2
from Common.utils import put_string

def zoom_bar(value):            # 줌 조절 콜백 함수
    global capture
    capture.set(cv2.CAP_PROP_ZOOM, value)   # 줌 설정

def focus_bar(value):           # 초점 조절 콜백 함수
    global capture
    capture.set(cv2.CAP_PROP_FOCUS, value)

capture = cv2.VideoCapture(0)   # 0번 카메라 연결
if not capture.isOpened(): raise Exception("카메라 연결 안됨")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 자동초점 중지 > 카메라 렌즈의 초점을 직접 조절하기 위해 자동 초점 중지
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)   # 프레임 밝기 초기화

title = "Change Camera Properties"
cv2.namedWindow(title)
cv2.createTrackbar('zoom', title, 0, 10, zoom_bar)  # 줌 트랙바
cv2.createTrackbar('focus_bar', title, 0, 40, focus_bar)

while True:
    ret, frame = capture.read() # 카메라 영상 받기
    if not ret: break
    if cv2.waitKey(30) >=0: break

    zoom = int(capture.get(cv2.CAP_PROP_ZOOM)) # 카메라 속성 가져오기
    focus = int(capture.get(cv2.CAP_PROP_FOCUS))
    put_string(frame, "Zoom: ", (10, 240), zoom) # 줌 값 표시
    put_string(frame, "Focus: ", (10, 270), focus) # 초점 값 표시
    cv2.imshow(title, frame)

capture.release() # 비디오 캡처 메모리 해제


