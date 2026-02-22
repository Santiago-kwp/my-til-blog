import cv2, numpy as np

"""
다음의 연립방정식을 가우시안 소거법의 역함수를 계산해서 해를 구하는 프로그램을 작성하시오
연립방정식
3x_1 + 6x_2 + 3x_3 = 2
-5x_1 + 6x_2 + x_3 = 10
2x_1 - 3x_2 + 5x_3 = 28
"""

A = np.array([[3, 6, 3], [-5, 6, 1], [2, -3, 5]], np.float32)
b = np.array([2, 10, 28], np.float32)

ret, A_inv = cv2.invert(A, cv2.DECOMP_LU) # LU 분해 기반 역행렬

if ret:
    x = A_inv @ b # 행렬곱
    print("해:", x)
else:
    print("역행렬이 존재하지 않습니다.")

"""
파이썬에서 @ 연산자는 행렬 곱(matrix multiplication)을 의미합니다.

📌 의미
A @ B → 두 배열(또는 행렬) 간의 행렬 곱을 수행합니다.

이는 np.dot(A, B) 또는 np.matmul(A, B)와 같은 동작입니다.
"""

# 직접 연립방정식 풀이
_, x = cv2.solve(A, b, cv2.DECOMP_LU)
print("해:", x.flatten())