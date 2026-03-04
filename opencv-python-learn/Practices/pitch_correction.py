"""
pitch_correction.py
===================
전후각(Pitch Angle) 기반 이미지 높이 보정 모듈.

수학 모델 (비대칭 투시 투영):
  h(θ) = K / (cos(α_top + θ) · cos(α_bot + θ))

  where:
    θ      : 카메라 전후각 (라디안)
    α_top  : 카메라 → 달력 상단 수직 시각 (라디안, 하향이면 음수)
    α_bot  : 카메라 → 달력 하단 수직 시각 (라디안, α_bot < α_top)
    K      : 스케일 상수

  보정 스케일:
    scale(θ) = h(θ_ref) / h(θ)
             = [cos(α_top + θ) · cos(α_bot + θ)]
               / [cos(α_top + θ_ref) · cos(α_bot + θ_ref)]

  ※ 이 공식은 카메라가 달력 중심보다 위에 있는 실제 셋업(비대칭)에 적합.
     대칭 케이스(α_top = -α_bot)로 귀결되면 h(θ) = K / cos²(α + θ) 형태가 됨.
"""

from __future__ import annotations

import numpy as np
import cv2
from typing import Optional, Tuple

try:
    from scipy.optimize import curve_fit as _scipy_curve_fit
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class PitchCorrectionModel:
    """
    비대칭 투시 투영 기반 전후각-이미지 높이 보정 모델.

    사용 예::

        model = PitchCorrectionModel()
        model.fit(angles_deg=[-10, -1, 6], heights_px=[500, 440, 415])
        scale = model.correction_scale(-10.0)   # → 0.88
        corrected = correct_image_size(img, pitch_angle_deg=-10.0, model=model)
    """

    def __init__(self):
        self.mode: Optional[str] = None
        # perspective 모드 파라미터
        self.alpha_top_deg: Optional[float] = None
        self.alpha_bot_deg: Optional[float] = None
        self.K: Optional[float] = None
        # polynomial 모드 파라미터
        self.poly_coeffs: Optional[np.ndarray] = None
        # 공통
        self.ref_angle_deg: Optional[float] = None
        self._angles: Optional[np.ndarray] = None
        self._heights: Optional[np.ndarray] = None

    # ------------------------------------------------------------------
    # Fitting
    # ------------------------------------------------------------------

    def fit(
        self,
        angles_deg: list,
        heights_px: list,
        ref_angle_deg: Optional[float] = None,
        mode: str = 'auto',
    ) -> PitchCorrectionModel:
        """
        측정 데이터로 모델 파라미터를 추정한다.

        Args:
            angles_deg    : 전후각 리스트 (도 단위). 최소 2개 필요.
            heights_px    : 각 각도에서 측정한 달력 픽셀 높이.
            ref_angle_deg : 보정 기준 각도. None이면 최솟값 높이의 각도.
            mode          : 'auto' | 'perspective' | 'polynomial'
                            - 'auto': SciPy 설치 여부에 따라 자동 선택.

        Returns:
            self (메서드 체이닝 지원)
        """
        angles = np.asarray(angles_deg, dtype=float)
        heights = np.asarray(heights_px, dtype=float)
        if len(angles) < 2:
            raise ValueError("At least 2 data points required.")

        self._angles = angles
        self._heights = heights

        if ref_angle_deg is not None:
            self.ref_angle_deg = float(ref_angle_deg)
        else:
            self.ref_angle_deg = float(angles[np.argmin(heights)])

        if mode == 'auto':
            mode = 'perspective' if HAS_SCIPY else 'polynomial'

        if mode == 'perspective' and HAS_SCIPY:
            success = self._fit_perspective(angles, heights)
            if not success:
                self._fit_polynomial(angles, heights)
        else:
            self._fit_polynomial(angles, heights)

        return self

    def _fit_perspective(self, angles: np.ndarray, heights: np.ndarray) -> bool:
        """비대칭 투시 투영 모델 피팅. 성공 여부 반환."""

        def _model(theta_deg, alpha_top_deg, alpha_bot_deg, K):
            at = np.radians(alpha_top_deg)
            ab = np.radians(alpha_bot_deg)
            t = np.radians(theta_deg)
            denom = np.cos(at + t) * np.cos(ab + t)
            denom = np.where(np.abs(denom) < 1e-10, 1e-10, denom)
            return K / denom

        try:
            h_min = float(np.min(heights))
            p0 = [-10.0, -25.0, h_min * 0.85]
            bounds = ([-89.0, -89.0, 1e-3], [89.0, 89.0, np.inf])
            popt, _ = _scipy_curve_fit(
                _model, angles, heights, p0=p0, bounds=bounds, maxfev=20000
            )
            self.alpha_top_deg = float(popt[0])
            self.alpha_bot_deg = float(popt[1])
            self.K = float(popt[2])
            self.mode = 'perspective'
            return True
        except Exception:
            return False

    def _fit_polynomial(self, angles: np.ndarray, heights: np.ndarray):
        """2차 다항식 폴백 피팅."""
        deg = min(2, len(angles) - 1)
        self.poly_coeffs = np.polyfit(angles, heights, deg=deg)
        self.mode = 'polynomial'

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict_height(self, angle_deg: float) -> float:
        """각도에서 예상 달력 픽셀 높이 반환."""
        if self.mode is None:
            raise RuntimeError("Model not fitted. Call fit() first.")
        if self.mode == 'perspective':
            at = np.radians(self.alpha_top_deg)
            ab = np.radians(self.alpha_bot_deg)
            t = np.radians(float(angle_deg))
            denom = float(np.cos(at + t) * np.cos(ab + t))
            if abs(denom) < 1e-10:
                raise ValueError(
                    f"Angle {angle_deg}° causes singularity (denom≈0). "
                    "Angle is too extreme for this model."
                )
            return self.K / denom
        else:
            return float(np.polyval(self.poly_coeffs, angle_deg))

    def correction_scale(self, angle_deg: float) -> float:
        """
        입력 각도에서 기준각으로 보정하기 위한 스케일 반환.

        Returns:
            scale = h(θ_ref) / h(θ)
            - scale < 1 : 현재 이미지가 기준보다 크게 투영 → 축소 필요
            - scale = 1 : 기준각과 동일
            - scale > 1 : 현재 이미지가 기준보다 작게 투영 → 확대 필요
        """
        if self.ref_angle_deg is None:
            raise RuntimeError("Model not fitted. Call fit() first.")
        h_ref = self.predict_height(self.ref_angle_deg)
        h_input = self.predict_height(angle_deg)
        if h_input <= 0:
            raise ValueError(f"Predicted height {h_input:.2f}px at {angle_deg}° is invalid.")
        return h_ref / h_input

    def __repr__(self) -> str:
        if self.mode == 'perspective':
            return (
                f"PitchCorrectionModel(mode=perspective, "
                f"alpha_top={self.alpha_top_deg:.2f}deg, "
                f"alpha_bot={self.alpha_bot_deg:.2f}deg, "
                f"K={self.K:.1f}, ref={self.ref_angle_deg:.1f}deg)"
            )
        if self.mode == 'polynomial':
            c = self.poly_coeffs
            return (
                f"PitchCorrectionModel(mode=polynomial, "
                f"coeffs=[{c[0]:.4f}, {c[1]:.4f}, {c[2]:.4f}], "
                f"ref={self.ref_angle_deg:.1f}deg)"
            )
        return "PitchCorrectionModel(not fitted)"


