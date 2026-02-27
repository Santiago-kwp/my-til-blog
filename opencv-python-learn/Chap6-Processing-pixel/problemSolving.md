# 챕터6 - 화소처리 연습문제 풀이

## 1. 그레이 스케일(gray-scale) 이미지가 의미하는 것이 무엇인지 설명하시오

**My answer** : 명암도 영상으로, 화소값을 0부터 255의 흑백 영상으로 저장하고, 0은 검정색, 255는 흰색으로 매핑하여 영상을 표현하는 것

**Claude 보완** :

핵심은 **단일 채널(1채널)** 영상이라는 점이다. 컬러 BGR 영상이 픽셀 하나에 B·G·R 3개의 값을 갖는 반면, 그레이스케일은 **밝기(intensity) 값 하나만** 갖는다.

| 구분 | 채널 수 | 픽셀당 메모리 | 표현 범위 |
|------|---------|------------|---------|
| 컬러 (BGR) | 3 | 3 byte | 약 1677만 색 |
| 그레이스케일 | 1 | 1 byte | 256 단계 밝기 |

> 메모리가 컬러의 1/3이며, 엣지 검출·모폴로지·히스토그램 분석 등 많은 알고리즘이 그레이스케일을 입력으로 요구한다.

---

## 2. 화소의 밝기와 화소값에 대해서 설명하시오

**My answer** : 화소의 밝기는 화소 값이 클수록 밝음을 뜻하고 낮을수록 어둡다는 것을 의미한다. 화소가 밝다는 것은 순수한 흰색에 가까우며, 어둡다는 것은 순수한 검정색에 가까운 것을 의미한다.

**Claude 보완** :

그레이스케일에서는 화소값 = 밝기가 1:1로 대응한다. 컬러 영상에서는 각 채널의 화소값이 해당 색상의 **강도(intensity)** 를 나타내며, 세 채널의 조합으로 최종 색상이 결정된다.

```
uint8 기준 화소값 범위: 0 ~ 255

  0        128        255
  ├──────────┼──────────┤
검정(Black) 회색(Gray) 흰색(White)
```

| 자료형 | 범위 | 흰색 | 검정 |
|--------|------|------|------|
| `uint8` | 0 ~ 255 | 255 | 0 |
| `float32` | 0.0 ~ 1.0 | 1.0 | 0.0 |

> `float32` 영상에서 OpenCV는 0.0~1.0을 0~255에 매핑하여 표시한다.

---

## 3. 두 개의 영상을 합성하는 방법을 두 가지 이상 기술하시오.

**My answer** : 두 개의 영상이 같은 너비와 높이(W, H)를 가질 때 같은 위치의 화소 값을 더하면 영상을 합성할 수 있다. 이때, 화소 값의 최대 범위가 정해져 있으므로, 두 화소 값을 더한 값이 Saturation(clipping) 되서 최댓값으로 될 수도 있고, 각 화소 값에 가중치를 곱하여 더할 수도 있다.

**Claude 보완** :

| 방법 | 함수 | 특징 |
|------|------|------|
| 포화 덧셈 | `cv2.add(img1, img2)` | 255 초과 시 255로 클리핑 |
| 가중 합산 (블렌딩) | `cv2.addWeighted(img1, α, img2, β, γ)` | `α·img1 + β·img2 + γ` |
| 마스크 기반 합성 | `cv2.bitwise_and/or` + mask | 특정 영역만 선택적으로 합성 |
| ROI 복사 합성 | `img[y:y+h, x:x+w] = roi` | 영상의 일부를 다른 영상에 덮어쓰기 |

```python
# 방법 1: 포화 덧셈
result1 = cv2.add(img1, img2)

# 방법 2: 가중 합산 (50:50 블렌딩)
result2 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

# 방법 3: 마스크 기반 합성 (img1의 특정 영역만 img2에 합성)
mask = np.zeros_like(img1)
mask[100:200, 100:200] = 255
fg = cv2.bitwise_and(img1, img1, mask=mask)
bg = cv2.bitwise_and(img2, img2, mask=cv2.bitwise_not(mask))
result3 = cv2.add(fg, bg)
```

