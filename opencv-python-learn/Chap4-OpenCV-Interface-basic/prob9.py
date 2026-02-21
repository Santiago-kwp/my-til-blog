import numpy as np, cv2

# 3채널 컬러 이미지 생성해야 함
image = np.zeros((600, 400, 3), np.uint8)
image[:] = 255
title = "OpenCV Image"

cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)


cv2.rectangle(image, (100, 100), (300, 400), (0, 0, 255), cv2.FILLED)

cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()

