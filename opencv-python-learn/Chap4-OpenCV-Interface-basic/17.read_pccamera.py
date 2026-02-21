import cv2

def put_string(frame, text, pt, value, color=(120, 200, 90) ): # 문자열 출력 함수
    text += str(value)
    shade = (pt[0] + 2, pt[1] + 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, shade, font, 0.7, (0, 0, 0), 2) # 그림자 효과
    cv2.putText(frame, text, pt, font, 0.7, color, 2)              # 글자 적기

capture = cv2.VideoCapture(0)   # 0 번 카메라 연결
if capture.isOpened() == False:
    raise Exception("Error opening video stream or file")


## 카메라 속성 획득 및 출력
print("너비 %d" % capture.get(cv2.CAP_PROP_FRAME_WIDTH))
print("높이 %d" % capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("노출 %d" % capture.get(cv2.CAP_PROP_EXPOSURE))
print("밝기 %d" % capture.get(cv2.CAP_PROP_BRIGHTNESS))

while True:
    ret, frame = capture.read()                     # 카메라 영상 받기
    if not ret: break
    if cv2.waitKey(30) >= 0: break                  # 종료 조건 - 스페이스바 키

    exposure = capture.get(cv2.CAP_PROP_EXPOSURE)   # 노출 속성 획득
    put_string(frame, 'EXPOS: ', (10, 40), exposure)
    title = "View Frame from Camera 0"
    cv2.imshow(title, frame)

capture.release()