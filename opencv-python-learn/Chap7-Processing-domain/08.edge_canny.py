import numpy as np, cv2

def nonmax_suppression(sobel, direct):  # 비최대치 억제 함수
    rows, cols = sobel.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            ## 관심 영역 참조 통해 이웃 화소 가져오기
            values = sobel[i - 1:i + 2, j - 1:j + 2].flatten()  # 중심 에지 주변 9개 화소 가져옴
            first = [3, 0, 1, 2]    # 첫 이웃 화소 좌표 4개
            id = first[direct[i, j]]    # 방향에 따른 첫 이웃화소 위치
            v1, v2 = values[id], values[8-id]   # 두 이웃 화소 가져옴

            ## if 문으로 이웃 화소 가져오기
            """
            if direct[i, j] == 0:   # 기울기 방향 0도
                v1, v2 = sobel[i, j-1], sobel[i, j+1]
            if direct[i, j] == 1:   # 기울기 방향 45도
                v1, v2 = sobel[i-1, j-1], sobel[i+1, j+1]
            if direct[i, j] == 2:   # 기울기 방향 90도
                v1, v2 = sobel[i-1, j], sobel[i+1, j]
            if direct[i, j] == 3:   # 기울기 방향 135도
                v1, v2 = sobel[i+1, j-1], sobel[i-1, j+1]
            """
            dst[i, j] = sobel[i, j] if (v1 < sobel[i, j] > v2) else 0 # 최대치 억제

    return dst

def trace(max_sobel, i, j, low):    # 에지 추적 함수
    h, w = max_sobel.shape
    if (0 <= i < h and 0 <= j < w) == False: return # 추적 화소 범위 확인
    if pos_ck[i, j] == 0 and max_sobel[i, j] > low:  # 추적 조건 확인
        pos_ck[i, j] = 255   # 추적 좌표 완료 표시
        canny[i, j] = 255    # 에지 지정

        trace(max_sobel, i - 1, j - 1, low) # 재귀 호출 - 8방향 추적
        trace(max_sobel, i, j - 1, low)
        trace(max_sobel, i + 1, j - 1, low)
        trace(max_sobel, i - 1, j, low)
        trace(max_sobel, i + 1, j, low)
        trace(max_sobel, i - 1, j + 1, low)
        trace(max_sobel, i, j + 1, low)
        trace(max_sobel, i + 1, j + 1, low)

def hysteresis_th(max_sobel, low, high): # 이력 임계 처리 수행 함수
    rows, cols = max_sobel.shape[:2]
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if max_sobel[i, j] >= high: trace(max_sobel, i, j, low) # 높은 임계값 이상 시 추적

image = cv2.imread("images/canny.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("Canny image is None")

pos_ck = np.zeros(image.shape[:2], np.uint8) # 추적 완료 점검 행렬
canny = np.zeros(image.shape[:2], np.uint8)  # 캐지 에지 행렬

## 캐니 에지 검출
gaus_img = cv2.GaussianBlur(image, (5, 5), 0.3)
Gx = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 1, 0, 3)   # x 방향 마스크
Gy = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 0, 1, 3)   # y 방향 마스크
sobel = cv2.magnitude(Gx, Gy)                                         # 두 행렬 벡터 크기

directs = cv2.phase(Gx, Gy)  / (np.pi/4)        # 에지 기울기 계산 및 근사 - phase() 함수로 Gx 행렬과 Gy 행렬의 원소간 각도를 계산한다. 각도는 라디안 값으로 계산되기에 45간격으로 근사하려면 pi/4로 나누어서 정수형으로 변환한다.
directs = directs.astype(int) % 4               # 8방향 -> 4방향 축소 - 나머지 연산자를 이용해서 8개 값으로 근사된 각도를 0~3까지의 값을 갖도록 한다. 즉 45도와 135도는 1이 되고, 90도와 270도는 2가 된다.
max_sobel = nonmax_suppression(sobel, directs)  # 비최대치 억제
hysteresis_th(max_sobel, 100, 150)      # 이력 임계값

canny2 = cv2.Canny(image, 100, 150)     # OpenCV 캐니 에지 검출


cv2.imshow("image", image)
cv2.imshow("canny", canny)
cv2.imshow("OpenCV_Canny", canny2)
cv2.waitKey(0)
cv2.destroyAllWindows()