"""STI 이미지의 구조 텐서(Structure Tensor)를 이용한 유속 분석기.

그레디언트 공분산 행렬의 고유벡터 분석을 통해 주 지배 방향(기울기)을 산출한다.
탐색 기반인 Radon/FFT보다 연산 속도가 빠르며 지역적 특징 추출에 강점이 있다.

개선 사항 (sti-tensor-enhanced):
- 그레디언트 크기 가중 집계: 고에너지 픽셀(궤적 에지)에 집중, 배경 희석 완화
  (Sxx+Syy 가중치 → 무방향 배경보다 강한 에지가 지배적)
- 청크별 중앙값 병합: 이상치 강건
"""
import math
import cv2
import numpy as np


class StiStructureTensorAnalyzer:
    """구조 텐서 기반 STI 분석기 개선 구현체.

    Args:
        sigma: 가우시안 윈도우 크기. 기본 3.0.
        n_chunks: STI 시간 분할 수. 기본 3.
        confidence_min: 유효 검출로 인정할 최소 Coherency. 기본 0.2.
        use_grad_weight: 그레디언트 크기 가중 집계 사용 여부. 기본 True.
    """

    def __init__(
        self,
        sigma: float = 3.0,
        n_chunks: int = 3,
        confidence_min: float = 0.2,
        use_grad_weight: bool = True,
    ) -> None:
        self.sigma = sigma
        self.n_chunks = n_chunks
        self.confidence_min = confidence_min
        self.use_grad_weight = use_grad_weight

    def analyze(self, imgSti384: np.ndarray) -> "StiResult":
        from core.StiAnalyzerInterface import StiResult

        # 1. 배경 제거 (최솟값 차감 or 중앙값 차감)
        img = imgSti384.astype(np.float32)
        # bg = img.min(axis=0, keepdims=True)
        bg = np.median(img, axis=0, keepdims=True)
        img = (img - bg).clip(0, 255) # 음수 방지 및 clip 자동 처리

        # 2. 청크별 분석
        h_chunk = img.shape[0] // self.n_chunks
        valid_slopes = []

        for i in range(self.n_chunks):
            chunk = img[i * h_chunk : (i + 1) * h_chunk, :]
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
            img_fft=None,
        )

    def _calc_structure_tensor(self, chunk: np.ndarray) -> tuple:
        """그레디언트 크기 가중 글로벌 구조 텐서로 slope과 coherency를 반환한다.

        개선:
        - w = sqrt(Sxx + Syy): 강한 에지 픽셀(궤적 후보)에 더 높은 가중치
        - 약한 배경 픽셀의 기여가 자동으로 축소됨

        Args:
            chunk: 배경제거된 STI 청크 (float32, 범위 0~255).

        Returns:
            (slope, coherency): slope은 px/frame, coherency는 0~1.
        """
        chunk_f = chunk.astype(np.float32)

        # Sobel 그레디언트
        Ix = cv2.Sobel(chunk_f, cv2.CV_32F, 1, 0, ksize=3)
        Iy = cv2.Sobel(chunk_f, cv2.CV_32F, 0, 1, ksize=3)

        # 지역 구조 텐서 성분 (가우시안 공간 평활화)
        ksize = int(self.sigma * 4) | 1
        Sxx = cv2.GaussianBlur(Ix * Ix, (ksize, ksize), self.sigma)
        Syy = cv2.GaussianBlur(Iy * Iy, (ksize, ksize), self.sigma)
        Sxy = cv2.GaussianBlur(Ix * Iy, (ksize, ksize), self.sigma)

        # 전역 집계
        if self.use_grad_weight:
            # 그레디언트 크기 가중: 강한 에지 픽셀이 지배적
            w = np.sqrt(Sxx + Syy + 1e-9)
            w_total = float(w.sum()) + 1e-9
            avg_Sxx = float(np.sum(Sxx * w) / w_total)
            avg_Syy = float(np.sum(Syy * w) / w_total)
            avg_Sxy = float(np.sum(Sxy * w) / w_total)
        else:
            # 단순 평균 (baseline)
            avg_Sxx = float(np.mean(Sxx))
            avg_Syy = float(np.mean(Syy))
            avg_Sxy = float(np.mean(Sxy))

        # 고유값 분해 (Coherency 계산)
        trace = avg_Sxx + avg_Syy
        det = avg_Sxx * avg_Syy - avg_Sxy ** 2
        disc = max(0.0, (trace / 2.0) ** 2 - det)
        sqrt_val = math.sqrt(disc)
        lambda1 = trace / 2.0 + sqrt_val
        lambda2 = trace / 2.0 - sqrt_val

        coherency = (lambda1 - lambda2) / (lambda1 + lambda2 + 1e-9)

        # 주방향 slope 추출 (STI 경사 변환)
        final_theta_rad = 0.5 * math.atan2(2.0 * avg_Sxy, avg_Syy - avg_Sxx)
        slope = abs(math.tan(final_theta_rad + math.pi / 2.0))

        return slope, coherency