---

## 4. 영상에서 밝기 변경과 명암 대비 변경의 차이를 설명하시오.

**My answer** : 밝기 변경은 명암도 영상에서 화소 값을 줄이거나 늘리는 것을 의미하며, 명암 대비 변경은 주변의 화소 값과의 차이를 곱셈 연산을 통해서 1 이상의 값을 곱하여 차이를 키우거나, 1 미만의 값을 곱하여 차이를 줄이는 것을 의미한다.

**Claude 보완** :

두 개념을 하나의 수식으로 통합해서 이해할 수 있다.

$$dst = a \times src + b$$

| 인수 | 역할 | 효과 |
|------|------|------|
| $a$ (scale) | 명암 대비 조절 | `a > 1`: 대비 증가, `0 < a < 1`: 대비 감소 |
| $b$ (shift) | 밝기 조절 | `b > 0`: 밝기 증가, `b < 0`: 밝기 감소 |

**히스토그램 관점의 차이**:

```
밝기 변경 (+b): 히스토그램 전체가 오른쪽으로 평행 이동
───────────────────────────────────────
원본:      ▃▅█▅▃
변경 후:         ▃▅█▅▃   (shift →)

명암 대비 변경 (×a): 히스토그램이 중심에서 펼쳐지거나 좁혀짐
───────────────────────────────────────
원본:    ▃▅█▅▃ (좁게 분포)
증가 후: ▂  ▃  █  ▃  ▂  (넓게 퍼짐)
```

```python
# 밝기 변경: cv2.add(src, 스칼라)
bright = cv2.add(img, 50)          # 밝기 +50

# 명암 대비 변경: cv2.multiply(src, scale)
contrast = cv2.multiply(img, 1.5)  # 대비 ×1.5

# 둘 다 동시 적용: convertScaleAbs(src, alpha, beta)
# dst = |alpha * src + beta|
dst = cv2.convertScaleAbs(img, alpha=1.5, beta=50)
```

---

## 5. 영상처리에서 히스토그램이란 무엇인가?

**My answer** : 영상처리에서의 히스토그램은 히스토그램의 빈으로 일정 범위의 화소 값이 같은 빈으로 분류되어, 하나의 영상에서 같은 빈으로 분류되는 화소의 개수를 히스토그램으로 나타내는 것을 뜻한다. 히스토그램을 통해서 하나의 영상의 화소 값 분포 정도를 알 수 있다.

**Claude 보완** :

히스토그램은 영상의 **화소값 분포를 시각적으로 표현**한 도표이다.

```
x축: 화소값 구간 (빈, bin) → 0 ~ 255
y축: 해당 구간에 속하는 화소 개수 (빈도수)
```

히스토그램 모양으로 영상의 특성을 즉시 파악할 수 있다.

| 히스토그램 모양 | 영상 특성 |
|----------------|---------|
| 왼쪽으로 치우침 | 어두운 영상 |
| 오른쪽으로 치우침 | 밝은 영상 |
| 중앙에 밀집 | 대비가 낮은 영상 |
| 전체에 넓게 분포 | 대비가 높은 영상 |

```python
# cv2.calcHist(images, channels, mask, histSize, ranges)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
# images  : 입력 영상 (리스트 형태로 전달)
# channels: 계산할 채널 인덱스 ([0]=그레이 또는 B, [1]=G, [2]=R)
# histSize: 빈(bin)의 개수 [256]
# ranges  : 화소값 범위 [0, 256]
```

---

## 6. 히스토그램 스트레칭의 과정을 기술하시오.

