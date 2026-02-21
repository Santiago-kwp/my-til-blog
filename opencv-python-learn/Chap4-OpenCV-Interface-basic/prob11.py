import numpy as np, cv2

def onMouse(event, x, y, flags, param):
    global title, image
    # 현재 트랙바에서 굵기 값 읽기
    thickness = cv2.getTrackbarPos('Line Thickness', title)
    # 현재 트랙바에서 원의 반지름 값 얻기
    radius = cv2.getTrackbarPos('Circle Radius', title)

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(image, (x, y), (x + 30, y + 30), (255, 0, 0), thickness)
        cv2.imshow(title, image)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(image, (x, y), radius, (255, 0, 255), thickness)
        cv2.imshow(title, image)

def nothing(x): pass

title = "OpenCV Image"
image = np.ones((300, 300, 3), np.uint8) * 255 # 흰색 바탕 윈도우

cv2.namedWindow(title, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(title, onMouse)
cv2.createTrackbar('Line Thickness', title, 1, 10, nothing)
cv2.createTrackbar('Circle Radius', title, 1, 50, nothing)

cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()