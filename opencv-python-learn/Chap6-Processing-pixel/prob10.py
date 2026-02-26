import numpy as np, cv2

image1 = np.zeros((50, 512), np.float32) # 50 X 512 영상 생성, float32
rows, cols = image1.shape[:2]

for i in range(rows):
    for j in range(cols):
        image1[i,j] = j / (cols-1)  # 화소값 점진적 증가

cv2.imshow("image1", image1)
cv2.waitKey(0)
cv2.destroyAllWindows()