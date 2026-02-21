import numpy as np, cv2

""" 기존 코드 
def onMouse(event, x, y, flags, params):
    global title
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, pt, 5, 100, 1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.rectangle(image, pt, pt+(30, 30), 100, 2)
        cv2.imshow(title, image)
"""

def onMouse(event, x, y, flags, params):
    global title, image
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x,y), 5, 100, 1)
        cv2.imshow(title, image)    # 원 그린 후 업데이트
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.rectangle(image, (x,y), (x+30,y+30), 100, 2)
        cv2.imshow(title, image)    # 사각형 그린 후 업데이트

image = np.ones((300, 300), np.uint8) * 255

title = "Draw Event"
cv2.namedWindow(title)
cv2.imshow(title, image)
cv2.setMouseCallback(title, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()