# ---------------------------------------------------------------------------
# Correction
# ---------------------------------------------------------------------------

def correct_image_size(
    image: np.ndarray,
    pitch_angle_deg: float,
    model: PitchCorrectionModel,
) -> np.ndarray:
    """
    전후각 보정을 적용한 이미지 반환.

    높이(H)만 보정 스케일 적용. 너비(W)는 유지.

    Args:
        image           : BGR 또는 그레이스케일 이미지 (H×W 또는 H×W×C)
        pitch_angle_deg : 촬영 시 카메라 전후각 (도)
        model           : 피팅된 PitchCorrectionModel 인스턴스

    Returns:
        보정된 이미지

    Raises:
        ValueError: 이미지가 비어있거나 스케일이 비정상인 경우
    """
    if image is None or image.size == 0:
        raise ValueError("Input image is empty or None.")

    scale = model.correction_scale(pitch_angle_deg)
    if scale <= 0 or not np.isfinite(scale):
        raise ValueError(
            f"Invalid correction scale {scale:.4f} at angle {pitch_angle_deg}°."
        )

    h, w = image.shape[:2]
    new_h = max(1, round(h * scale))

    if new_h == h:
        return image.copy()

    return cv2.resize(image, (w, new_h), interpolation=cv2.INTER_LINEAR)


# ---------------------------------------------------------------------------
# Calendar Detection
# ---------------------------------------------------------------------------

def measure_calendar_height(
    image: np.ndarray,
    method: str = 'blue_hough',
) -> Tuple[int, int, int]:
    """
    이미지에서 달력 영역의 픽셀 높이 자동 측정.

    Args:
        image  : BGR 이미지 (H×W×3)
        method : 'blue_hough' | 'variance'

    Returns:
        (top_y, bottom_y, height_px)

    Raises:
        ValueError: 달력 영역 자동 감지 실패
    """
    if method not in ('blue_hough', 'variance'):
        raise ValueError(f"Unknown method '{method}'. Use 'blue_hough' or 'variance'.")

    result = _detect_blue_hough(image) if method == 'blue_hough' else None
    if result is None:
        result = _detect_variance(image)
    if result is None:
        raise ValueError(
            "Calendar region could not be detected automatically. "
            "Inspect the image and specify ROI manually."
        )
    return result


