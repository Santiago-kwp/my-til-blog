import cv2
import numpy as np

image = np.zeros((300, 400), np.uint8)
image[:] = 100

title = 'Window'
cv2.namedWindow(title, cv2.WINDOW_NORMAL)
cv2.moveWindow(title, 100, 200)
cv2.imshow(title, image)

image = np.zeros((400, 600, 3), np.uint8)
image[:] = (255, 255, 255)
pt1, pt2 = (50, 100), (200, 300)

cv2.line(image, pt1, pt2, (0, 255,0), 5)
cv2.rectangle(image, pt2, (300, 400), (0,0,255), -1, cv2.LINE_4, 1)

cv2.imshow("Line & Rectangle", image)
cv2.waitKey(0)
cv2.destroyAllWindows()