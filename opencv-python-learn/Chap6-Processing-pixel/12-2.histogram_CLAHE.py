import sys, os, cv2
import numpy as np

# Common 폴더의 histogram.py 파일을 사용하기 위해 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.histogram import draw_histo

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# 이미지 경로를 루트 기준으로 설정
image_path = os.path.join(project_root, "images", "equalize.jpg")
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

bins, ranges = [256], [0, 256]

# 원본 이미지의 히스토그램
hist = cv2.calcHist([image], [0], None, bins, ranges)
hist_img = draw_histo(hist)

# 1. 일반적인 히스토그램 평활화 (equalizeHist)
# 여기서는 OpenCV 함수를 사용하여 간단히 구현합니다.
dst_equalize = cv2.equalizeHist(image)
hist_equalize = cv2.calcHist([dst_equalize], [0], None, bins, ranges)
hist_img_equalize = draw_histo(hist_equalize)

# 2. CLAHE (Contrast Limited Adaptive Histogram Equalization) 적용
0# cv2.createCLAHE(clipLimit, tileGridSize) 함수로 CLAHE 객체를 생성
# clipLimit: 대비 제한 임계값. 값이 클수록 대비가 강해집니다.
# tileGridSize: 영상을 나눌 그리드 크기 (예: (8,8)은 8x8 타일로 나눔)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
dst_clahe = clahe.apply(image)

# CLAHE 적용 후 히스토그램
hist_clahe = cv2.calcHist([dst_clahe], [0], None, bins, ranges)
hist_img_clahe = draw_histo(hist_clahe)

# 결과 영상 및 히스토그램 표시
cv2.imshow("Original Image", image)
cv2.imshow("Original Histogram", hist_img)

cv2.imshow("Equalized Image", dst_equalize)
cv2.imshow("Equalized Histogram", hist_img_equalize)

cv2.imshow("CLAHE Image", dst_clahe)
cv2.imshow("CLAHE Histogram", hist_img_clahe)

cv2.waitKey(0)
cv2.destroyAllWindows()