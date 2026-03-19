import numpy as np
import cv2, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Common.interpolation import scaling

def scaling_nearest(img, size):
    """
    OpenCV나 일반적인 그래픽스에서 이미지의 크기(size)를 지정할 때는 x축(가로, Width) 먼저, y축(세로, Height) 
    예: 해상도가 800x600인 이미지라면 size = (800, 600)

    반면, 파이썬의 NumPy 배열에서 형태(shape)를 정의할 때는 행(Row, 세로, y축) 먼저, 열(Column, 가로, x축) 나중의 순서로 표현합니다.
    예: 높이가 600, 폭이 800인 빈 이미지를 만들려면 행렬 크기는 (600, 800)이 되어야 합니다.
    """
    dst = np.zeros(size[::-1], img.dtype)   # 행렬과 크기는 원소가 역순
    ratioY, ratioX = np.divide(size[::-1], img.shape[:2])   # 변경 크기 비율
    i = np.arange(0, size[1], 1)    # 목적 영상 세로(i) 좌표 생성
    j = np.arange(0, size[0], 1)    # 목적 영상 가로(j) 좌표 생성
    i, j = np.meshgrid(i, j)
    y, x = np.int32(i / ratioY), np.int32(j / ratioX)   # 입력 영상 좌표
    dst[i, j] = img[y, x]       # 역방향 사상 -> 입력 영상 좌표 계산

    return dst


# 프로젝트 루트 경로 (현재 파일 기준으로 상위 디렉토리까지 올라감)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# 이미지 경로를 루트 기준으로 설정
image_path = os.path.join(project_root, "images", "interpolation.jpg")
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

dst1 = scaling(image, (350, 400))   # 크기 변경 - 기본
dst2 = scaling_nearest(image, (350, 400))   # 크기 변경 - 최근접 이웃 보간

cv2.imshow("image", image)
cv2.imshow("dst1- forward mapping", dst1)
cv2.imshow("dst2 - NN interpolation", dst2)

cv2.waitKey(0)