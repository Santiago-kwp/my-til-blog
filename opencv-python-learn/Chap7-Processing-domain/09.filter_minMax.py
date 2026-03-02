import numpy as np, cv2

def minmax_filter(image, ksize, mode):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.uint8)
    center = ksize // 2

    for i in range(center, rows-center):    # 입력 영상 순회
        for j in range(center, cols-center):
            ## 마스크 영역의 행렬 처리 방식
            y1, y2 = i - center, i + center + 1 # 마스크 높이 범위
            x1, x2 = j - center, j + center + 1 # 마스크 너비 범위
            mask = image[y1:y2, x1:x2]
            dst[i, j] = cv2.minMaxLoc(mask)[mode] # 최소 or 최대
    return dst

image = cv2.imread("images/min_max.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("mine.jpg not found")

minfilter_img = minmax_filter(image, 3, 0)  # 3x3 마스크 최솟값  필터링
maxfilter_img = minmax_filter(image, 3, 1)

cv2.imshow("image", image)
cv2.imshow("minfilter", minfilter_img)
cv2.imshow("maxfilter", maxfilter_img)
cv2.waitKey(0)
cv2.destroyAllWindows()