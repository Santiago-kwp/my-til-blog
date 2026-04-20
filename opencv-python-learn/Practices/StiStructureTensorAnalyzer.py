"""STI 이미지의 구조 텐서(Structure Tensor)를 이용한 유속 분석기.

그레디언트 공분산 행렬의 고유벡터 분석을 통해 주 지배 방향(기울기)을 산출한다.
탐색 기반인 Radon/FFT보다 연산 속도가 빠르며 지역적 특징 추출에 강점이 있다.
"""
import math
import cv2
import numpy as np

class StiStructureTensorAnalyzer:
    """구조 텐서 기반 STI 분석기 구현체.

    Args:
        sigma: 가우시안 윈도우 크기 (누적 윈도우). 기본 3.0.
        n_chunks: STI 시간 분할 수. 기본 3.
        confidence_min: 유효 검출로 인정할 최소 Coherency. 기본 0.2.
    """
    def __init__(
        self,
        sigma: float = 3.0,
        n_chunks: int = 3,
        confidence_min: float = 0.2
    ) -> None:
        self.sigma = sigma
        self.n_chunks = n_chunks
        self.confidence_min = confidence_min

    def analyze(self, imgSti384: np.ndarray) -> "StiResult":
        from core.StiAnalyzerInterface import StiResult
        
        # 1. 전처리 (배경제거 등)
        img = imgSti384.astype(np.float32)
        bg = img.min(axis=0, keepdims=True)
        img = (img - bg).clip(0, 255)

        # 2. 청크별 분석
        h_chunk = img.shape[0] // self.n_chunks
        valid_slopes = []
        
        for i in range(self.n_chunks):
            chunk = img[i*h_chunk:(i+1)*h_chunk, :]
            slope, coherency = self._calc_structure_tensor(chunk)
            if coherency >= self.confidence_min and slope > 0:
                valid_slopes.append(slope)

        if not valid_slopes:
            return StiResult(0.0, 0.0, img.astype(np.uint8), None)

        final_slope = float(np.median(valid_slopes))
        final_angle = math.atan(final_slope) * 180.0 / math.pi

        return StiResult(
            disp_per_frame=final_slope,
            angle_deg=final_angle,
            img_sti=img.astype(np.uint8),
            img_fft=None
        )

    def _calc_structure_tensor(self, chunk: np.ndarray) -> tuple:
        # 그레디언트 Ix, Iy (Sobel)
        Ix = cv2.Sobel(chunk, cv2.CV_32F, 1, 0, ksize=3)
        Iy = cv2.Sobel(chunk, cv2.CV_32F, 0, 1, ksize=3)

        # 텐서 성분 Ix^2, Iy^2, IxIy
        Ixx = Ix**2
        Iyy = Iy**2
        Ixy = Ix*Iy

        # 가우시안 블러를 통한 지역 평균 (누적)
        ksize = int(self.sigma * 4) | 1
        Sxx = cv2.GaussianBlur(Ixx, (ksize, ksize), self.sigma)
        Syy = cv2.GaussianBlur(Iyy, (ksize, ksize), self.sigma)
        Sxy = cv2.GaussianBlur(Ixy, (ksize, ksize), self.sigma)

        # 주방향 각도 계산 (이미지 좌표계 기준)
        # 0.5 * atan2(2*Sxy, Syy - Sxx)
        # STI 축에 맞게 보정 (수직축 기준 각도로 변환)
        angle = 0.5 * np.arctan2(2 * Sxy, Syy - Sxx)
        
        # 전체 영역의 평균 각도와 일관성(Coherency) 계산
        # Coherency = (lambda1 - lambda2) / (lambda1 + lambda2)
        # 여기서는 단순 평균 대신 픽셀별 Coherency 가중치를 고려할 수 있으나 단순 구현 적용
        
        avg_Sxx = np.mean(Sxx)
        avg_Syy = np.mean(Syy)
        avg_Sxy = np.mean(Sxy)
        
        # 고유값 계산 (Tensor의 Eigenvalues)
        trace = avg_Sxx + avg_Syy
        det = avg_Sxx * avg_Syy - avg_Sxy**2
        sqrt_val = math.sqrt(max(0, (trace/2)**2 - det))
        lambda1 = trace/2 + sqrt_val
        lambda2 = trace/2 - sqrt_val
        
        coherency = (lambda1 - lambda2) / (lambda1 + lambda2) if (lambda1 + lambda2) > 0 else 0
        
        # 최종 각도 추출 (주 고유벡터 방향)
        final_theta_rad = 0.5 * math.atan2(2 * avg_Sxy, avg_Syy - avg_Sxx)
        # 수직축 기준 slope로 변환 (STI 특성에 맞게 조정 필요)
        # 텐서 각도는 보통 Gradient 방향이므로 90도 회전
        slope = math.tan(final_theta_rad + math.pi/2)
        
        return abs(slope), coherency