def _detect_blue_hough(image: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    달력 흰 인쇄 영역(white body) 감지 — 연결 컴포넌트 기반.

    전략:
      1. HSV 마스킹으로 네이비 블루 베이스 탐색
         - bottom_y = 파란 베이스의 상단 (= 흰 인쇄 영역의 하단)
         - 가로세로 비율 필터(w/h > 2.0)
      2. 파란 베이스 열 범위 내에서만 흰색 세그멘테이션
         - HSV(S<55, V>175) + 열 범위 제한 → 배경 벽면 제외
         - 모폴로지 클로징으로 격자선·날짜 숫자 공백 채우기
      3. 블루 베이스 바로 위에서 연결 컴포넌트 시드
         - bottom_y 근처에서 흰색 컴포넌트 ID 수집
         - 해당 컴포넌트의 최상단 y = top_y (배경 분리 보장)
      4. 폴백: 중앙 50% 열 기반 고휘도 행 탐색
    """
    H_img, W_img = image.shape[:2]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # ── Step 1: 파란 베이스 감지 (bottom_y, bx, bw) ──
    lower_blue = np.array([100, 80, 20])
    upper_blue = np.array([125, 255, 130])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel_blue = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 8))
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel_blue)

    cnts, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None

    blue_cands = []
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        cx = x + w / 2
        if area > 15000 and W_img * 0.15 < cx < W_img * 0.85 and w > h * 2.0:
            blue_cands.append((area, x, y, w, h))
    if not blue_cands:
        return None

    blue_cands.sort(reverse=True)
    _, bx, by, bw, bh = blue_cands[0]
    bottom_y = by

    # ── Step 2: 흰색 마스크 — 파란 베이스 열 범위로 배경 제외 ──
    white_mask = cv2.inRange(
        hsv,
        np.array([0,   0, 175]),
        np.array([180, 55, 255]),
    )
    # 파란 베이스 열 범위 ±12.5% 밖은 배경으로 간주해 제거
    col_l = max(0,    bx - bw // 8)
    col_r = min(W_img, bx + bw + bw // 8)
    tmp = np.zeros_like(white_mask)
    tmp[:, col_l:col_r] = white_mask[:, col_l:col_r]
    white_mask = tmp
    white_mask[bottom_y:, :] = 0

    # ── Step 3: 모폴로지 클로징 ──
    kw = max(64, bw // 10)
    kh = max(32, H_img // 34)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (kw, kh))
    white_filled = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel_close)

    # ── Step 4: 연결 컴포넌트 — 블루 베이스 위에서 시드 ──
    _, labeled = cv2.connectedComponents(white_filled)
    seed_labels: set = set()
    for dy in range(1, min(80, bottom_y)):
        row_labels = set(labeled[bottom_y - dy, col_l:col_r].tolist()) - {0}
        seed_labels |= row_labels
        if seed_labels:
            break

    top_y = None
    if seed_labels:
        cal_mask = np.isin(labeled, list(seed_labels)).astype(np.uint8)
        ys = np.where(cal_mask)[0]
        if len(ys) > 0:
            top_y = int(ys.min())

    # ── Step 5: 폴백 — 고휘도 행 탐색 ──
    if top_y is None:
        col_c_l = max(0, W_img // 4)
        col_c_r = min(W_img, 3 * W_img // 4)
        search_top = max(0, by - int(H_img * 0.85))
        roi_gray = cv2.cvtColor(
            image[search_top:bottom_y, col_c_l:col_c_r], cv2.COLOR_BGR2GRAY
        )
        row_mean = np.mean(roi_gray, axis=1)
        white_rows = np.where(row_mean > 185)[0]
        top_y = int(white_rows[0]) + search_top if len(white_rows) > 0 else search_top

    height_px = bottom_y - top_y
    if height_px <= 0:
        return None
    return (top_y, bottom_y, height_px)


def _detect_variance(image: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """로컬 분산 기반 달력 영역 감지 (폴백)."""
    H_img, W_img = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

    x0, x1 = W_img // 4, 3 * W_img // 4
    col = gray[:, x0:x1]
    row_std = np.std(col, axis=1)

    window = 25
    kernel = np.ones(window) / window
    smoothed = np.convolve(row_std, kernel, mode='same')

    rows = np.where(smoothed > smoothed.max() * 0.30)[0]
    if len(rows) < 10:
        return None

    top_y, bottom_y = int(rows[0]), int(rows[-1])
    height_px = bottom_y - top_y
    if height_px <= 0:
        return None
    return (top_y, bottom_y, height_px)
