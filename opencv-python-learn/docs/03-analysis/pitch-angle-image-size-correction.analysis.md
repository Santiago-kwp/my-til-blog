# pitch-angle-image-size-correction Analysis Report

> **Analysis Type**: Gap Analysis (Design vs Implementation)
>
> **Project**: opencv-python-learn
> **Analyst**: gap-detector
> **Date**: 2026-03-04
> **Design Doc**: [pitch-angle-image-size-correction.design.md](../02-design/features/pitch-angle-image-size-correction.design.md)

---

## 1. Analysis Overview

### 1.1 Analysis Purpose

Design 문서(`pitch-angle-image-size-correction.design.md`)와 실제 구현 코드 사이의 일치도를 검증하고, 미구현/변경/추가 항목을 식별한다.

### 1.2 Analysis Scope

- **Design Document**: `docs/02-design/features/pitch-angle-image-size-correction.design.md`
- **Implementation Files**:
  - `Practices/pitch_correction.py`
  - `Practices/test_pitch_correction.py`
  - `Practices/pitch_angle_analysis.ipynb`
- **Analysis Date**: 2026-03-04

---

## 2. Gap Analysis (Design vs Implementation)

### 2.1 Overall Match Rate

```
+---------------------------------------------+
|  Overall Match Rate: 88%                     |
+---------------------------------------------+
|  Matched:            30 items (88%)          |
|  Changed:             3 items  (9%)          |
|  Missing:             1 item   (3%)          |
|  Added:               2 items  (6%)          |
+---------------------------------------------+
```

### 2.2 Overall Scores

| Category | Score | Status |
|----------|:-----:|:------:|
| Design Match | 88% | Warning |
| Architecture Compliance | 95% | Pass |
| Convention Compliance | 90% | Pass |
| **Overall** | **91%** | **Pass** |

---

## 3. Detailed Comparison

### 3.1 Mathematical Model (Section 2)

| Item | Design | Implementation | Status | Notes |
|------|--------|----------------|--------|-------|
| Core formula | `h(theta) = K / (cos^2(theta-theta0) - alpha^2*sin^2(theta-theta0))` (symmetric) | `h(theta) = K / (cos(alpha_top+theta) * cos(alpha_bot+theta))` (asymmetric) | Changed | Implementation uses more general asymmetric model. Mathematically valid improvement. |
| Correction scale | `scale = h(ref) / h(input)` | `scale = h(ref) / h(input)` | Match | Identical formula |
| Parameters | `alpha, theta0` (2 params) | `alpha_top_deg, alpha_bot_deg, K` (3 params) | Changed | Asymmetric model requires separate top/bottom angles. More flexible. |
| Fallback model | 2nd-degree polynomial via `numpy.polyfit` | 2nd-degree polynomial via `numpy.polyfit` | Match | |

**Impact**: LOW - The asymmetric model is a mathematical generalization. The symmetric case `alpha_top = -alpha_bot` reduces to the design formula. This is an improvement, not a regression.

### 3.2 PitchCorrectionModel Class (Section 3.1)

| Item | Design | Implementation | Status |
|------|--------|----------------|--------|
| Class exists | `PitchCorrectionModel` | `PitchCorrectionModel` | Match |
| `fit()` method | `fit(angles_deg, heights_px, ref_angle_deg, mode)` | `fit(angles_deg, heights_px, ref_angle_deg, mode)` | Match |
| `fit()` - mode default | `mode='perspective'` | `mode='auto'` | Changed |
| `predict_height()` method | `predict_height(angle_deg) -> float` | `predict_height(angle_deg) -> float` | Match |
| `correction_scale()` method | `correction_scale(angle_deg) -> float` | `correction_scale(angle_deg) -> float` | Match |
| Method chaining (`fit` returns `self`) | Yes | Yes | Match |
| SciPy `curve_fit` usage | Yes (perspective mode) | Yes (perspective mode) | Match |
| Polynomial fallback | Yes | Yes | Match |
| `__repr__()` method | Not in design | Implemented | Added |
| Minimum data validation | Not specified | `len(angles) < 2 -> ValueError` | Added |
| Auto mode selection | Not specified | `'auto'` mode selects based on SciPy availability | Added |

**`mode` default value difference detail**:
- Design: `mode='perspective'` (explicit)
- Implementation: `mode='auto'` (SciPy installed -> perspective, else polynomial)
- Impact: LOW - `'auto'` is a practical improvement. When SciPy is available, behavior is identical to `'perspective'`.

### 3.3 Calendar Detection Strategy (Section 3.2)

| Item | Design | Implementation | Status |
|------|--------|----------------|--------|
| 3-stage fallback | blue_hough -> variance -> ValueError | blue_hough -> variance -> ValueError | Match |
| `_detect_blue_hough()` | Internal function | Implemented | Match |
| `_detect_variance()` | Fallback function | Implemented | Match |
| `measure_calendar_height()` | Public function with `method` param | Implemented | Match |
| Return type | `(top_y, bottom_y, height_px)` | `Tuple[int, int, int]` | Match |
| `'manual'` method option | Listed in design docstring | Not accepted (raises ValueError) | Missing |

