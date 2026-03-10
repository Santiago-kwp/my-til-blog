import numpy as np, cv2

from Common.filters import erode, dilate

def opening(img, mask): # 열림 연산 함수
    tmp = erode(img, mask)  # 침식
    dst = dilate(tmp, mask) # 팽창
    return dst

def closing(img, mask): # 닫힘 연산 함수
    tmp = dilate(img, mask)
    dst = erode(tmp, mask)
    return dst

image = cv2.imread("images/morph.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Could not read image")

mask = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
th_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]

dst1 = opening(th_img, mask)
dst2 = closing(th_img, mask)
dst3 = cv2.morphologyEx(th_img, cv2.MORPH_OPEN, mask)
dst4 = cv2.morphologyEx(th_img, cv2.MORPH_CLOSE, mask, iterations=1) # 닫힘 함수

cv2.imshow("User_opening", dst1); cv2.imshow("User_closing", dst2)
cv2.imshow("OpenCV_opening", dst3); cv2.imshow("OpenCV_closing", dst4)
cv2.waitKey(0)
cv2.destroyAllWindows()