**My answer** : 히스토그램 스트레칭은 영상의 화소값과 화소의 개수를 히스토그램으로 나타낸 뒤, 화소 값의 최솟값과 최댓값을 구하여, 다음의 수식을 통해서 히스토그램 스트레칭을 하여 영상의 화소값의 분포를 넓게 만들 수 있다.

$$
\text{stretched} = \frac{\text{원본 화소값} - \text{최소 화소값}}{\text{최대 화소값} - \text{최소 화소값}} \times 255
$$

**Claude 보완** :

수식이 정확하다. 수식의 의미를 단계별로 풀면:

1. `(원본 - min)` : 최솟값을 0으로 이동
2. `/ (max - min)` : 전체 범위를 [0, 1]로 정규화
3. `× 255` : [0, 255] 범위로 스케일

결과적으로 **원본의 최솟값 → 0, 최댓값 → 255** 로 선형 변환되어 전체 범위를 최대한 활용한다.

```
원본 히스토그램 (좁은 범위)          스트레칭 후 (전체 범위 활용)
   min          max                     0                     255
    ├──▃▅█▅▃──┤             →          ├──▃────▅────█────▅────▃──┤
```

```python
min_val, max_val, _, _ = cv2.minMaxLoc(img)

# 방법 1: 직접 계산
ratio = 255.0 / (max_val - min_val)
stretched = np.round((img - min_val) * ratio).astype(np.uint8)

# 방법 2: cv2.normalize() 활용 (권장)
stretched = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
```

> `cv2.normalize(NORM_MINMAX)`는 내부적으로 히스토그램 스트레칭과 동일한 연산을 수행한다.

---

## 7. 히스토그램 평활화 과정을 기술하시오.

**My answer** :

1. 히스토그램을 만들고 누적 히스토그램 빈도수를 계산한다.
2. 누적 빈도수를 정규화한다.
3. 결과 화소 값 = 누적 빈도수 × 최대 화소값

**Claude 보완** :

단계를 수식과 함께 보완하면:

**① 히스토그램 계산** : $h(v)$ = 화소값 $v$의 개수

**② 누적 히스토그램(CDF) 계산** :

$$\text{cdf}(v) = \sum_{i=0}^{v} h(i)$$

**③ 정규화(0~255 스케일)**:

$$\text{dst}(v) = \frac{\text{cdf}(v) - \text{cdf}_{min}}{(H \times W) - \text{cdf}_{min}} \times 255$$

> 히스토그램 평활화의 목적은 히스토그램을 **균등 분포(uniform distribution)**에 가깝게 펼쳐 전체적인 대비를 향상시키는 것이다.

```
원본 (특정 구간에 몰려 있음)      평활화 후 (균등하게 분포)
█                                  ▅ ▅ ▅ ▅ ▅ ▅ ▅ ▅
█ █                     →         ▅ ▅ ▅ ▅ ▅ ▅ ▅ ▅
█ █ █                              ▅ ▅ ▅ ▅ ▅ ▅ ▅ ▅
0       128       255             0             255
```

```python
# OpenCV는 cv2.equalizeHist() 한 번으로 전 과정을 자동 처리
equalized = cv2.equalizeHist(gray_img)  # 단일 채널(그레이스케일)만 가능

# 컬러 영상에 적용하려면: YCrCb 변환 후 Y 채널(밝기)만 평활화
ycrcb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCrCb)
ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
```

> `cv2.equalizeHist()`는 그레이스케일 단일 채널 영상에만 직접 적용 가능하다. 컬러 영상에 적용하면 색상이 왜곡되므로, 밝기 채널(Y)만 분리해서 처리해야 한다.

---

## 8. `cv2.addWeighted()` 함수를 사용해서 두 영상을 합성하는 프로그램을 작성하시오.

## 9. 8번 문제에 두 개의 트랙바를 추가해서 각 영상의 반영 비율을 조절할 수 있도록 수정하시오.

`prob8-9.py` 참고

