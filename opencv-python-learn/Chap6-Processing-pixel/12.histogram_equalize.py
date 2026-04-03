import sys, os, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turtledemo.lindenmayer import draw

import numpy as np, cv2

from Common.histogram import draw_histo

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# 이미지 경로를 루트 기준으로 설정
image_path = os.path.join(project_root, "images", "equalize.jpg")
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")


bins, ranges = [256], [0, 256]
hist = cv2.calcHist([image], [0], None, bins, ranges)

## 히스토그램 누적합 계산
accum_hist = np.zeros(hist.shape[:2], np.float32)
accum_hist[0] = hist[0]
for i in range(1, hist.shape[0]):
    accum_hist[i] = accum_hist[i - 1] + hist[i]

accum_hist = (accum_hist / sum(hist)) * 255                # 누적합의 정규화
dst1 = [[accum_hist[val] for val in row] for row in image] # 화소값 할당
dst1 = np.array(dst1, dtype=np.uint8)

## numpy 함수 및 OpenCV 룩업 테이블 사용(내부적으로 C,C++ 코드로 작동하여 빠름)
"""
accum_hist = np.cumsum(hist)    # 누적합 계산
cv2.normalize(accum_hist, accum_hist, 0, 255, cv2.NORM_MINMAX)  # 정규화
dst1 = cv2.LUT(image, accum_hist.astype(np.uint8))
"""

dst2 = cv2.equalizeHist(image)  # OpenCV 히스토그램 평활화
hist1 = cv2.calcHist([dst1], [0], None, bins, ranges)
hist2 = cv2.calcHist([dst2], [0], None, bins, ranges)
hist_img = draw_histo(hist)
hist_img1 = draw_histo(hist1)
hist_img2 = draw_histo(hist2)

cv2.imshow("image", image); cv2.imshow("hist_img", hist_img)
cv2.imshow("dst1_User", dst1); cv2.imshow("User_hist", hist_img1)
cv2.imshow("dst2_OpenCV", dst2); cv2.imshow("OpenCV2_hist", hist_img2)
cv2.waitKey(0); cv2.destroyAllWindows()



