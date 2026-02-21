import numpy as np, cv2

x = np.array([1, 2, 3 ,5, 10], np.float32)  # 리스트로 ndarray 객체 생성
y = np.array([2, 5, 6, 2, 9]).astype("float32")    # 행렬 생성 후 실수형 변환

mag = cv2.magnitude(x, y)   # 크기 계산
ang = cv2.phase(x, y)       # 각도(방향) 계산
p_mag, p_ang = cv2.cartToPolar(x, y)    # 극 좌표로 변환
x2, y2 = cv2.polarToCart(p_mag, p_ang)  # 직교좌표로 변환

print("[x] 형태: %s 원소: %s" % (x.shape, x))       # 1차원 행렬
print("[y] 형태: %s 원소: %s" % (y.shape, y))       # 1차원 행렬
print("[mag] 형태: %s 원소: %s" % (mag.shape, mag)) # 2차원 열벡터

print(">>> 열벡터를 1행에 출력하는 방법")
print("[m_mag] = %s" % mag.transpose())
print("[p_mag] = %s" % np.ravel(p_mag)) # ravel() 함수로 전개
print("[p_ang] = %s" % np.ravel(p_ang)) # ravel() 함수로 전개
print("[x_mat2] = %s" % x2.flatten())
print("[y_mat2] = %s" % y2.flatten())