```python
import cv2

img1 = cv2.imread("images/add1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("images/add2.jpg", cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
cv2.createTrackbar("image1", "dst", 50, 100, lambda x: None)
cv2.createTrackbar("image2", "dst", 50, 100, lambda x: None)

while True:
    w1 = cv2.getTrackbarPos("image1", "dst") / 100  # 0~100 → 0.0~1.0
    w2 = cv2.getTrackbarPos("image2", "dst") / 100
    dst = cv2.addWeighted(img1, w1, img2, w2, 0)
    cv2.imshow("dst", dst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
```

**핵심 포인트**:

| 항목 | 설명 |
|------|------|
| `createTrackbar(name, window, value, count, callback)` | 초기값 50, 최대 100으로 트랙바 생성 |
| `getTrackbarPos() / 100` | 0~100 정수 → 0.0~1.0 실수로 변환 |
| `lambda x: None` | 트랙바 콜백 — 루프 내에서 직접 읽으므로 빈 함수 사용 |
| `addWeighted(img1, α, img2, β, γ)` | `α·img1 + β·img2 + γ` 수식 적용, `γ=0`은 순수 블렌딩 |

> `prob8-9.py` 초기 버전은 루프 밖에서 `dst`를 미리 생성한 뒤 루프에서 재사용했다. `prob8-9-updated.py`에서는 루프 내부에서 매번 새로 생성하는 방식으로 단순화했다. 후자가 코드가 더 간결하다.

---

## 10. 예제 \_6.2.1(`02.grayscale_image.py`)를 수정해서 np.float32(CV_32F)형으로 행렬을 선언하며, 회색이 점진적으로 짙어지는 영상을 만드시오

`prob10.py` 참고

```python
import numpy as np, cv2

image1 = np.zeros((50, 512), np.float32)  # float32 단일채널 영상 생성
rows, cols = image1.shape[:2]

for i in range(rows):
    for j in range(cols):
        image1[i, j] = j / (cols - 1)    # 0.0(검정) → 1.0(흰색) 점진적 증가

cv2.imshow("image1", image1)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**핵심 포인트**:

| 항목 | 설명 |
|------|------|
| `np.float32` 선언 | 픽셀값 범위 0.0 ~ 1.0 |
| `j / (cols - 1)` | 열 인덱스를 [0, 1] 범위로 정규화 |
| OpenCV float32 표시 | 0.0 → 검정, 1.0 → 흰색으로 자동 매핑 |

> `uint8`은 0~255 정수로 밝기를 표현하지만 `float32`는 0.0~1.0 실수로 표현한다. OpenCV `imshow()`는 두 타입 모두 자동으로 처리한다.

```python
# NumPy 벡터 연산으로 루프 없이 동일 결과 (더 빠름)
image2 = np.tile(np.linspace(0.0, 1.0, 512, dtype=np.float32), (50, 1))
```

---

## 11.`cv2.calcHist()` 함수는 1~3채널 영상에 대해서 히스토그램을 계산할 수 있다. 예제\_6.3.5(`11.histogram_stretching.py`)에서 `calc_histo()` 함수는 단일채널 영상에서 히스토그램을 계산하는데 `cv2.calcHist()` 함수와 같이 2채널 혹은 3채널 영상에서 2차원 혹은 3차원 히스토그램을 계산하도록 빈칸을 채우시오.

`prob11.py` 참조

```python
import numpy as np

def calc_histo(image, channels, bsize, ranges):
    # 채널이 2개 이상이면 다차원 shape, 1개면 (bsize[0], 1)
    shape = bsize if len(channels) > 1 else (bsize[0], 1)
    hist = np.zeros(shape, np.int32)      # 히스토그램 누적 행렬
    gap = np.divide(ranges[1::2], bsize)  # 각 채널의 계급 간격 계산

    for row in image:       # 행 순회
        for val in row:     # 열(픽셀) 순회
            idx = np.divide(val[channels], gap).astype('uint')  # 빈 인덱스 산출
            hist[tuple(idx)] += 1

    return hist
