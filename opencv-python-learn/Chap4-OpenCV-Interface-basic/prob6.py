import cv2
import numpy as np

image = np.zeros((300, 400), dtype=np.uint8)
image.fill(100)
title = 'PROBLEM6'
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)

cv2.imshow(title, image)
cv2.resizeWindow(title, 500, 600)


cv2.waitKey(0)
cv2.destroyAllWindows()

