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
