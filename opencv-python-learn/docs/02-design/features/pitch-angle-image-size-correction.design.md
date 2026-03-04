# Design: 전후각(Pitch Angle) 기반 이미지 크기 보정 함수

**Feature**: `pitch-angle-image-size-correction`
**Date**: 2026-03-04
**Phase**: Design
**Based on**: `docs/01-plan/features/pitch-angle-image-size-correction.plan.md`

---

## 1. 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                  pitch_correction (패키지)                      │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  calendar_detect  │    │   pitch_model    │                  │
│  │  (달력 영역 감지) │    │  (투시투영 모델) │                  │
│  └────────┬─────────┘    └────────┬─────────┘                  │
│           │                       │                             │
│           └──────────┬────────────┘                             │
│                      ▼                                          │
│            ┌──────────────────┐                                 │
│            │ pitch_correction │  ← 사용자 진입점               │
│            │  (보정 함수)     │                                 │
│            └──────────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              pitch_angle_analysis.ipynb (분석 노트북)           │
│  1. 이미지별 달력 bounding box 측정                              │
│  2. 전후각-크기 관계 시각화 + 모델 피팅                          │
│  3. 보정 전/후 시각화 비교                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              test_pitch_correction.py (pytest)                  │
│  1. 모델 수식 수치 검증                                          │
│  2. 보정 함수 이미지 크기 검증                                   │
│  3. 엣지 케이스 검증 (0도, 극단 각도)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 수학 모델 설계

### 2.1 투시 투영 모델 (이론)

카메라가 피치각 θ(기준각 θ_ref 기준)만큼 기울어졌을 때,
수직 평면(달력)의 픽셀 높이 변화 비율:

```
h(θ) / h(θ_ref) = (cos²(θ_ref - θ₀) - α²·sin²(θ_ref - θ₀))
                  ─────────────────────────────────────────────
                  (cos²(θ - θ₀) - α²·sin²(θ - θ₀))
```

- `θ`: 현재 촬영 전후각 (도 단위)
- `θ_ref`: 보정 목표 각도 (기본값: 데이터 내 최솟값 각도)
- `θ₀`: 달력 상하 중심이 카메라 광축과 일치하는 각도 (카메라 기하 파라미터)
- `α = H / (2d)`: 달력 실제 높이의 절반 / 달력까지 수평 거리
- 단, `cos²(θ - θ₀) > α²·sin²(θ - θ₀)` 범위 내에서 유효

### 2.2 파라미터 추정 전략

3개 데이터 포인트 (-10°, -1°, 6°)로 파라미터 추정:

```
측정값: [(θ₁, h₁), (θ₂, h₂), (θ₃, h₃)]
최적화:  α, θ₀ = argmin Σ |h_model(θᵢ) - hᵢ|²
```

**Fallback (데이터 부족 시):**
단순 2차 다항식 근사:
```
h(θ) ≈ a·θ² + b·θ + c
```
3점으로 계수 a, b, c를 직접 계산 (numpy.polyfit 사용).

### 2.3 보정 스케일 계산

입력 이미지의 달력 높이를 기준 각도 기준으로 정규화:

```
scale = h(θ_ref) / h(θ_input)
corrected_height = round(original_height × scale)
```

단, 너비(width)는 피치각 영향이 미미하므로 보정하지 않음.

---

## 3. 모듈 설계

### 3.1 `pitch_correction.py`

