import sys, os, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from Common.interpolation import rotate_pt

def calc_angle(pts): # 3개 좌표로 각도 계산 함수
    d1 = np.subtract(pts[1], pts[0]).astype(float)  # 두 좌표간 차분 계산
    d2 = np.subtract(pts[2], pts[0]).astype(float)
    angle1 = cv2.fastAtan2(d1[1], d1[0])    # 차분으로 각도 계산
    angle2 = cv2.fastAtan2(d2[1], d2[0])
    return (angle2 - angle1)                # 두 각도 간의 차분

def draw_point(x,y):        # 좌표 저장 및 그리기
    pts.append([x,y])
    print("좌표:", len(pts), [x,y])      # 클릭 좌표 표시
    cv2.circle(tmp, (x, y), 2, 255, 2)  # 중심 좌표 표시
    cv2.imshow("image", tmp)

def onMouse(event, x, y, flags, param):
    global tmp, pts
    if (event == cv2.EVENT_LBUTTONUP and len(pts)==0): draw_point(x,y)
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts)==1): draw_point(x,y)
    if (event == cv2.EVENT_LBUTTONUP and len(pts)==2): draw_point(x,y)

    if len(pts) == 3:
        angle = calc_angle(pts)
        print("회전각: %3.2f" % angle)
        dst = rotate_pt(image, angle, pts[0])
        cv2.imshow("image", dst)
        tmp = np.copy(image)    # 임시 행렬 초기화
        pts = []                # 클릭 좌표 초기화

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# 이미지 경로를 루트 기준으로 설정
image_path = os.path.join(project_root, "images", "rotate.jpg")
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)
