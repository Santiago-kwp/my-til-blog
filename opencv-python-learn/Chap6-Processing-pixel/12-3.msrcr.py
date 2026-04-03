import sys, os, cv2
import numpy as np

# Common 폴더의 histogram.py 파일을 사용하기 위해 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.histogram import draw_histo

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# 이미지 경로를 루트 기준으로 설정
image_path = os.path.join(project_root, "images", "equalize.jpg")
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 그레이스케일로 로드
if image is None: raise Exception("영상파일 읽기 에러")

bins, ranges = [256], [0, 256]

# 원본 이미지의 히스토그램
hist = cv2.calcHist([image], [0], None, bins, ranges)
hist_img = draw_histo(hist)


# MSRCR (Multi-Scale Retinex with Color Restoration) 구현
# 여기서는 그레이스케일 이미지에 대한 Retinex의 밝기/대비 향상 부분을 구현합니다.
# 컬러 이미지에 대한 완전한 MSRCR은 채널별 처리 및 색상 복원 단계가 추가됩니다.

def singleScaleRetinex(img, sigma):
    """단일 스케일 Retinex를 적용합니다."""
    img = np.float64(img) + 1.0  # 로그 변환을 위해 0 방지

    # 가우시안 필터를 적용하여 조명 성분 추정 (큰 sigma는 전역 조명)
    L_blur = cv2.GaussianBlur(img, (0, 0), sigma)

    # 조명 성분이 0이 되는 것을 방지 (로그 계산 시 무한대 방지)
    L_blur[L_blur == 0] = 0.01

    # 반사율 성분 계산: log(R) - log(L) = log(R/L)
    retinex = np.log10(img / L_blur)
    return retinex


def multiScaleRetinex(img, sigma_list):
    """다중 스케일 Retinex를 적용합니다."""
    retinex = np.zeros_like(img, dtype=np.float64)
    for sigma in sigma_list:
        retinex += singleScaleRetinex(img, sigma)

    # 각 스케일의 결과를 평균
    retinex = retinex / len(sigma_list)
    return retinex


def MSRCR_Grayscale(img, sigma_list):
    """
    그레이스케일 이미지에 대한 MSRCR (Multi-Scale Retinex with Color Restoration) 구현.
    여기서는 'Color Restoration' 부분은 그레이스케일이므로 '대비 향상 및 정규화'로 대체됩니다.
    """

    # 1. 다중 스케일 Retinex 적용 (로그 도메인에서의 반사율 성분)
    retinex_result = multiScaleRetinex(img, sigma_list)

    # 2. 결과 정규화 및 스케일 조정 (0-255 범위로)
    # 로그 도메인에서 나온 결과는 음수와 양수를 가질 수 있으므로, Min-Max 정규화 적용
    min_val = np.min(retinex_result)
    max_val = np.max(retinex_result)

    # 0-255 범위로 정규화
    dst_msrcr = ((retinex_result - min_val) / (max_val - min_val)) * 255
    dst_msrcr = np.uint8(dst_msrcr)

    return dst_msrcr


# MSRCR 파라미터 설정
sigma_list = [15, 80, 250]  # 가우시안 필터의 표준 편차 리스트 (작은 값은 지역 대비, 큰 값은 전역 대비)

# MSRCR 적용
dst_msrcr = MSRCR_Grayscale(image, sigma_list)

# MSRCR 적용 후 히스토그램
hist_msrcr = cv2.calcHist([dst_msrcr], [0], None, bins, ranges)
hist_img_msrcr = draw_histo(hist_msrcr)

# 결과 영상 및 히스토그램 표시
cv2.imshow("Original Image", image)
cv2.imshow("Original Histogram", hist_img)

cv2.imshow("MSRCR Image (Grayscale)", dst_msrcr)
cv2.imshow("MSRCR Histogram (Grayscale)", hist_img_msrcr)

cv2.waitKey(0)
cv2.destroyAllWindows()