```python
# ─────────────────────────────────────────
# Module: pitch_correction
# 전후각 기반 이미지 높이 보정 함수 모음
# ─────────────────────────────────────────

class PitchCorrectionModel:
    """
    투시 투영 기반 전후각-크기 보정 모델.

    Attributes:
        alpha (float): H/(2d) 기하 파라미터
        theta0_deg (float): 카메라 광축 기준각 (도)
        mode (str): 'perspective' | 'polynomial'
        poly_coeffs (np.ndarray): 다항식 계수 (mode='polynomial'일 때)
        ref_height_px (int): 기준 각도에서의 달력 픽셀 높이
        ref_angle_deg (float): 기준 각도 (도)
    """

    def fit(self,
            angles_deg: list[float],
            heights_px: list[int],
            ref_angle_deg: float | None = None,
            mode: str = 'perspective') -> 'PitchCorrectionModel':
        """
        측정 데이터로 모델 파라미터 추정.

        Args:
            angles_deg: 각도 리스트 (도)
            heights_px: 각 각도에서의 달력 픽셀 높이
            ref_angle_deg: 기준 각도 (None이면 최솟값 높이의 각도 사용)
            mode: 모델 종류

        Returns:
            self (메서드 체이닝 지원)
        """

    def predict_height(self, angle_deg: float) -> float:
        """각도에서 예상 달력 픽셀 높이 반환."""

    def correction_scale(self, angle_deg: float) -> float:
        """
        주어진 각도에서 기준 각도로 보정하기 위한 스케일 반환.
        scale = h(ref) / h(angle)
        """


def correct_image_size(
    image: np.ndarray,
    pitch_angle_deg: float,
    model: PitchCorrectionModel,
) -> np.ndarray:
    """
    전후각 보정을 적용한 이미지 반환.

    높이(H)만 보정 스케일을 적용하여 리사이즈.

    Args:
        image: 원본 이미지 (H×W 또는 H×W×C)
        pitch_angle_deg: 촬영 전후각 (도)
        model: 피팅된 PitchCorrectionModel 인스턴스

    Returns:
        보정된 이미지 (높이 변경, 너비 유지)

    Raises:
        ValueError: 보정 스케일이 0 이하이거나 비정상인 경우
    """


def measure_calendar_height(
    image: np.ndarray,
    method: str = 'blue_hough',
) -> tuple[int, int, int]:
    """
    이미지에서 달력 높이(픽셀) 자동 측정.

    Args:
        image: BGR 이미지
        method: 'blue_hough' | 'variance' | 'manual'

    Returns:
        (top_y, bottom_y, height_px)
    """
```

### 3.2 달력 감지 전략 (3단계 폴백)

```
1단계: Blue Base + Hough 수평선 조합
   ├── HSV로 파란 베이스 하단 (y_bottom) 검출
   ├── 베이스 위쪽 영역에서 Hough 수평선 밀도 피크 (y_top) 검출
   └── height = y_bottom - y_top

2단계: 분산 기반 감지 (1단계 실패 시)
   ├── 로컬 분산 → 이진화 → 가장 큰 사각형 윤곽
   └── bounding box height 반환

3단계: 수동 입력 (2단계도 실패 시)
   └── ValueError 발생, 사용자에게 ROI 수동 지정 유도
```

---

## 4. 노트북 설계 (`pitch_angle_analysis.ipynb`)

### Cell 구성

| Cell # | 유형 | 내용 |
|--------|------|------|
| 1 | Code | 라이브러리 임포트, 경로 설정 |
| 2 | Markdown | 실험 개요 및 이론 |
| 3 | Code | 3개 이미지 로드 및 표시 |
| 4 | Code | 달력 bounding box 측정 + 결과 표 |
| 5 | Markdown | 측정 결과 해석 |
| 6 | Code | 전후각-높이 산점도 + 모델 피팅 그래프 |
| 7 | Code | PitchCorrectionModel 피팅 |
| 8 | Code | 보정 함수 적용 결과 시각화 (Before/After) |
| 9 | Markdown | 결론 및 한계 |

### 핵심 시각화 (Cell 6)

```
[산점도]
X축: 전후각 (도)      Y축: 달력 높이 (픽셀)
데이터포인트: 3개 측정값 (●)
이론곡선:    투시투영 모델 (실선)
다항곡선:    2차 다항식 피팅 (점선)

[Before/After 비교]
| -10° (원본) | -10° (보정) |
| -1° (원본)  | -1° (보정)  |
| +6° (원본)  | +6° (보정)  |
```

---

## 5. 테스트 설계 (`test_pitch_correction.py`)

### 테스트 케이스

