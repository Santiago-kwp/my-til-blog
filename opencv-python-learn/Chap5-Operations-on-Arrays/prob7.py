import numpy as np, cv2

logo = cv2.imread("images/logo.jpg", cv2.IMREAD_COLOR)
if logo is None: raise Exception("logo not found")

blue, green, red = cv2.split(logo)

# 빈 채널 생성
# 채널 합성
ch0 = np.zeros(logo.shape[:2], dtype=np.uint8)

# 빈 채널 생성 (logo와 동일한 크기, 0으로 채움) - 다른 방법!
zeros = np.zeros_like(blue)

blue_img = cv2.merge((blue, ch0, ch0))
green_img = cv2.merge((ch0, green, ch0))
red_img = cv2.merge((ch0, ch0, red))

cv2.imshow("logo", logo)
cv2.imshow("blue", blue_img)
cv2.imshow("green", green_img)
cv2.imshow("red", red_img)

cv2.waitKey(0)
cv2.destroyAllWindows()