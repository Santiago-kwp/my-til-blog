import numpy as np, cv2

data = [3, 0, 6, -3, 4, 2, -5, -1, 9]   # 연립방정식의 계수들
m1 = np.array(data, np.float32).reshape(3,3)    # 계수들을 행렬로 생성
m2 = np.array([36, 10, 28], np.float32)  # 상수 벡터

ret, inv = cv2.invert(m1, cv2.DECOMP_LU)
if ret:
    dst1 = inv.dot(m2)  # numpy 제공 행렬곱 함수
    dst2 = cv2.gemm(inv, m2, 1, None, 1)    # OpenCV 제공 행렬곱 함수
    _, dst3 = cv2.solve(m1, m2, cv2.DECOMP_LU)               # 연립방정식 풀이

    print("[inv] \n%s\n" % inv)
    print("[dst1] \n%s\n" % dst1.flatten()) # 행렬을 벡터로 변환
    print("[dst2] \n%s\n" % dst2.flatten())
    print("[dst3] \n%s\n" % dst3.flatten())
else:
    print("역행렬이 존재하지 않습니다.")