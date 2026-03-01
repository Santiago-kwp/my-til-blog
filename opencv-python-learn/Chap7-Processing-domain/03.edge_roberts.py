import numpy as np, cv2

from Common.filters import filter

def differential(image, data1, data2):
    mask1 = np.array(data1, np.float32).reshape(3, 3)   # 입력 인자로 마스크 원소 초기화
    mask2 = np.array(data2, np.float32).reshape(3, 3)

    dst1 = filter(image, mask1)     # 저자 구현 회선 함수 호출
    dst2 = filter(image, mask2)
    dst1, dst2 = np.abs(dst1), np.abs(dst2) # 회선 결과 행렬 양수 변경
    dst = cv2.magnitude(dst1, dst2) # 두 행렬의 크기 계산

    dst = np.clip(dst, 0 ,255).astype(np.uint8) # 윈도우 영상 표시 위한 형변환 및 클리핑
    dst1 = np.clip(dst1, 0 ,255).astype(np.uint8)
    dst2 = np.clip(dst2, 0 ,255).astype(np.uint8)
    return dst, dst1, dst2

image = cv2.imread("images/edge.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("Could not read image")

data1 = [-1,0,0,
         0,1,0,
         0,0,0]
data2 = [0,0,-1,
         0,1,0,
         0,0,0]
dst, dst1, dst2 = differential(image, data1, data2)

cv2.imshow("image", image)
cv2.imshow("roberts edge", dst)
cv2.imshow("dst1", dst1)
cv2.imshow("dst2", dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()