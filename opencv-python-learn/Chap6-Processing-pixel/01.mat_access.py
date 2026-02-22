import numpy as np

def mat_access1(mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            k = mat[i, j]
            mat[i, j] = k * 2   # 원소 할당

mat = np.arange(10).reshape(2, 5)   # 0 ~ 10 사이 원소 생성

print("원소 처리 전: \n%s\n" % mat)
mat_access1(mat)
print("원소 처리 후: \n%s\n" % mat)