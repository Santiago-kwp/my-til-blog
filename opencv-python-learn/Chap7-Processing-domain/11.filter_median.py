import numpy as np, cv2

def median_filter(image, size):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.uint8)
    center = size // 2

    for i in range(center, rows - center):
        for j in range(center, cols - center):
            y1, y2 = i - center, i + center + 1
            x1, x2 = j - center, j + center + 1
            mask = image[y1:y2, x1:x2].flatten()    # 관심 영역 지정 및 벡터 변환

            sort_mask = cv2.sort(mask, cv2.SORT_EVERY_COLUMN).flatten() # 정렬 수행
            dst[i, j] = sort_mask[sort_mask.size//2]    # 출력 화소로 지정

    return dst


def salt_pepper_noise(img, n):
    h, w = img.shape[:2]
    x, y = np.random.randint(0, w, n), np.random.randint(0, h, n)
    noise = img.copy()
    for (x, y) in zip(x, y):
        noise[y, x] = 0 if np.random.rand() < 0.5 else 255

    return noise


image = cv2.imread("images/median.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("mine.jpg not found")

noise = salt_pepper_noise(image, 500)   # 소금 - 후추 잡음 영상 생성
med_img1 = median_filter(noise, 5)    # 사용자 정의 함수
med_img2 = cv2.medianBlur(noise, 5)  # OpenCV 제공 함수

cv2.imshow("image", image)
cv2.imshow("noise", noise)
cv2.imshow("median - User", med_img1)
cv2.imshow("median - OpenCV", med_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()