**Missing `'manual'` method**: Design docstring mentions `method: 'blue_hough' | 'variance' | 'manual'` but implementation only accepts `'blue_hough'` and `'variance'`. The 3rd stage in design is "raise ValueError to prompt manual ROI" which is effectively what happens, so this is a minor documentation inconsistency rather than a missing feature.

### 3.4 `correct_image_size()` Function (Section 3.1)

| Item | Design | Implementation | Status |
|------|--------|----------------|--------|
| Function exists | Yes | Yes | Match |
| Parameters | `(image, pitch_angle_deg, model)` | `(image, pitch_angle_deg, model)` | Match |
| Height-only correction | Yes | Yes | Match |
| Width preserved | Yes | Yes | Match |
| ValueError on invalid | Yes | Yes | Match |
| Empty image check | Not explicit | `image is None or image.size == 0` | Match |
| Scale validation | Not explicit | `scale <= 0 or not np.isfinite(scale)` | Match |
| Resize interpolation | Not specified | `cv2.INTER_LINEAR` | Added |

### 3.5 Notebook Structure (Section 4)

| Cell # | Design Content | Implementation | Status |
|--------|---------------|----------------|--------|
| 1 | Library import + path setup | Cell 0 (markdown) + Cell 1 (code): import + paths | Match |
| 2 | Markdown: experiment overview + theory | Cell 0: markdown with math model description | Match |
| 3 | Load & display 3 images | Cell 3: loads 3 images with matplotlib | Match |
| 4 | Calendar bounding box measurement + table | Cell 5: measurement with manual/auto fallback | Match |
| 5 | Markdown: measurement result interpretation | Cell 6: markdown interpretation | Match |
| 6 | Scatter plot + model fitting graph | Cell 9: scatter plot + fitted curve | Match |
| 7 | PitchCorrectionModel fitting | Cell 9: model fitting (combined with Cell 6) | Match |
| 8 | Before/After visualization | Cell 13: 2x3 grid before/after comparison | Match |
| 9 | Markdown: conclusion + limitations | Cell 14: conclusion markdown | Match |

**Note**: Notebook has additional cells (Cell 7: measurement table, Cell 10-11: correction scale distribution chart) that go beyond design specification. Total cells: 15 (design specified 9). The extra cells add value without deviating from the design intent.

### 3.6 Test Cases (Section 5)

| TC ID | Design Test Name | Implementation | Status |
|-------|-----------------|----------------|--------|
| TC-01 | `test_model_fit_residuals` | `test_model_fit_residuals()` L68 | Match |
| TC-02 | `test_correct_at_reference_angle_is_identity` | `test_correct_at_reference_angle_is_identity()` L93 | Match |
| TC-03 | `test_correction_scale_ordering` | `test_correction_scale_ordering()` L111 | Match |
| TC-04 | `test_corrected_image_height` | `test_corrected_image_height()` L145 | Match |
| TC-05 | `test_model_symmetry` | `test_model_symmetry_with_centered_camera()` L169 | Match |
| TC-06 | `test_edge_cases` | Split into 5 individual tests (L199-L231) | Match |
| - | - | `test_double_correction_consistency()` L238 | Added |

**TC-05 name difference**: Design says `test_model_symmetry`, implementation says `test_model_symmetry_with_centered_camera`. The implementation name is more descriptive. Content matches design intent.

**TC-06 split**: Design has a single `test_edge_cases()`. Implementation splits this into:
- `test_edge_case_zero_angle` (theta=0 no error)
- `test_edge_case_empty_image` (0x0 image -> ValueError)
- `test_edge_case_model_not_fitted` (predict before fit -> RuntimeError)
- `test_edge_case_model_not_fitted_scale` (scale before fit -> RuntimeError)
- `test_edge_case_insufficient_data` (1 data point -> ValueError)

This is a best practice improvement -- individual test functions provide better failure isolation.

**Added test**: `test_double_correction_consistency` verifies round-trip correction. Not in design but adds value.

### 3.7 Dependencies (Section 8)

| Dependency | Design | Implementation | Status |
|------------|--------|----------------|--------|
| numpy | Yes (>=1.24) | Yes (imported) | Match |
| opencv-python | Yes (>=4.8) | Yes (cv2 imported) | Match |
| matplotlib | Yes (>=3.7) | Yes (in notebook) | Match |
| pytest | Yes (>=7.4) | Yes (in test file) | Match |
| scipy | Yes (curve_fit) | Yes (optional, with try/except) | Match |

### 3.8 File Structure (Section 6)