```

**핵심 포인트**:

| 항목 | 설명 |
|------|------|
| `bsize` | 각 채널의 빈 개수 — e.g. `[30, 48]` |
| `ranges[1::2]` | 슬라이싱으로 각 채널 최댓값만 추출 — e.g. `[180, 256, 256]` → `[180, 256]` (짝수 인덱스 1, 3, ...) |
| `gap = ranges_max / bsize` | 채널별 계급 간격 (`180/30=6`, `256/48≈5.3`) |
| `np.divide(val[channels], gap)` | 픽셀값을 간격으로 나눠 어느 빈에 속하는지 산출 |
| `hist[tuple(idx)] += 1` | 해당 (H, S, ...) 조합의 빈도 증가 |

```
사용 예시 (2채널):
calc_histo(hsv_img, channels=[0, 1], bsize=[30, 48], ranges=[0, 180, 0, 256])
→ cv2.calcHist([hsv_img], [0, 1], None, [30, 48], [0, 180, 0, 256]) 와 동일
```

---

## 12. 영상처리에서 투영(projection)은 다음의 수식으로 표현된다. OpenCV 함수 중에 `cv2.reduce()` 함수를 이용해서 수식과 같이 수직 및 수평 방향 투영을 수행하는 프로그램을 작성하고, 영상 파일을 읽어서 투영 히스토그램을 출력하시오.

$$
histo\_v(x) = \sum^{h-1}_{y=0}{f(x,y)}
$$

$$
histo\_h(y) = \sum^{w-1}_{x=0}{f(x,y)}, \quad f(x,y) = \text{좌표}(x,y)\text{의 화소값}
$$

`prob12.py` 참조

```python
import numpy as np, cv2
from Common.histogram import draw_histo

image = cv2.imread("images/pixel.jpg", cv2.IMREAD_GRAYSCALE)

# 수직 투영: 각 열의 화소값 합계 → (1, W) 행벡터
red0 = cv2.reduce(image, dim=0, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S)

# 수평 투영: 각 행의 화소값 합계 → (H, 1) 열벡터
red1 = cv2.reduce(image, dim=1, rtype=cv2.REDUCE_SUM, dtype=cv2.CV_32S)

