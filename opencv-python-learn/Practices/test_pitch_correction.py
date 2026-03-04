"""
test_pitch_correction.py
========================
전후각 보정 함수 pytest 테스트 모음.

실험 조건:
  - 카메라가 달력보다 위에 위치 (비대칭 셋업)
  - 측정 각도: -10°, -1°, +6°
  - 예상 높이 순서: h(-10°) > h(-1°) > h(+6°)
    (카메라가 뒤로 기울수록 달력이 더 크게 보임)

주의: MEASURED_HEIGHTS 는 노트북 분석 후 실측값으로 업데이트 권장.
"""

import sys
import os
import math
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from pitch_correction import PitchCorrectionModel, correct_image_size


# ---------------------------------------------------------------------------
# 테스트 데이터
# ---------------------------------------------------------------------------
# 실측 추정값 (노트북 pitch_angle_analysis.ipynb 실행 후 업데이트)
# 순서: h(-10°) > h(-1°) > h(+6°) — 비대칭 카메라 셋업 기준
MEASURED_ANGLES = [-10.0, -1.0, 6.0]
MEASURED_HEIGHTS = [500, 440, 415]   # 픽셀 (추정)
REF_ANGLE = -1.0                     # 보정 기준 각도


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fitted_model():
    """실측 데이터로 피팅된 모델."""
    model = PitchCorrectionModel()
    model.fit(MEASURED_ANGLES, MEASURED_HEIGHTS, ref_angle_deg=REF_ANGLE)
    return model


@pytest.fixture
def dummy_image():
    """테스트용 더미 이미지 (400×600 검정)."""
    return np.zeros((400, 600, 3), dtype=np.uint8)


def _make_theoretical_heights(alpha_top_deg, alpha_bot_deg, K, angles_deg):
    """이론 모델에서 기대 높이 생성 (테스트 데이터 제조용)."""
    heights = []
    for a in angles_deg:
        at = math.radians(alpha_top_deg)
        ab = math.radians(alpha_bot_deg)
        t = math.radians(a)
        heights.append(K / (math.cos(at + t) * math.cos(ab + t)))
    return heights


# ---------------------------------------------------------------------------
# TC-01: 모델 피팅 잔차 검증
# ---------------------------------------------------------------------------

def test_model_fit_residuals():
    """
    이론 모델에서 생성한 데이터를 피팅하면
    각 포인트에서 예측값 오차가 ±5% 이내여야 한다.
    """
    alpha_top, alpha_bot, K = -8.0, -28.0, 420.0
    angles = [-12.0, -1.0, 8.0]
    heights = _make_theoretical_heights(alpha_top, alpha_bot, K, angles)

    model = PitchCorrectionModel()
    model.fit(angles, heights, ref_angle_deg=-1.0)

    for angle, h_expected in zip(angles, heights):
        h_pred = model.predict_height(angle)
        err = abs(h_pred - h_expected) / h_expected
        assert err <= 0.05, (
            f"angle={angle}deg: predicted={h_pred:.1f}, "
            f"expected={h_expected:.1f}, error={err:.1%} > 5%"
        )


# ---------------------------------------------------------------------------
# TC-02: 기준각에서 보정 = 항등 변환
# ---------------------------------------------------------------------------

def test_correct_at_reference_angle_is_identity(fitted_model, dummy_image):
    """
    기준각(θ_ref)에서 correct_image_size()를 호출하면
    출력 이미지 높이 = 입력 이미지 높이 (항등 변환).
    """
    ref = fitted_model.ref_angle_deg
    corrected = correct_image_size(dummy_image, ref, fitted_model)
    assert corrected.shape[0] == dummy_image.shape[0], (
        f"Height must not change at reference angle {ref}deg. "
        f"Before={dummy_image.shape[0]}, After={corrected.shape[0]}"
    )
    assert corrected.shape[1] == dummy_image.shape[1], "Width must never change."


# ---------------------------------------------------------------------------
# TC-03: 보정 스케일 순서 검증 (비대칭 셋업)
# ---------------------------------------------------------------------------

def test_correction_scale_ordering(fitted_model):
    """
    비대칭 셋업(카메라 > 달력 높이):
      h(-10°) > h(-1°) > h(+6°)
    따라서 보정 스케일:
      scale(-10°) < scale(-1°) = 1.0 < scale(+6°)

    -10°은 달력이 가장 크게 찍혔으므로 축소 필요 (scale < 1)
    +6°은 달력이 가장 작게 찍혔으므로 확대 필요 (scale > 1)
    """
    s_m10 = fitted_model.correction_scale(-10.0)
    s_m1 = fitted_model.correction_scale(-1.0)
    s_p6 = fitted_model.correction_scale(6.0)

    assert abs(s_m1 - 1.0) < 0.01, (
        f"Scale at reference angle must be ~1.0, got {s_m1:.4f}"
    )
    assert s_m10 < s_m1, (
        f"scale(-10°)={s_m10:.3f} should be < scale(-1°)={s_m1:.3f}. "
        "Camera tilted back → calendar appears larger → needs reduction."
    )
    assert s_p6 > s_m1, (
        f"scale(+6°)={s_p6:.3f} should be > scale(-1°)={s_m1:.3f}. "
        "Camera tilted forward → calendar appears smaller → needs enlargement."
    )
    assert s_m10 < s_p6, (
        f"scale(-10°)={s_m10:.3f} should be < scale(+6°)={s_p6:.3f}."
    )


