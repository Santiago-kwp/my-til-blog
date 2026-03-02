import cv2

def onTrackbar(th):
    edge = cv2.GaussianBlur(gray, (5, 5), 0)    # 가우시안 블러링
    edge = cv2.Canny(edge, th, th*2, 5) # 캐니 에지 검출

    color_edge = cv2.copyTo(image, mask=edge)   # 입력 행렬에 대해서 mask 원소가 1이상인 위치만 복사한다. 즉, 에지 행렬(edge)에서 흰색인 위치의 image 행렬의 원소만 복사되어 color_edge 행렬을 생성한다.
    dst = cv2.hconcat([image, color_edge])      # 하나의 창에 입력 영상과 컬러 에지 영상을 모두 표시하기 위해 가로 방향으로 병합하여 하나의 행렬을 만듦
    cv2.imshow("color edge", dst)

image = cv2.imread("images/smoothing.jpg", cv2.IMREAD_COLOR)
if image is None: raise ValueError("mine.jpg not found")

th = 50
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 명암도 영상으로 변환
dst = cv2.hconcat([image, image])
cv2.imshow("color edge", dst)
cv2.createTrackbar("Canny th", "color edge", th, 150, onTrackbar)
onTrackbar(th)  # 콜백 함수 첫 실행
cv2.waitKey(0)
cv2.destroyAllWindows()