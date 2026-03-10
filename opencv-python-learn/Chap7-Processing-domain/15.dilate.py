import numpy as np, cv2

def dilate(img, mask=None):
    dst = np.zeros(img.shape, np.uint8)
    if mask is None: mask = np.ones((3, 3), np.uint8)
    ycenter, xcenter = np.divmod(mask.shape[:2], 2)[0]  # 마스크 중심 좌표

    for i in range(ycenter, img.shape[0] - ycenter):    # 입력 행렬 반복 순회
        for j in range(xcenter, img.shape[1] - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1   # 마스크 높이 범위
            x1, x2 = j - xcenter, j + xcenter + 1   # 마스크 너비 범위
            roi = img[y1:y2, x1:x2]                 # 마스크로 확인할 영역
            temp = cv2.bitwise_and(roi, mask)   # 논리곱으로 일치 원소 지정
            cnt = cv2.countNonZero(temp)        # 일치 원소 개수 계산
            dst[i, j] = 0 if (cnt == 0) else 255
    return dst

image = cv2.imread("images/morph.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Could not read image")

data = [0, 1, 0,
        1, 1, 1,
        0, 1, 0]    # 마스크 원소 지정

mask = np.array(data, np.uint8).reshape(3,3)
th_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]   # 영상 이진화
dst1 = dilate(th_img, mask) # 사용자 정의 침식 함수
dst2 = cv2.dilate(th_img, mask) # OpenCV의 침식 함수
# dst2 = cv2.morphologyEx(th_img, cv2.MORPH_DILATE, mask) # OpenCV의 침식 함수2

cv2.imshow("image", image)
cv2.imshow("binary image", th_img)
cv2.imshow("User dilate", dst1)
cv2.imshow("OpenCV dilate", dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()
