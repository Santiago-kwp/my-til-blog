import cv2, numpy as np


def calc_histo(image, hsize, ranges=[0, 256]):
    hist = np.zeros((hsize, 1), np.float32)  # 히스토그램 누적 행렬
    gap = ranges[1]/hsize   # 계급 간격, hsize : 간격 수 -> hsize=256 → gap=1, 즉 각 밝기 값마다 하나의 bin.

    for i in (image/gap).flat: # .flat → NumPy 배열을 1차원 반복자로 펼쳐서 모든 화소를 순회.
        hist[int(i)] += 1 # 예: 화소값이 200이고 gap=4라면 200/4 = 50, 즉 50번째 bin에 속함.
    return hist