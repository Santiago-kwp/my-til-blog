import numpy as np, cv2

def onMouse(event, x, y, flags, param):
    global title, image
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(image, (x, y), (x + 30, y + 30), (255, 0, 0), 2)
        cv2.imshow(title, image)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(image, (x, y), 20, (255, 0, 255), 2)
        cv2.imshow(title, image)

title = "OpenCV Image"
image = np.ones((300, 300, 3), np.uint8) * 255 # 흰색 바탕 윈도우

cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(title, onMouse)
cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()