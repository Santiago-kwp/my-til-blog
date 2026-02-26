import numpy as np
import timeit

# 단일 픽셀 (BGR 값)
bgr = np.array([100, 150, 200], dtype=np.uint8)

# 전체 배열을 float으로 변환
def use_astype():
    B, G, R = bgr.astype(float)
    return B, G, R

# 개별 요소만 float 변환
def use_float_each():
    B, G, R = float(bgr[0]), float(bgr[1]), float(bgr[2])
    return B, G, R

# 실행 시간 측정
t_astype = timeit.timeit(use_astype, number=1000000)
t_float_each = timeit.timeit(use_float_each, number=1000000)

print(f"astype(float): {t_astype:.4f} sec")
print(f"float(bgr[i]): {t_float_each:.4f} sec")



# 큰 배열 준비 (1000x1000, 값은 0~255)
img = np.random.randint(0, 256, size=(1000, 1000, 3), dtype=np.uint8)

# 전체 배열을 float으로 변환 (이미지 전체)
def use_astype():
    arr_float = img.astype(float)
    return arr_float

# 픽셀 단위로 float 변환 (루프 방식)
def use_float_each():
    h, w, _ = img.shape
    result = np.empty((h, w, 3), dtype=float)
    for i in range(h):
        for j in range(w):
            B, G, R = float(img[i, j, 0]), float(img[i, j, 1]), float(img[i, j, 2])
            result[i, j] = [B, G, R]
    return result

# 실행 시간 측정
t_astype = timeit.timeit(use_astype, number=10)
t_float_each = timeit.timeit(use_float_each, number=10)

print(f"astype(float): {t_astype:.4f} sec")
print(f"float(bgr[i]) loop: {t_float_each:.4f} sec")

