import numpy as np, cv2
from Common.histogram import draw_histo

image = cv2.imread("images/pixel.jpg", cv2.IMREAD_GRAYSCALE)


red0 = cv2.reduce(image, dim=0, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S) # 화소값의 덧셈인 경우 숫자가 커지므로 uint8에 담을 수 없음
red1 = cv2.reduce(image, dim=1, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S)

print(red0.shape, red1.shape)

norm0 = cv2.normalize(red0, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
norm1 = cv2.normalize(red1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

hist0 = cv2.calcHist(norm0, [0], None, [64], [0, 256])
hist1 = cv2.calcHist([norm1], [0], None, [64], [0, 256])

hist0_img = draw_histo(hist0)
hist1_img = draw_histo(hist1)
cv2.imshow("hist0", hist0_img)
cv2.imshow("hist1", hist1_img)


cv2.waitKey(0)
cv2.destroyAllWindows()
