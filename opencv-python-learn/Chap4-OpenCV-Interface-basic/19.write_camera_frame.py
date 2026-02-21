import cv2

capture = cv2.VideoCapture(0)       # 0번 카메라 연결
if not capture.isOpened(): raise Exception("카메라 연결 안됨")

fps = 29.97
delay = round(1000/fps)     # 프레임 간 지연 시간
size = (640, 480)
fourcc = cv2.VideoWriter.fourcc(*'DX50')    # 압축 코덱 설정

## 카메라 속성 실행창에 출력
print("width x height: ", size)
print("VideoWriter_fourcc: %s" % fourcc)
print("delay: %2d ms" % delay)
print("fps: %d" % fps)

capture.set(cv2.CAP_PROP_ZOOM, 1) # 카메라 속성 지정
capture.set(cv2.CAP_PROP_FOCUS, 0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, size[0]) # 해상도 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

## 동영상 파일 개방 및 코덱, 해상도 설정
writer = cv2.VideoWriter("images/video_file.avi", fourcc, fps, size)
if not writer.isOpened(): raise Exception("동영상 파일 개발 안됨")

while True:
    ret, frame = capture.read() # 카메라 영상 받기
    if not ret: break
    if cv2.waitKey(delay) >= 0: break

    writer.write(frame) # 프레임을 동영상으로 저장
    cv2.imshow("Video Frame from Camera", frame)

writer.release()
capture.release()