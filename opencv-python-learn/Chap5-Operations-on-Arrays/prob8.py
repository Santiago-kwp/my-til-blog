import numpy as np, cv2

image = cv2.imread("images/color.jpg", cv2.IMREAD_COLOR)
if image is None: raise ValueError("Could not read the image")

mask = np.zeros(image.shape[:2], dtype=np.uint8)
center = (190, 170)

## 특정 영역의 타원만을 복사하여 새 창에 표시
cv2.ellipse(mask, center, (80, 100), 0, 0, 360, 255, -1)
dst = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("dst", dst)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
