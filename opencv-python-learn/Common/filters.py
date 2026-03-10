import numpy as np, cv2

## 회선 수행 함수 - 행렬 처리 방식(속도 면에서 유리)
def filter(image, mask):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    ycenter, xcenter = mask.shape[0]//2, mask.shape[1]//2 # 마스크 중심 좌표

    for i in range(ycenter, rows - ycenter):    # 입력 행렬 반복 순회
        for j in range(xcenter, cols - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1 # 관심 영역 높이 범위
            x1, x2 = j - xcenter, j + xcenter + 1 # 관심 영역 너비 범위
            roi = image[y1:y2, x1:x2].astype(np.float32)    # 관심 영역 형변환
            tmp = cv2.multiply(roi, mask)   # 회선 적용 - 원소간 곱셈
            dst[i, j] = cv2.sumElems(tmp)[0]    # 출력 화소 저장
    return dst


def differential(image, data1, data2):
    mask1 = np.array(data1, np.float32).reshape(3, 3)
    mask2 = np.array(data2, np.float32).reshape(3, 3)

    dst1 = filter(image, mask1) # 사용자 정의 회선 함수
    dst2 = filter(image, mask2)
    dst = cv2.magnitude(dst1, dst2)

    dst = cv2.convertScaleAbs(dst)  # 절대값 및 형변환
    dst1 = cv2.convertScaleAbs(dst1)
    dst2 = cv2.convertScaleAbs(dst2)
    return dst, dst1, dst2


def erode(img, mask=None):
    dst = np.zeros(img.shape, np.uint8)
    if mask is None: mask = np.ones((3, 3), np.uint8)
    ycenter, xcenter = np.divmod(mask.shape[:2], 2)[0]  # 마스크 중심 좌표

    mcnt = cv2.countNonZero(mask)           # 마스크 값이 1인 원소의 개수
    for i in range(ycenter, img.shape[0] - ycenter):    # 입력 행렬 반복 순회
        for j in range(xcenter, img.shape[1] - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1   # 마스크 높이 범위
            x1, x2 = j - xcenter, j + xcenter + 1   # 마스크 너비 범위
            roi = img[y1:y2, x1:x2]                 # 마스크로 확인할 영역
            temp = cv2.bitwise_and(roi, mask)   # 논리곱으로 일치 원소 지정
            cnt = cv2.countNonZero(temp)        # 일치 원소 개수 계산
            dst[i, j] = 255 if (cnt == mcnt) else 0
    return dst


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
