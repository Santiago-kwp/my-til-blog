import numpy as np


def calc_histo(image, channels, bsize, ranges):
    shape = bsize if len(channels) > 1 else (bsize[0], 1)
    hist = np.zeros(shape, np.int32) # 히스토그램 누적 행렬
    gap = np.divide(ranges[1::2], bsize) # 계급 간격

    for row in image:          # 2차원 행렬 순회 방식
        for val in row:
            idx = np.divide(val[channels], gap).astype('uint')
            hist[tuple(idx)] += 1

    return hist

