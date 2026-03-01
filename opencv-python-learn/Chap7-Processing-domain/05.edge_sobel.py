import numpy as np, cv2

from Common.filters import differential

image = cv2.imread("images/edge.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Could not read image")

data1 = [-1, 0, 1,
         -2, 0, 2,
         -1, 0, 1]

data2 = [-1, -2, -1,
         0, 0, 0,
         1, 2, 1]
dst, dst1, dst2 = differential(image, data1, data2)

## OpenCV 제공 소벨 에지 계산
dst3 = cv2.Sobel(np.float32(image), cv2.CV_32F, 1, 0, 3) # x 방향 미분 - 수직 마스크
dst4 = cv2.Sobel(np.float32(image), cv2.CV_32F, 0, 1, 3) # y 방향 미분 - 수평 마스크
dst3 = cv2.convertScaleAbs(dst3)
dst4 = cv2.convertScaleAbs(dst4)

cv2.imshow("dst1- vertical mask", dst1)
cv2.imshow("dst2- horizontal mask", dst2)
cv2.imshow("dst3- vertical OpenCV", dst3)
cv2.imshow("dst4- horizontal OpenCV", dst4)
cv2.waitKey(0)
cv2.destroyAllWindows()
