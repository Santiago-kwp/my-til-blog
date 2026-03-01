import numpy as np, cv2

image = cv2.imread("images/laplacian.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("Could not read the image")

data1 = [ [0, 1, 0],
          [1, -4, 1],
          [0, 1, 0]]    # 4방향 필터

data2 = [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]] # 8방향 필터

mask4 = np.array(data1, np.int16)   # 음수로 인해 int16형 행렬 선언
mask8 = np.array(data2, np.int16)

dst1 = cv2.filter2D(image, cv2.CV_16S, mask4) # OpenCV 회선 함수 호출
dst2 = cv2.filter2D(image, cv2.CV_16S, mask8)
dst3 = cv2.Laplacian(image, cv2.CV_16S, 1)  # OpenCV 라플라시안 수행 함수, 1을 지정하면 3x3 기본 마스크

cv2.imshow("image", image)
cv2.imshow("filter2D 4-direction", cv2.convertScaleAbs(dst1))
cv2.imshow("filter2D 8-direction", cv2.convertScaleAbs(dst2))
cv2.imshow("Laplacian_OpenCV", cv2.convertScaleAbs(dst3))
cv2.waitKey(0)
cv2.destroyAllWindows()