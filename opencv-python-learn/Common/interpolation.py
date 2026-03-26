import numpy as np

def scaling(img, size):
    dst = np.zeros(size[::-1], img.dtype)   # size와 shape는 원소 역순
    ratioY, ratioX = np.divide(size[::-1], img.shape[:2])   # 비율 계산
    y = np.arange(0, img.shape[0], 1)   # 입력 영상 세로(y) 좌표 생성
    x = np.arange(0, img.shape[1], 1)   # 입력 영상 가로(x) 좌표 생성
    y, x = np.meshgrid(y, x)            # i, j 좌표에 대한 좌표 행렬 생성
    i, j = np.int32(y * ratioY), np.int32(x * ratioX)   # 목적 영상 좌표
    dst[i, j] = img[y, x]               # 정방향 사상 -> 목적 영상 좌표 계산
    return dst

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

