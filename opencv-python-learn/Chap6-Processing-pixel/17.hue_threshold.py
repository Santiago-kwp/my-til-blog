import numpy as np, cv2

def onThreshold(value):
    # 일단 두 트랙바의 값을 가져와 봅니다.
    t1 = cv2.getTrackbarPos("Hue_th1", "result")
    t2 = cv2.getTrackbarPos("Hue_th2", "result")

    # 아직 트랙바가 다 만들어지지 않아서 -1을 반환했다면 함수를 바로 종료합니다.
    # 이렇게 하면 초기값(th 배열)이 -1로 오염되는 것을 막을 수 있습니다.
    if t1 < 0 or t2 < 0:
        return

    # 정상적으로 값을 가져왔을 때만 th 배열에 저장합니다.
    th[0] = t1
    th[1] = t2

    ## OpenCV 이진화 함수 이용 - 상위 값과 하위 값 제거
    _, result = cv2.threshold(hue, th[1], 255, cv2.THRESH_TOZERO_INV)
    cv2.threshold(result, th[0], 255, cv2.THRESH_BINARY, result)
    cv2.imshow("result", result)

BGR_img = cv2.imread("images/color_space.jpg", cv2.IMREAD_COLOR)
if BGR_img is None: raise Exception("Could not open image")

HSV_img = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2HSV)  # 컬러 공간 변환
hue = np.copy(HSV_img[:, :, 0])                     # hue 행렬에 색상 채널 복사

th =[50, 100]          # 트랙바로 선택할 범위 변수
cv2.namedWindow("result")

# 1. 첫 번째 트랙바 생성 (onThreshold가 호출되지만, t2가 -1이라 안전하게 return 됨)
cv2.createTrackbar("Hue_th1", "result", th[0], 255, onThreshold)

# 2. 두 번째 트랙바 생성 (th[1]이 여전히 100으로 유지되어 있으므로 에러 없이 생성됨)
cv2.createTrackbar("Hue_th2", "result", th[1], 255, onThreshold)

# 두 트랙바가 정상적으로 만들어진 후 이진화 1회 명시적 실행
onThreshold(0)

cv2.imshow("BGR_img", BGR_img)
cv2.waitKey(0)
cv2.destroyAllWindows()