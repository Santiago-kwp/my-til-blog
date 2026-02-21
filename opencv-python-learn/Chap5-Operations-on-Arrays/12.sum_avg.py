import numpy as np, cv2

image = cv2.imread("images/sum_test.jpg", cv2.IMREAD_COLOR)
if image is None: raise ValueError("image is None")

mask = np.zeros(image.shape[:2], np.uint8)
mask[60:160, 20:120] = 255

sum_value = cv2.sumElems(image)     # 채널별 합 - 튜플로 반환
mean_value1 = cv2.mean(image)       # 채널별 평균 - 튜플로 반환
mean_value2 = cv2.mean(image, mask)
print("sum_value 자료형:", type(sum_value), type(sum_value[0])) # 결과 행렬의 자료형
print("[sum_value] =", sum_value)
print("[mean_value1] =", mean_value1)
print("[mean_value2] =", mean_value2)

## 평균과 표준편차 결과 저장
mean, stddev = cv2.meanStdDev(image)
mean2, stddev2 = cv2.meanStdDev(image, mask=mask)
print("mean 자료형:", type(mean), type(mean[0][0]))    # 반환 행렬 자료형, 원소 자료형
print("[mean] =", mean.flatten())                    # 백터 변환 후 출력
print("[stddev] =", stddev.flatten())

print("[mean2] =", mean2.flatten())
print("[stddev2] =", stddev2.flatten())

cv2.imshow("image", image)
cv2.imshow("mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()