import cv2, numpy as np

def onChange(x):
    pass

img1 = cv2.imread("images/add1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("images/add2.jpg", cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('dst',cv2.WINDOW_NORMAL)
cv2.createTrackbar("image1", "dst", 0, 100, onChange)
cv2.createTrackbar("image2", "dst", 0, 100, onChange)
cv2.setTrackbarPos("image1", "dst", 50)
cv2.setTrackbarPos("image2", "dst", 50)
dst = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

while True:
    w1 = cv2.getTrackbarPos("image1", "dst")
    w2 = cv2.getTrackbarPos("image2", "dst")
    cv2.addWeighted(img1, w1/100, img2, w2/100, 1, dst)
    cv2.imshow("dst", dst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()