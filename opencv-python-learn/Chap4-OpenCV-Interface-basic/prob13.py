import numpy as np, cv2
import os
print(os.getcwd())
print(os.path.exists("images"))

image = np.ones((512, 512, 3), np.uint8)*255

title = 'KoreaFlag'

cv2.namedWindow(title)
cv2.ellipse(image, (256, 256), (100, 100), 0, 0, -180, (0, 0, 255), -1)
cv2.ellipse(image, (256, 256), (100, 100), 0, 0, 180, (255, 0, 0), -1)
cv2.ellipse(image, (256-50, 256), (50, 50), 0, 0, 180, (0, 0, 255), -1)
cv2.ellipse(image, (256+50, 256), (50, 50), 0, 0, -180, (255, 0, 0), -1)

params_jpg = (cv2.IMWRITE_JPEG_QUALITY, 100)
params_png = (cv2.IMWRITE_PNG_COMPRESSION, 9)

ret_jpg = cv2.imwrite("images/koreaFlag.jpg", image, params_jpg)
ret_png = cv2.imwrite("images/koreaFlag.png", image, params_png)

# True가 나오면 정상 저장, False가 나오면 실패
print(f"JPG 저장 성공 여부: {ret_jpg}")
print(f"PNG 저장 성공 여부: {ret_png}")

cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()

