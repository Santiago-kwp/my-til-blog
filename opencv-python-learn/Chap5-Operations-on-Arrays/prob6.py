import numpy as np, cv2

m1 = np.array([1, 2, 3, 1, 2, 3], np.int8)
m2 = np.array([3, 3, 4, 2, 2, 3], np.int8)
m3 = m1 + m2
m4 = m1 - m2

print("m1: ", m1, type(m1))
print("m2: ", m2)
print("m3: ", m3)
print("m4: ", m4)

data = [1, 2, 3, 4, 5, 6, 7, 8 ,9 , 10, 11, 12]
m1 = np.array(data).reshape(2,2,3)
r, g, b = cv2.split(m1)

print("[m1] = %s" % m1)
print("[r, g, b] = %s, %s, %s" % (r, g, b))