# 합산 결과를 0~255 범위로 정규화 (시각화를 위해 uint8 변환)
norm0 = cv2.normalize(red0, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
norm1 = cv2.normalize(red1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# 정규화된 투영 벡터로 히스토그램 시각화
hist0 = cv2.calcHist(norm0, [0], None, [64], [0, 256])    # 수직 투영 히스토그램
hist1 = cv2.calcHist([norm1], [0], None, [64], [0, 256])  # 수평 투영 히스토그램

hist0_img = draw_histo(hist0)
hist1_img = draw_histo(hist1)
cv2.imshow("hist0 - vertical projection",   hist0_img)
cv2.imshow("hist1 - horizontal projection", hist1_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

**핵심 포인트**:

| 항목 | 설명 |
|------|------|
| `dtype=cv2.CV_32S` | 열/행 합산 시 최대 `255 × H` 가 되므로 uint8 범위 초과 → int32 필수 |
| `dim=0` (수직 투영) | 각 열의 값을 세로 방향으로 더함 → `(1, W)` 결과 |
| `dim=1` (수평 투영) | 각 행의 값을 가로 방향으로 더함 → `(H, 1)` 결과 |
| `cv2.normalize(NORM_MINMAX)` | int32 합산 결과를 히스토그램 시각화를 위해 uint8 범위로 정규화 |

```
수직 투영 histo_v(x): 각 열을 세로로 더함
┌─────────────────────┐
│   ░░  ██  ░░  ▒▒   │  → red0 = [ 300, 820, 120, 450 ... ]  (열별 합계)
│   ░░  ██  ░░  ▒▒   │
│   ░░  ██  ░░  ▒▒   │
└─────────────────────┘

수평 투영 histo_h(y): 각 행을 가로로 더함
┌──────────────┐ 340
│  ░░░░░░░░   │ 210   → red1 = [[340], [210], [580]] (행별 합계)
│  ░░████░░   │ 580
└──────────────┘
```

---

## 14. 컬러 영상 파일을 읽어 들여서 HSV 컬러 공간으로 변환하고, Hue 와 Saturation 채널로 2차원 히스토그램을 그림과 같이 만드시오. 즉, 2차원 히스토그램의 Hue(세로)와 Saturation(가로)을 2개 축으로 구성하고, 빈도값을 밝기로 표현해서 오른쪽 그림과 같이 2차원 그래프로 그리시오

> 조건
>
> 1.  계급 개수 : Hue 채널 30개, Saturation 채널: 48개
> 2.  결과 영상 크기 : 300X480

`prob14.py` 참조

```python
import numpy as np, cv2

image = cv2.imread("images/color_model.jpg", cv2.IMREAD_COLOR)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# H·S 2채널 2차원 히스토그램 계산: 결과 shape (30, 48)
histo2d = cv2.calcHist([image_hsv], [0, 1], None, [30, 48], [0, 180, 0, 256])

# 빈도값을 0~255 로 정규화 (V 채널 = 밝기로 사용)
cv2.normalize(histo2d, histo2d, 0, 255, cv2.NORM_MINMAX)

def draw_histo2(hist):
    """2D 히스토그램을 HSV 컬러 이미지로 시각화"""
    h, w = hist.shape[:2]
    hue_idx, sat_idx = np.indices(hist.shape)          # 빈 인덱스 그리드 생성
    ratios = np.array([180 / h, 256 / w, 256])         # 빈 인덱스 → 실제 HSV 값 비율
    graph = np.stack([hue_idx, sat_idx, hist], axis=2) # (h, w, 3) HSV 배열 구성
    graph = np.multiply(graph, ratios).astype(np.uint8)
    bgr = cv2.cvtColor(graph, cv2.COLOR_HSV2BGR)
    bgr = cv2.resize(bgr, (480, 300), interpolation=cv2.INTER_NEAREST)
    return bgr

dst = draw_histo2(histo2d)
cv2.imshow("2D Histogram H x S", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**핵심 포인트**:

| 항목 | 설명 |
|------|------|
| `calcHist([img], [0,1], None, [30,48], [0,180,0,256])` | H(0~180) × S(0~256) 2차원 히스토그램, 결과 shape `(30, 48)` |
| `normalize(0~255)` | 빈도수를 V(밝기)값으로 변환 |
| `np.indices(hist.shape)` | 각 빈의 H·S 인덱스를 그리드로 일괄 생성 |
| `np.stack([h, s, v], axis=2)` | H인덱스·S인덱스·빈도수를 HSV 채널로 조합 |
| `cv2.COLOR_HSV2BGR` | 각 (H, S) 조합의 색상을 실제 컬러로 변환하여 시각화 |
| `resize((480, 300))` | 조건에 맞는 결과 영상 크기 (가로480 × 세로300) 로 확대 |

**2차원 히스토그램 구조 이해**:

```
histo2d[i][j] = 영상에서 H가 i번 빈에, S가 j번 빈에 속하는 픽셀 수

          S=0   S=1  ... S=47   (가로축: Saturation)
  H=0   [   0,   0, ...,   0 ],
  H=1   [   3,   8, ...,   1 ],   ← 특정 Hue에서의 채도 분포
  ...
  H=29  [   0,   2, ...,   5 ] ]
  (세로축: Hue)

시각화 원리:
  빈도 높음 → V(밝기) 크게 → 밝은 색으로 표시
  빈도 낮음 → V(밝기) 작게 → 어두운 색으로 표시
  → 영상의 색상 분포를 2D 지도처럼 표현
```
