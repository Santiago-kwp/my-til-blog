import numpy as np
import cv2

image = cv2.imread("images/color.jpg",cv2.IMREAD_COLOR)    # 영상 읽기
if image is None: raise Exception("Could not read image from /images/color.jpg")
if image.ndim != 3: raise Exception("컬러 영상 아님")

bgr = cv2.split(image)  # 채널 분리: 컬러 영상 -> 3채널 분리
# blue, green, red = cv2.split(image)
print("bgr 자료형:", type(bgr), type(bgr[0]), type(bgr[0][0][0]))  # tuple, numpy,ndarray, numpy.uint8
print("bgr 원소개수: %s" % len(bgr))

## 각 채널을 윈도우에 띄우기
cv2.imshow("image", image)
cv2.imshow("Blue channel", bgr[0])      # Blue 채널 ~ 원본 영상의 파란색 부분이 밝게 나타남
cv2.imshow("Green channel", bgr[1])     # Green 채널
cv2.imshow("Red channel", bgr[2])       # Red 채널

cv2.waitKey(0)
cv2.destroyAllWindows()