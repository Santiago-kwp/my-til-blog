import numpy as np, cv2, time

def pixel_access1(image):
    image1 = np.zeros(image.shape[:2], image.dtype) # image.shape  → (rows, cols, channels) // image.shape[:2] → (rows, cols)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = image[i, j]     # 화소 접근
            image1[i, j] = 255 - pixel # 화소 할당
    return image1

def pixel_access2(image):   # 룩업테이블 이용 방법
    lut = [255 - i for i in range(256)]  # 룩업테이블 생성
    lut = np.array(lut, np.uint8)
    image3 = lut[image]
    return image3

def pixel_access3(image):   # OpenCV 함수 이용 방법
    image4 = cv2.subtract(255, image)
    return image4

def pixel_access4(image):   # ndarray 산술 연산 방법
    image5 = 255 - image
    return image5

image = cv2.imread("images/bright.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

## 수행시간 체크 함수
def time_check(func, msg):
    start_time = time.perf_counter()
    ret_img = func(image)
    elapsed = (time.perf_counter() - start_time) * 1000
    print(msg, "수행시간 : %0.2f ms" % elapsed)
    return ret_img

image1 = time_check(pixel_access1, "[방법1] 직접 접근 방식")
image2 = time_check(pixel_access2, "[방법2] 룩업테이블 방식")
image3 = time_check(pixel_access3, "[방법3] OpenCV 함수 방식")
image4 = time_check(pixel_access4, "[방법4] ndarray 연산 방식")

# 결과 영상 보기
cv2.imshow("image - original", image)
cv2.imshow("image1 - directly access to pixel", image1)
cv2.imshow("image2 - LUT", image2)
cv2.imshow("image3 - LUT", image3)
cv2.imshow("image4 - ndarray", image4)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
[방법1] 직접 접근 방식 수행시간 : 31.67 ms
[방법2] 룩업테이블 방식 수행시간 : 0.26 ms
[방법3] OpenCV 함수 방식 수행시간 : 1.88 ms
[방법4] ndarray 연산 방식 수행시간 : 0.17 ms
"""
