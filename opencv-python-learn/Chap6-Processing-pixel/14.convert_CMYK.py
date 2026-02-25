import numpy as np, cv2

BGR_img = cv2.imread("images/color_model.jpg", cv2.IMREAD_COLOR)
if BGR_img is None: raise ValueError("Cannot read the image")

white = np.array([255, 255, 255], np.uint8)
CMY_img = white - BGR_img
CMY = cv2.split(CMY_img)

black = cv2.min(CMY[0], cv2.min(CMY[1], CMY[2]))    # 원소 간의 최솟값 저장
Yellow, Magenta, Cyan = CMY-black   # 3개 행렬 화소값 차분

titles = ["black", "Yellow", "Magenta", "Cyan"]
for t in titles:
    cv2.imshow(t, eval(t))

cv2.waitKey(0)
cv2.destroyAllWindows()