```python
# ─────────────────────────
# TC-01: 모델 피팅 정확도
# ─────────────────────────
def test_model_fit_residuals():
    """
    3개 측정 포인트에 피팅 후,
    각 포인트에서의 예측값이 실측값 ±10% 이내인지 검증.
    """

# ─────────────────────────
# TC-02: 기준각 보정 항등성
# ─────────────────────────
def test_correct_at_reference_angle_is_identity():
    """
    기준각(θ_ref)에서 correct_image_size()를 호출하면
    입력 이미지와 출력 이미지 높이가 동일해야 함.
    scale = h(ref)/h(ref) = 1.0 → 이미지 크기 불변.
    """

# ─────────────────────────
# TC-03: 기준각 대비 크기 관계
# ─────────────────────────
def test_correction_scale_ordering():
    """
    |θ - θ_ref|가 클수록 보정 스케일(scale)이 더 작아야 함.
    (기준각에서 멀수록 크게 투영 → 보정 시 더 많이 축소)
    scale(-10°) < scale(-1°) ≈ 1.0 > scale(+6°)
    단, scale(-10°) < scale(+6°) < scale(-1°)
    """

# ─────────────────────────
# TC-04: 이미지 높이 보정 적용
# ─────────────────────────
def test_corrected_image_height():
    """
    보정 후 이미지 높이 = round(원본높이 × scale).
    너비(width)는 변경 없어야 함.
    """

# ─────────────────────────
# TC-05: 대칭성 검증
# ─────────────────────────
def test_model_symmetry():
    """
    투시투영 모델은 (θ - θ₀)와 -(θ - θ₀)에 대해 대칭이어야 함.
    h(θ₀ + δ) ≈ h(θ₀ - δ) (이론적으로 동일)
    """

# ─────────────────────────
# TC-06: 엣지 케이스
# ─────────────────────────
def test_edge_cases():
    """
    - θ = 0°에서 오류 없음
    - 매우 큰 각도(±80°)에서 ValueError 또는 경고 발생
    - 빈 이미지(0×0) 입력 시 ValueError 발생
    """
```

---

## 6. 파일 구조

```
Practices/
├── pitch_angle_analysis.ipynb     ← 분석 노트북 (Cell 1~9)
├── pitch_correction.py            ← 보정 함수 모듈
│   ├── class PitchCorrectionModel
│   │   ├── fit()
│   │   ├── predict_height()
│   │   └── correction_scale()
│   ├── correct_image_size()
│   └── measure_calendar_height()
└── test_pitch_correction.py       ← pytest 테스트
    ├── TC-01: test_model_fit_residuals
    ├── TC-02: test_correct_at_reference_angle_is_identity
    ├── TC-03: test_correction_scale_ordering
    ├── TC-04: test_corrected_image_height
    ├── TC-05: test_model_symmetry
    └── TC-06: test_edge_cases
```

---

## 7. 구현 순서 (Do Phase 체크리스트)

- [ ] **Step 1**: `pitch_correction.py` 생성 — `PitchCorrectionModel` 클래스 (fit, predict, scale)
- [ ] **Step 2**: `measure_calendar_height()` 구현 (blue_hough 방법)
- [ ] **Step 3**: `correct_image_size()` 구현
- [ ] **Step 4**: `pitch_angle_analysis.ipynb` 작성 (Cell 1~9 순서대로)
- [ ] **Step 5**: `test_pitch_correction.py` 작성 (TC-01~06)
- [ ] **Step 6**: `pytest Practices/test_pitch_correction.py` 실행 및 PASS 확인

---

## 8. 의존성

```txt
# requirements.txt 추가 항목
numpy>=1.24
opencv-python>=4.8
matplotlib>=3.7
pytest>=7.4
```

SciPy는 `scipy.optimize.curve_fit`으로 모델 피팅에 사용.
미설치 시 numpy의 polyfit으로 자동 폴백.

---

## 9. 설계 결정 사항 (Design Decisions)

| 결정 | 선택 | 이유 |
|------|------|------|
| 보정 대상 | 높이(H)만 | 피치각은 수직 투영에만 영향, 너비 변화 미미 |
| 기본 모델 | 투시투영 (1/(cos²θ - α²sin²θ)) | 단순 cos(θ)보다 정확, 3점 데이터로 피팅 가능 |
| 폴백 모델 | 2차 다항식 | SciPy 없는 환경 지원, numpy만으로 구현 가능 |
| 기준각 기본값 | 측정값 중 최솟값 각도 | 가장 왜곡이 적은 상태를 기준으로 |
| 달력 감지 주요 방법 | Blue Base + Hough | 흰 배경과 혼동 없음, 달력 고유 색상 활용 |

---

*PDCA Phase: Plan ✅ → **Design** → Do → Check → Act*
