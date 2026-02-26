import cv2

img1 = cv2.imread("images/add1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("images/add2.jpg", cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
cv2.createTrackbar("image1", "dst", 50, 100, lambda x: None)
cv2.createTrackbar("image2", "dst", 50, 100, lambda x: None)

while True:
    w1 = cv2.getTrackbarPos("image1", "dst") / 100
    w2 = cv2.getTrackbarPos("image2", "dst") / 100
    dst = cv2.addWeighted(img1, w1, img2, w2, 0)
    cv2.imshow("dst", dst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()