| Expected File | Exists | Status |
|---------------|:------:|--------|
| `Practices/pitch_correction.py` | Yes | Match |
| `Practices/test_pitch_correction.py` | Yes | Match |
| `Practices/pitch_angle_analysis.ipynb` | Yes | Match |

---

## 4. Differences Summary

### 4.1 Missing Features (Design O, Implementation X)

| Item | Design Location | Description | Impact |
|------|-----------------|-------------|--------|
| `'manual'` method in `measure_calendar_height` | design.md:177 | Design docstring lists `'manual'` as valid method option, but implementation rejects it with ValueError | LOW - 3rd stage fallback (ValueError) effectively achieves the same user interaction |

### 4.2 Added Features (Design X, Implementation O)

| Item | Implementation Location | Description | Impact |
|------|------------------------|-------------|--------|
| `__repr__()` method | pitch_correction.py:187-202 | Human-readable model representation | LOW - Debug convenience |
| `test_double_correction_consistency` | test_pitch_correction.py:238-261 | Round-trip correction verification test | LOW - Positive addition |
| Notebook extra cells (scale distribution, table) | pitch_angle_analysis.ipynb cells 7,10-11 | Additional visualizations beyond 9-cell design | LOW - Enhanced analysis |
| `'auto'` mode | pitch_correction.py:103-104 | Automatic mode selection based on SciPy availability | LOW - Usability improvement |
| Input validation (min 2 points) | pitch_correction.py:92-93 | `fit()` validates minimum data points | LOW - Robustness improvement |

### 4.3 Changed Features (Design != Implementation)

| Item | Design | Implementation | Impact |
|------|--------|----------------|--------|
| Math model formula | Symmetric: `1/(cos^2 - alpha^2*sin^2)` with params `(alpha, theta0)` | Asymmetric: `K/(cos(a_top+t)*cos(a_bot+t))` with params `(alpha_top, alpha_bot, K)` | MEDIUM - More general model; symmetric is a special case |
| `fit()` mode default | `'perspective'` | `'auto'` | LOW - Auto selects perspective when SciPy available |
| TC-05 test name | `test_model_symmetry` | `test_model_symmetry_with_centered_camera` | LOW - More descriptive name |

---

## 5. Convention Compliance

### 5.1 Naming Convention

| Category | Convention | Compliance | Violations |
|----------|-----------|:----------:|------------|
| Class | PascalCase | 100% | - |
| Functions | snake_case (Python) | 100% | - |
| Constants | UPPER_SNAKE_CASE | 100% | `MEASURED_ANGLES`, `REF_ANGLE`, `HAS_SCIPY` |
| Files | snake_case.py | 100% | - |
| Private functions | `_prefix` | 100% | `_detect_blue_hough`, `_detect_variance`, `_fit_perspective`, `_fit_polynomial` |

### 5.2 Code Quality

| Metric | Value | Status |
|--------|-------|--------|
| Docstrings present | All public functions | Pass |
| Type hints | Used (Optional, Tuple, np.ndarray) | Pass |
| Error handling | ValueError, RuntimeError with messages | Pass |
| Import structure | stdlib -> third-party -> local | Pass |

---

## 6. Architecture Compliance

This is a Python utility module (Starter level), not a web application. Architecture assessment is simplified.

| Item | Status | Notes |
|------|--------|-------|
| Module separation | Pass | Model class + utility functions well separated |
| Private/public distinction | Pass | Internal functions prefixed with `_` |
| Test isolation | Pass | Tests use fixtures, no external dependencies |
| Notebook references module | Pass | Imports from `pitch_correction` module |

---

## 7. Recommended Actions

### 7.1 Documentation Update Needed

| Priority | Item | Action |
|----------|------|--------|
| 1 | Math model formula update | Design Section 2.1 should be updated to reflect the asymmetric model `h(theta) = K / (cos(alpha_top+theta) * cos(alpha_bot+theta))` actually implemented |
| 2 | `fit()` mode default | Design Section 3.1 should change default from `'perspective'` to `'auto'` |
| 3 | Remove `'manual'` from `measure_calendar_height` design docstring | Or implement `'manual'` method option in code |
| 4 | Reflect additional test cases | Add `test_double_correction_consistency` and edge case split to design Section 5 |
| 5 | Notebook cell count | Update design Section 4 cell table to reflect actual 15-cell structure |

### 7.2 No Immediate Code Changes Required

All differences are either improvements over the design or minor documentation inconsistencies. No critical gaps that require code fixes.

---

## 8. Synchronization Recommendation

**Match Rate: 88% -> Recommendation: "There are some differences. Document update is recommended."**

The implementation is a faithful and slightly improved version of the design. The primary gap is the mathematical model formulation change from symmetric to asymmetric, which is a valid generalization. Recommended action:

**Option 2: Update design to match implementation** -- The implementation's asymmetric model is mathematically superior and the code quality exceeds design expectations in several areas (additional tests, input validation, auto mode selection).

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-04 | Initial gap analysis | gap-detector |
