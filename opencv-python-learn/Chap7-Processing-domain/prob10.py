import numpy as np, cv2
from Common.filters import filter

img = cv2.imread("images/filter_sharpen.jpg", cv2.IMREAD_COLOR)
print(img.shape)
# 사용자 정의 커널 생성 (예: 평균 필터)
kernel = np.ones((5, 5), np.float32) / 25
kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) # 3x3 샤프닝

dst = cv2.filter2D(img, -1, kernel)
dst2 = cv2.filter2D(img, -1, kernel2)

b = filter(img[:,:,0], kernel)
g = filter(img[:,:,1], kernel)
r = filter(img[:,:,2], kernel)
dst3 = np.stack((b, g, r), axis=2)
dst3 = np.clip(dst3, 0, 255).astype(np.uint8) # 0~255 범위 제한 후 uint8 형변환


cv2.imshow("original", img)
cv2.imshow('Filtered Image - 5x5 avg', dst)
cv2.imshow('Filtered Image - 3x3 sharpening', dst2)
cv2.imshow('Filtered Image - 5x5 avg - User defined', dst3)


cv2.waitKey(0)
cv2.destroyAllWindows()