# ---------------------------------------------------------------------------
# TC-04: 이미지 높이 보정 수치 검증
# ---------------------------------------------------------------------------

def test_corrected_image_height(fitted_model):
    """
    보정 후 높이 = round(원본 높이 × scale).
    너비(W)는 변경 없어야 한다.
    """
    orig_h, orig_w = 500, 800
    test_image = np.zeros((orig_h, orig_w, 3), dtype=np.uint8)

    for angle in MEASURED_ANGLES:
        corrected = correct_image_size(test_image, angle, fitted_model)
        scale = fitted_model.correction_scale(angle)
        expected_h = round(orig_h * scale)
        assert corrected.shape[0] == expected_h, (
            f"angle={angle}deg: expected_h={expected_h}, got={corrected.shape[0]}"
        )
        assert corrected.shape[1] == orig_w, (
            f"Width must not change. Expected {orig_w}, got {corrected.shape[1]}"
        )


# ---------------------------------------------------------------------------
# TC-05: 모델 대칭성 검증 (대칭 셋업 케이스)
# ---------------------------------------------------------------------------

def test_model_symmetry_with_centered_camera():
    """
    카메라가 달력 중심 높이에 있는 경우(대칭 셋업):
      alpha_bot = -alpha_top → h(+δ) = h(-δ)

    이 경우 투시 투영 모델은 기준각(θ₀)에 대해 대칭이어야 한다.
    """
    alpha_top = -12.0
    alpha_bot = 12.0   # 대칭: -alpha_top
    K = 500.0
    angles = [-15.0, 0.0, 15.0]
    heights = _make_theoretical_heights(alpha_top, alpha_bot, K, angles)

    model = PitchCorrectionModel()
    model.fit(angles, heights, ref_angle_deg=0.0)

    h_neg = model.predict_height(-15.0)
    h_pos = model.predict_height(15.0)

    rel_diff = abs(h_neg - h_pos) / max(h_neg, h_pos)
    assert rel_diff < 0.02, (
        f"Symmetric model: h(-15°)={h_neg:.2f}, h(+15°)={h_pos:.2f}, "
        f"relative_diff={rel_diff:.2%} > 2%"
    )


# ---------------------------------------------------------------------------
# TC-06: 엣지 케이스
# ---------------------------------------------------------------------------

def test_edge_case_zero_angle(fitted_model, dummy_image):
    """θ=0°에서 오류 없이 보정 가능해야 한다."""
    result = correct_image_size(dummy_image, 0.0, fitted_model)
    assert result is not None
    assert result.shape[1] == dummy_image.shape[1]


def test_edge_case_empty_image(fitted_model):
    """빈 이미지(0×0×3) 입력 시 ValueError."""
    empty = np.zeros((0, 0, 3), dtype=np.uint8)
    with pytest.raises(ValueError, match="empty"):
        correct_image_size(empty, -1.0, fitted_model)


def test_edge_case_model_not_fitted():
    """fit() 호출 전 predict_height() 시 RuntimeError."""
    model = PitchCorrectionModel()
    with pytest.raises(RuntimeError, match="not fitted"):
        model.predict_height(0.0)


def test_edge_case_model_not_fitted_scale():
    """fit() 호출 전 correction_scale() 시 RuntimeError."""
    model = PitchCorrectionModel()
    with pytest.raises(RuntimeError, match="not fitted"):
        model.correction_scale(0.0)


def test_edge_case_insufficient_data():
    """데이터 1개 입력 시 ValueError."""
    model = PitchCorrectionModel()
    with pytest.raises(ValueError, match="At least 2"):
        model.fit([0.0], [400])


# ---------------------------------------------------------------------------
# 추가: 보정 후 원본 복원 일관성
# ---------------------------------------------------------------------------

def test_double_correction_consistency(fitted_model):
    """
    -10°로 촬영된 이미지를 -1°로 보정한 후,
    다시 역방향으로 보정하면 원본 높이로 복원되어야 한다.
    """
    orig_h, orig_w = 500, 800
    img = np.zeros((orig_h, orig_w, 3), dtype=np.uint8)

    # -10° → 기준(-1°)으로 보정
    corrected = correct_image_size(img, -10.0, fitted_model)
    corrected_h = corrected.shape[0]

    # 기준(-1°)으로 보정된 이미지를 다시 -10°로 역보정할 모델 생성
    inv_model = PitchCorrectionModel()
    inv_model.fit(MEASURED_ANGLES, MEASURED_HEIGHTS, ref_angle_deg=-10.0)

    restored = correct_image_size(corrected, -1.0, inv_model)
    restored_h = restored.shape[0]

    # 1픽셀 반올림 오차 허용
    assert abs(restored_h - orig_h) <= 1, (
        f"Round-trip: original={orig_h}, corrected={corrected_h}, "
        f"restored={restored_h} (expected ~{orig_h})"
    )
