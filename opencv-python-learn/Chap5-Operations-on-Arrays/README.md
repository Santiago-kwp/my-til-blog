# 5. 기본 배열 연산 (Operations on Arrays)

## 목차

- [5.1 기본 배열 처리 함수](#51-기본-배열-처리-함수)
- [5.2 채널 처리 함수](#52-채널-처리-함수)
- [5.3 산술 연산 함수](#53-산술-연산-함수)
  - [5.3.1 사칙 연산](#531-사칙-연산)
  - [5.3.2 지수·로그·제곱근 관련 함수](#532-지수로그제곱근-관련-함수)
  - [5.3.3 논리(비트) 연산 함수](#533-논리비트-연산-함수)
- [5.4 절댓값 연산](#54-절댓값-연산)
  - [5.4.1 원소의 최솟값과 최댓값](#541-원소의-최솟값과-최댓값)
- [5.5 통계 관련 함수](#55-통계-관련-함수)
- [5.6 행렬 연산 함수](#56-행렬-연산-함수)

---

## Chapter 5 전체 구조

```mermaid
mindmap
  root((Chap5 배열 연산))
    기본 배열 처리
      flip 뒤집기
      repeat 반복
      transpose 전치
    채널 처리
      merge 합성
      split 분리
    산술 연산
      사칙연산 add subtract multiply divide
      지수로그 exp log sqrt pow
      크기각도 magnitude phase cartToPolar
      비트연산 and or xor not
    절댓값
      absdiff
      convertScaleAbs
      min max minMaxLoc
    통계
      sumElems mean meanStdDev
      sort sortIdx reduce
    행렬 연산
      gemm 행렬곱
      invert 역행렬
      solve 연립방정식
```

---

## 5.1 기본 배열 처리 함수

> 행렬(배열)의 형태를 변환하는 함수들이다.
> 카메라 영상처럼 좌우가 뒤집힌 영상을 보정하거나, 영상을 반복·전치하는 데 활용한다.

### 주요 함수

| 함수 | 설명 |
|------|------|
| `cv2.flip(src, flipCode[, dst])` | 배열을 수직/수평/양축으로 뒤집는다 |
| `cv2.repeat(src, ny, nx[, dst])` | 배열을 세로 ny회, 가로 nx회 반복한다 |
| `cv2.transpose(src[, dst])` | 배열의 전치 행렬을 반환한다 |

### `cv2.flip()` flipCode 기준

```mermaid
graph LR
    SRC["원본 영상"]
    F0["flipCode = 0<br/>수평축 기준<br/>(상하 뒤집기)"]
    F1["flipCode = 1<br/>수직축 기준<br/>(좌우 뒤집기)"]
    FM1["flipCode = -1<br/>양축 기준<br/>(상하+좌우 뒤집기)"]

    SRC --> F0
    SRC --> F1
    SRC --> FM1

    style F0 fill:#d4edda
    style F1 fill:#cce5ff
    style FM1 fill:#f8d7da
```

| flipCode | 기준 축 | 효과 |
|----------|---------|------|
| `0` | 수평축 (x-axis) | 상하 반전 |
| `1` | 수직축 (y-axis) | 좌우 반전 (거울 효과) |
| `-1` | 양축 동시 | 상하 + 좌우 반전 (180도 회전과 동일) |

### `[, dst]` 인수의 의미

```python
# dst 생략 → 새 배열 반환
flipped = cv2.flip(img, 1)

# dst 지정 → 결과가 dst 배열에 저장 (메모리 재사용)
dst = np.empty_like(img)
cv2.flip(img, 1, dst)
```

> `[dst]`는 선택적 인수이다. 생략하면 OpenCV가 새 배열을 만들어 반환하고,
> 지정하면 해당 배열에 결과를 저장하므로 메모리를 재사용할 수 있다.

### 예시 코드 (`01.mat_array.py`)

```python
import numpy as np, cv2

image = cv2.imread('images/flip_test.jpg', cv2.IMREAD_COLOR)

x_axis   = cv2.flip(image, 0)   # 상하 반전
y_axis   = cv2.flip(image, 1)   # 좌우 반전
xy_axis  = cv2.flip(image, -1)  # 상하+좌우 반전
rep_image   = cv2.repeat(image, 1, 2)   # 가로 방향으로 2회 반복
trans_image = cv2.transpose(image)      # 전치 (행↔열 교환)
```

### transpose() 동작 원리

```
원본 (M×N):          전치 (N×M):
[ a  b  c ]          [ a  d ]
[ d  e  f ]    →     [ b  e ]
                     [ c  f ]

행과 열이 교환됨
영상에서는 90도 회전과 유사하지만 정확히 같지 않음
```

---

## 5.2 채널 처리 함수

> OpenCV에서 컬러 영상은 **BGR 3채널** 행렬로 저장된다.
> 채널을 분리하거나 합성하여 특정 채널만 처리할 수 있다.

```mermaid
flowchart LR
    MULTI["다채널 배열<br/>(H × W × 3)"]
    CH0["B 채널<br/>(H × W)"]
    CH1["G 채널<br/>(H × W)"]
    CH2["R 채널<br/>(H × W)"]

    MULTI -- "cv2.split()" --> CH0
    MULTI -- "cv2.split()" --> CH1
    MULTI -- "cv2.split()" --> CH2

    CH0 -- "cv2.merge()" --> MULTI
    CH1 -- "cv2.merge()" --> MULTI
    CH2 -- "cv2.merge()" --> MULTI

    style MULTI fill:#4a90d9,color:#fff
    style CH0 fill:#0056b3,color:#fff
    style CH1 fill:#28a745,color:#fff
    style CH2 fill:#dc3545,color:#fff
```

### 주요 함수

| 함수 | 설명 |
|------|------|
| `cv2.merge(mv[, dst])` | 단일채널 배열들을 → 다채널 배열로 합성 |
| `cv2.split(m[, mv])` | 다채널 배열을 → 단일채널 배열들로 분리 |

### 채널 분리/합성 예시 (`02.mat_channel.py`)

```python
import numpy as np, cv2

ch0 = np.zeros((2, 4), np.uint8) + 10   # 값 10으로 채워진 채널
ch1 = np.ones((2, 4), np.uint8) * 20    # 값 20
ch2 = np.full((2, 4), 30, np.uint8)     # 값 30

list_bgr  = [ch0, ch1, ch2]
merge_bgr = cv2.merge(list_bgr)   # (2, 4, 3) 다채널 행렬
split_bgr = cv2.split(merge_bgr)  # 다시 3개의 단일채널로 분리

print(merge_bgr.shape)             # (2, 4, 3)
print(np.array(split_bgr).shape)   # (3, 2, 4)
```

> `cv2.split()`의 반환값은 **튜플**이다. (numpy 배열의 리스트가 아님)

### 실제 컬러 영상 채널 분리 (`03.image_channels.py`)

```python
image = cv2.imread("images/color.jpg", cv2.IMREAD_COLOR)
bgr = cv2.split(image)  # B, G, R 채널을 각각 분리

cv2.imshow("Blue channel",  bgr[0])  # 파란색이 많은 영역이 밝게 나타남
cv2.imshow("Green channel", bgr[1])
cv2.imshow("Red channel",   bgr[2])
```

| 채널 분리 결과 | 해석 |
|---------------|------|
| Blue 채널 밝은 영역 | 원본 영상에서 파란색이 강한 부분 |
| Green 채널 밝은 영역 | 원본 영상에서 초록색이 강한 부분 |
| Red 채널 밝은 영역 | 원본 영상에서 빨간색이 강한 부분 |

---

## 5.3 산술 연산 함수

### 5.3.1 사칙 연산

> OpenCV의 산술 연산은 **포화 연산(Saturate)**을 수행한다.
> 결과값이 자료형의 범위를 초과하면 최솟값/최댓값으로 클리핑된다.
> (예: uint8에서 255+10 = 255, 0-10 = 0)

```mermaid
graph TD
    ARITH["사칙 연산 함수"]
    ARITH --> ADD["cv2.add(src1, src2)<br/>합산 (포화 연산)"]
    ARITH --> SUB["cv2.subtract(src1, src2)<br/>차분 (포화 연산)"]
    ARITH --> MUL["cv2.multiply(src1, src2)<br/>원소 간 곱"]
    ARITH --> DIV["cv2.divide(src1, src2)<br/>원소 간 나눗셈"]
    ARITH --> WGT["cv2.addWeighted()<br/>가중 합산"]

    style ARITH fill:#6c757d,color:#fff
    style ADD fill:#d4edda
    style SUB fill:#f8d7da
    style MUL fill:#cce5ff
    style DIV fill:#fff3cd
    style WGT fill:#e2d9f3
```

#### 주요 공통 인수

| 인수 | 설명 |
|------|------|
| `src1`, `src2` | 입력 배열 또는 스칼라 |
| `dst` | 결과 출력 배열 |
| `mask` | 8비트 단일채널 마스크 — 0이 아닌 위치만 연산 수행 |
| `dtype` | 출력 배열의 자료형 |

#### `cv2.add()` / `cv2.subtract()`

```python
m1 = np.full((3, 6), 10, np.uint8)
m2 = np.full((3, 6), 50, np.uint8)

# 마스크: 오른쪽 절반(3열~)만 연산 수행
m_mask = np.zeros(m1.shape, np.uint8)
m_mask[:, 3:] = 1

m_add1 = cv2.add(m1, m2)               # 전체 덧셈
m_add2 = cv2.add(m1, m2, mask=m_mask)  # 마스크 영역만 덧셈
```

#### `cv2.multiply()` — scale 인수 주의

```
cv2.multiply(src1, src2[, dst[, scale[, dtype]]])
```

- `scale`: 두 배열의 원소 곱에 추가로 곱해주는 배율
- 수식: `dst(i) = saturate(src1(i) × src2(i) × scale)`

#### `cv2.addWeighted()` — 영상 블렌딩에 자주 사용

```
cv2.addWeighted(src1, alpha, src2, beta, gamma)
```

$$dst = \alpha \cdot src1 + \beta \cdot src2 + \gamma$$

| 인수 | 설명 |
|------|------|
| `alpha` | src1의 가중치 |
| `beta` | src2의 가중치 |
| `gamma` | 합산 결과에 추가로 더해주는 스칼라 |

```python
# 예: 두 영상을 50:50으로 합성
blended = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
```

#### uint8 vs float32 나눗셈 비교 (`04.arithmetic_op.py`)

```python
m1 = np.full((3, 6), 10, np.uint8)
m2 = np.full((3, 6), 50, np.uint8)

m_div1 = cv2.divide(m1, m2)                          # uint8 → 소수점 버림 (0)
m1 = m1.astype(np.float32)
m2 = np.float32(m2)
m_div2 = cv2.divide(m1, m2)                          # float32 → 0.2 정확히 계산
```

> uint8 나눗셈 시 소수 부분이 버려진다.
> 정밀한 나눗셈 결과가 필요하면 반드시 **float32** 형변환 후 연산한다.

---

### 5.3.2 지수·로그·제곱근 관련 함수

```mermaid
graph LR
    MATH["수학 함수"]
    MATH --> EXP["cv2.exp(src)<br/>e^x"]
    MATH --> LOG["cv2.log(src)<br/>ln(|x|)"]
    MATH --> SQRT["cv2.sqrt(src)<br/>√x"]
    MATH --> POW["cv2.pow(src, p)<br/>x^p"]
    MATH --> MAG["cv2.magnitude(x, y)<br/>√(x²+y²)"]
    MATH --> PHA["cv2.phase(x, y)<br/>atan2(y, x)"]
    MATH --> CTP["cv2.cartToPolar(x, y)<br/>직교→극"]
    MATH --> PTC["cv2.polarToCart(mag, ang)<br/>극→직교"]

    style MATH fill:#6c757d,color:#fff
```

> 모든 수학 함수는 **ndarray 객체만** 입력 가능하다. 파이썬 리스트는 직접 전달 불가.

#### 기본 수학 함수

| 함수 | 수식 | 비고 |
|------|------|------|
| `cv2.exp(src)` | $e^{src}$ | 자연지수 |
| `cv2.log(src)` | $\ln(\|src\|)$ | 자연로그, 절댓값 먼저 |
| `cv2.sqrt(src)` | $\sqrt{src}$ | 제곱근 |
| `cv2.pow(src, p)` | $src^p$ | p승 |

```python
v1 = np.array([1, 2, 3], np.float32)   # float32 필수
v2 = np.array([[1], [2], [3]], np.float32)  # 열벡터 (3×1)
v3 = np.array([[1, 2, 3]], np.float32)      # 행벡터 (1×3)

v1_exp  = cv2.exp(v1)
v1_log  = cv2.log(v1)
v2_sqrt = cv2.sqrt(v2)
v3_pow  = cv2.pow(v3, 3)   # 세제곱

# 열벡터 출력 시 활용하는 변환 패턴
print(v1_log.transpose())  # 전치 → 행벡터
print(np.ravel(v2_sqrt))   # ravel() → 1차원 배열
print(v3_pow.flatten())    # flatten() → 1차원 배열
```

#### 크기(magnitude)와 각도(phase)

$$magnitude(i) = \sqrt{x(i)^2 + y(i)^2}$$

$$angle(i) = \text{atan2}(y(i), x(i))$$

```mermaid
graph LR
    XY["직교 좌표<br/>(x, y)"]
    POLAR["극 좌표<br/>(magnitude, angle)"]

    XY -- "cv2.cartToPolar()" --> POLAR
    POLAR -- "cv2.polarToCart()" --> XY

    style XY fill:#d4edda
    style POLAR fill:#cce5ff
```

```python
x = np.array([1, 2, 3, 5, 10], np.float32)
y = np.array([2, 5, 6, 2,  9], np.float32)

mag = cv2.magnitude(x, y)           # 크기 계산
ang = cv2.phase(x, y)               # 각도 계산 (기본: 라디안)
p_mag, p_ang = cv2.cartToPolar(x, y)    # 직교 → 극 좌표 동시 변환
x2, y2 = cv2.polarToCart(p_mag, p_ang) # 극 → 직교 좌표 복원
```

| 인수 | 설명 |
|------|------|
| `anglenDegrees=True` | 각도를 도(degree)로 반환 |
| `anglenDegrees=False` (기본값) | 각도를 라디안으로 반환 |

---

### 5.3.3 논리(비트) 연산 함수

> 비트 단위 연산으로 영상의 특정 영역을 추출하거나 마스킹할 때 핵심적으로 사용된다.

#### 진리표

| 비트 A | 비트 B | AND | OR | XOR | NOT A |
|--------|--------|-----|----|-----|-------|
| 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 |

#### 함수 목록

| 함수 | 연산 | 특징 |
|------|------|------|
| `cv2.bitwise_and(src1, src2)` | 비트별 AND | 두 영역의 교집합 추출 |
| `cv2.bitwise_or(src1, src2)` | 비트별 OR | 두 영역의 합집합 |
| `cv2.bitwise_xor(src1, src2)` | 비트별 XOR | 두 영역이 다른 부분만 추출 |
| `cv2.bitwise_not(src)` | 비트별 NOT | 흑백 반전 |

```mermaid
graph TD
    subgraph 원본 영상들
        IMG1["image1<br/>원 (흰색)"]
        IMG2["image2<br/>사각형 (흰색)"]
    end

    subgraph 비트 연산 결과
        OR["bitwise_OR<br/>원 + 사각형 합집합"]
        AND["bitwise_AND<br/>원과 사각형 겹치는 부분"]
        XOR["bitwise_XOR<br/>겹치지 않는 부분만"]
        NOT["bitwise_NOT<br/>흑백 반전"]
    end

    IMG1 --> OR; IMG2 --> OR
    IMG1 --> AND; IMG2 --> AND
    IMG1 --> XOR; IMG2 --> XOR
    IMG1 --> NOT
```

```python
# 07.bitwise_op.py
image1 = np.zeros((300, 300), np.uint8)
image2 = image1.copy()
cx, cy = 150, 150

cv2.circle(image1, (cx, cy), 100, 255, -1)       # 원
cv2.rectangle(image2, (0, 0, cx, 300), 255, -1)  # 좌측 절반 사각형

image3 = cv2.bitwise_or(image1, image2)   # 합집합
image4 = cv2.bitwise_and(image1, image2)  # 교집합
image5 = cv2.bitwise_xor(image1, image2)  # 차집합
image6 = cv2.bitwise_not(image1)          # 반전
```

#### 실전 응용 — 로고 합성 (`08.bitwise_overlap.py`)

```mermaid
flowchart TD
    LOGO["로고 영상"]
    THRESH["이진화 (threshold)<br/>220보다 크면 255, 작으면 0"]
    SPLIT["채널 분리 (split)<br/>3채널 → 단일채널 3개"]
    FGMASK["전경 마스크 생성<br/>OR 연산으로 3채널 마스크 합성"]
    BGMASK["배경 마스크 생성<br/>NOT 연산"]
    FG["foreground<br/>로고 전경 (bitwise_and + fg_mask)"]
    BG["background<br/>원본 roi 배경 (bitwise_and + bg_mask)"]
    RESULT["합성 결과<br/>add(background, foreground)"]

    LOGO --> THRESH --> SPLIT --> FGMASK
    FGMASK --> BGMASK
    FGMASK --> FG
    BGMASK --> BG
    FG --> RESULT
    BG --> RESULT

    style RESULT fill:#d4edda
```

```python
# 이진화로 로고의 마스크 생성
masks = cv2.threshold(logo, 220, 255, cv2.THRESH_BINARY)[1]
masks = cv2.split(masks)

fg_pass_mask = cv2.bitwise_or(masks[0], masks[1])
fg_pass_mask = cv2.bitwise_or(masks[2], fg_pass_mask)  # 전경 마스크
bg_pass_mask = cv2.bitwise_not(fg_pass_mask)            # 배경 마스크

foreground = cv2.bitwise_and(logo, logo, mask=fg_pass_mask)  # 로고 전경
background = cv2.bitwise_and(roi,  roi,  mask=bg_pass_mask)  # 원본 배경
dst = cv2.add(background, foreground)  # 합성
```

---

## 5.4 절댓값 연산

> 영상 차분(Frame Difference) 등에서 음수값이 발생할 때 절댓값으로 변환하여 다음 처리 단계로 넘긴다.

### 주요 함수

| 함수 | 수식 | 설명 |
|------|------|------|
| `cv2.absdiff(src1, src2)` | $\|src1 - src2\|$ | 두 배열 간 차분의 절댓값 |
| `cv2.convertScaleAbs(src, alpha, beta)` | $\|src \times \alpha + \beta\|$ → uint8 | 스케일 + 절댓값 + uint8 변환 |

```mermaid
flowchart LR
    A["image1 (uint8)"]
    B["image2 (uint8)"]

    SUB1["cv2.subtract()<br/>uint8 포화: 음수→0 클리핑"]
    SUB2["int16 변환 후 subtract<br/>음수 보존 가능"]
    ABS1["np.absolute().astype('uint8')<br/>절댓값 변환"]
    ABS2["cv2.absdiff()<br/>내부적으로 절댓값 계산"]

    A --> SUB1; B --> SUB1
    A --> SUB2; B --> SUB2
    SUB2 --> ABS1
    A --> ABS2; B --> ABS2

    style ABS2 fill:#d4edda
    style SUB1 fill:#f8d7da
```

```python
# 10.mat_abs.py
dif_img1 = cv2.subtract(image1, image2)  # 음수 → 0 클리핑 (정보 손실)

# 음수 보존이 필요한 경우: int16으로 변환 후 연산
dif_img2 = cv2.subtract(np.int16(image1), np.int16(image2))
abs_dif1 = np.absolute(dif_img2).astype('uint8')

# 가장 간단한 방법: absdiff()
abs_dif2 = cv2.absdiff(image1, image2)  # 권장
```

> 단순히 `cv2.subtract(uint8, uint8)`를 사용하면 음수가 0으로 클리핑되어 **정보가 손실**된다.
> 차분 절댓값이 필요하다면 `cv2.absdiff()`를 사용하거나, int16으로 형변환 후 처리한다.

---

### 5.4.1 원소의 최솟값과 최댓값

| 함수 | 반환값 | 설명 |
|------|--------|------|
| `cv2.min(src1, src2)` | 배열 | 원소 간 비교하여 작은 값으로 구성된 배열 |
| `cv2.max(src1, src2)` | 배열 | 원소 간 비교하여 큰 값으로 구성된 배열 |
| `cv2.minMaxLoc(src)` | `(minVal, maxVal, minLoc, maxLoc)` | 전체 최솟값/최댓값과 그 위치 반환 |

```python
# 10.mat_min_max.py
data = [10, 200, 5, 7, 9, 15, 35, 60, 80, 180, 100, 2, 55, 27, 70]
m1 = np.reshape(data, (3, 5))
m2 = np.full((3, 5), 50)

m_min = cv2.min(m1, 30)   # 각 원소와 스칼라 30 중 작은 값
m_max = cv2.max(m1, m2)   # 두 행렬의 원소 간 큰 값

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(m1)
```

> `minMaxLoc()`의 반환 좌표 `(loc)`는 `(x열, y행)` 순서이다.
> 행렬의 인덱스 순서 `[행][열]`과 반대이므로 주의한다.

#### 실전 응용 — 영상 정규화 (`11.image_min_max.py`)

```mermaid
flowchart LR
    SRC["원본 영상<br/>최솟값~최댓값 범위 좁음"]
    PROC["정규화 처리<br/>ratio = 255 / (max - min)<br/>dst = (src - min) × ratio"]
    DST["결과 영상<br/>0~255 전체 범위 활용<br/>대비(contrast) 향상"]

    SRC --> PROC --> DST

    style SRC fill:#f8d7da
    style DST fill:#d4edda
```

```python
min_val, max_val, _, _ = cv2.minMaxLoc(image)
ratio = 255 / (max_val - min_val)
dst = np.round((image - min_val) * ratio).astype('uint8')
# 결과: 원본의 최솟값 → 0, 최댓값 → 255로 선형 변환
```

---

## 5.5 통계 관련 함수

> 배열 원소들의 합·평균·표준편차·정렬 등 통계적 처리를 담당한다.

```mermaid
graph TD
    STAT["통계 함수"]
    STAT --> SUM["cv2.sumElems()<br/>채널별 원소 합 → 스칼라 튜플"]
    STAT --> MEAN["cv2.mean()<br/>채널별 평균 → 스칼라 튜플"]
    STAT --> MSTD["cv2.meanStdDev()<br/>평균+표준편차 → float64 배열"]
    STAT --> CNZ["cv2.countNonZero()<br/>0이 아닌 원소 개수"]
    STAT --> SORT["cv2.sort()<br/>행/열 단위 정렬"]
    STAT --> SIDX["cv2.sortIdx()<br/>정렬된 원소의 인덱스 반환"]
    STAT --> RED["cv2.reduce()<br/>행렬을 1행 또는 1열로 축소"]

    style STAT fill:#6c757d,color:#fff
```

### 합과 평균 (`12.sum_avg.py`)

```python
image = cv2.imread("images/sum_test.jpg", cv2.IMREAD_COLOR)

# 마스크 영역(ROI) 지정
mask = np.zeros(image.shape[:2], np.uint8)
mask[60:160, 20:120] = 255

sum_value  = cv2.sumElems(image)       # 채널별 합 → 튜플 (B합, G합, R합, 0)
mean_val1  = cv2.mean(image)           # 채널별 평균 → 튜플
mean_val2  = cv2.mean(image, mask)     # 마스크 영역만 평균

mean, stddev   = cv2.meanStdDev(image)       # 전체 평균·표준편차
mean2, stddev2 = cv2.meanStdDev(image, mask=mask)  # 마스크 영역
```

| 함수 | 반환 자료형 | 반환 구조 |
|------|------------|-----------|
| `cv2.sumElems()` | `tuple` | `(B합, G합, R합, 0)` |
| `cv2.mean()` | `tuple` | `(B평균, G평균, R평균, 0)` |
| `cv2.meanStdDev()` | `numpy.ndarray` (float64) | `(채널수×1)` 배열 |

### 정렬 (`13.sort.py`, `14.sortIdx.py`)

```mermaid
graph LR
    subgraph cv2.sort flags 조합
        ROW["SORT_EVERY_ROW<br/>행 단위 정렬"]
        COL["SORT_EVERY_COLUMN<br/>열 단위 정렬"]
        ASC["SORT_ASCENDING<br/>오름차순 (기본)"]
        DESC["SORT_DESCENDING<br/>내림차순"]
    end
    ROW --> DESC
    ROW --> ASC
    COL --> DESC
    COL --> ASC
```

```python
m = np.random.randint(0, 100, 15).reshape(3, 5)

# cv2.sort() — 정렬된 값 반환
sort1 = cv2.sort(m, cv2.SORT_EVERY_ROW)                           # 행 단위 오름차순
sort2 = cv2.sort(m, cv2.SORT_EVERY_COLUMN)                        # 열 단위 오름차순
sort3 = cv2.sort(m, cv2.SORT_EVERY_ROW + cv2.SORT_DESCENDING)    # 행 단위 내림차순

# cv2.sortIdx() — 정렬된 원소의 인덱스 반환
sort1_idx = cv2.sortIdx(m, cv2.SORT_EVERY_ROW)     # 각 행에서 원소의 원래 열 인덱스
sort2_idx = cv2.sortIdx(m, cv2.SORT_EVERY_COLUMN)  # 각 열에서 원소의 원래 행 인덱스

# NumPy 대응 함수
sort4 = np.sort(m, axis=1)             # cv2.sort + SORT_EVERY_ROW 동일
sort5 = np.sort(m, axis=0)             # cv2.sort + SORT_EVERY_COLUMN 동일
sort6 = np.sort(m, axis=1)[:, ::-1]   # 행 단위 내림차순
sort7 = np.argsort(m, axis=0)          # cv2.sortIdx + SORT_EVERY_COLUMN 동일
```

> `cv2.sortIdx()`는 값 대신 **정렬 후 원소들의 원래 인덱스**를 반환한다.
> 정렬 순서를 추적하거나 원본 데이터 위치를 참조할 때 유용하다.

### 행렬 축소 (`16.mat_reduce.py`)

> `cv2.reduce()`는 행렬을 **열 방향(dim=0) → 1행** 또는 **행 방향(dim=1) → 1열**로 축소한다.

```mermaid
graph LR
    subgraph "dim=0 (열 방향 축소 → 1행)"
        M0["3×5 행렬"]
        R0["1×5 행 벡터<br/>각 열의 합/평균/최대/최소"]
        M0 -- "↓ 열 방향 연산" --> R0
    end
    subgraph "dim=1 (행 방향 축소 → 1열)"
        M1["3×5 행렬"]
        R1["3×1 열 벡터<br/>각 행의 합/평균/최대/최소"]
        M1 -- "→ 행 방향 연산" --> R1
    end
```

| rtype 상수 | 연산 |
|-----------|------|
| `cv2.REDUCE_SUM` | 합산 |
| `cv2.REDUCE_AVG` | 평균 |
| `cv2.REDUCE_MAX` | 최댓값 |
| `cv2.REDUCE_MIN` | 최솟값 |

```python
m = np.random.rand(3, 5) * 100

reduce_sum = cv2.reduce(m, dim=0, rtype=cv2.REDUCE_SUM)  # 각 열의 합 → (1, 5) 행벡터
reduce_avg = cv2.reduce(m, dim=1, rtype=cv2.REDUCE_AVG)  # 각 행의 평균 → (3, 1) 열벡터
reduce_max = cv2.reduce(m, dim=0, rtype=cv2.REDUCE_MAX)  # 각 열의 최댓값
reduce_min = cv2.reduce(m, dim=1, rtype=cv2.REDUCE_MIN)  # 각 행의 최솟값
```

> `cv2.reduce()`는 `np.float32` 또는 `np.float64` 타입 배열에서만 사용 가능하다.

---

## 5.6 행렬 연산 함수

> OpenCV는 선형대수 계산을 위한 행렬 연산 함수를 제공한다.

```mermaid
graph TD
    MAT["행렬 연산 함수"]
    MAT --> GEMM["cv2.gemm()<br/>일반화 행렬 곱셈<br/>GEMM"]
    MAT --> PERSP["cv2.perspectiveTransform()<br/>투영 변환"]
    MAT --> INV["cv2.invert()<br/>역행렬 계산"]
    MAT --> SOLV["cv2.solve()<br/>연립방정식 풀이"]

    style MAT fill:#6c757d,color:#fff
```

### `cv2.gemm()` — 일반화 행렬 곱셈

$$dst = \alpha \cdot src1^T \cdot src2 + \beta \cdot src3^T$$

```
cv2.gemm(src1, src2, alpha, src3, beta[, dst[, flags]])
```

| 인수 | 설명 |
|------|------|
| `src1`, `src2` | 곱할 두 입력 행렬 (float32/float64, 2채널 이하) |
| `alpha` | 행렬 곱에 대한 가중치 |
| `src3` | 행렬 곱 결과에 더해지는 델타 행렬 (없으면 `None`) |
| `beta` | src3에 곱해지는 가중치 |
| `flags` | 전치 플래그 조합 |

| flags | 동작 |
|-------|------|
| `cv2.GEMM_1_T` | src1을 전치한 후 곱셈 |
| `cv2.GEMM_2_T` | src2을 전치한 후 곱셈 |
| `cv2.GEMM_3_T` | src3을 전치 |

```python
# 17.gemm.py
src1 = np.array([1, 2, 3, 1, 2, 3], np.float32).reshape(2, 3)
src2 = np.array([1, 2, 3, 4, 5, 6], np.float32).reshape(2, 3)

# src1^T × src2  (src1을 전치)
dst1 = cv2.gemm(src1, src2, 1.0, None, 1.0, flags=cv2.GEMM_1_T)

# src1 × src2^T  (src2를 전치)
dst2 = cv2.gemm(src1, src2, 1.0, None, 1.0, flags=cv2.GEMM_2_T)
```

### 실전 응용 — 좌표 회전 변환 (`18.point_transform.py`)

> 회전 변환 행렬과 `cv2.gemm()`을 조합하면 좌표를 임의 각도로 회전시킬 수 있다.

```mermaid
flowchart LR
    ANGLE["회전 각도 θ (도)"]
    RMAT["회전 변환 행렬<br/>[[cosθ, -sinθ],<br/> [sinθ,  cosθ]]"]
    PTS1["원본 좌표 배열<br/>(N×2 float32)"]
    PTS2["변환된 좌표 배열<br/>gemm(pts1, rot_mat, GEMM_2_T)"]

    ANGLE --> RMAT
    PTS1 --> PTS2
    RMAT --> PTS2

    style PTS2 fill:#d4edda
```

```python
theta = 20 * np.pi / 180  # 20도 → 라디안
rot_mat = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta),  np.cos(theta)]], np.float32)

pts1 = np.array([(250, 30), (400, 70), (350, 250), (150, 200)], np.float32)
pts2 = cv2.gemm(pts1, rot_mat, 1, None, 1, flags=cv2.GEMM_2_T)  # 회전 적용

# 결과 시각화
cv2.polylines(image, [np.int32(pts1)], True, (0, 255, 0), 2)  # 원본: 초록
cv2.polylines(image, [np.int32(pts2)], True, (255, 0, 0), 3)  # 회전: 파랑
```

### `cv2.invert()` — 역행렬 계산

```
cv2.invert(src[, dst[, flags]])  → (retval, dst)
```

| flags | 역행렬 계산 방법 | 입력 행렬 조건 |
|-------|----------------|---------------|
| `cv2.DECOMP_LU` | 가우시안 소거법 | 역행렬이 존재하는 정방행렬 |
| `cv2.DECOMP_SVD` | 특이치 분해(SVD) | 정방행렬이 아닌 경우 → 의사 역행렬 |
| `cv2.DECOMP_CHOLESKY` | 촐레스키 분해 | 대칭 + 양의 정부호 정방행렬 |

### `cv2.solve()` — 연립방정식 풀이

$$Ax = b \quad \Rightarrow \quad x = A^{-1}b$$

```python
# 19.equation.py  —  연립방정식 Ax = b 풀기
data = [3, 0, 6, -3, 4, 2, -5, -1, 9]
m1 = np.array(data, np.float32).reshape(3, 3)   # 계수 행렬 A
m2 = np.array([36, 10, 28], np.float32)          # 상수 벡터 b

# 방법 1: 역행렬로 직접 계산
ret, inv = cv2.invert(m1, cv2.DECOMP_LU)
if ret:
    dst1 = inv.dot(m2)                        # NumPy 행렬곱
    dst2 = cv2.gemm(inv, m2, 1, None, 1)     # OpenCV 행렬곱

# 방법 2: cv2.solve() 직접 사용 (권장)
_, dst3 = cv2.solve(m1, m2, cv2.DECOMP_LU)
```

```mermaid
flowchart LR
    EQ["연립방정식<br/>Ax = b"]
    INV["역행렬 방법<br/>A⁻¹ 계산 후 x = A⁻¹b"]
    SOL["cv2.solve()<br/>내부적으로 효율적 계산"]

    EQ --> INV
    EQ --> SOL

    style SOL fill:#d4edda
    style INV fill:#fff3cd
```

> `cv2.solve()`는 역행렬을 명시적으로 구하지 않고 방정식을 직접 풀기 때문에
> 수치 안정성이 더 좋고 일반적으로 더 빠르다.

---

## 핵심 함수 정리

```mermaid
mindmap
  root((Chap5 핵심 정리))
    배열 변형
      flip 0상하 1좌우 -1양축
      repeat ny nx
      transpose 행열 교환
    채널
      split 다채널→단일채널
      merge 단일채널→다채널
    산술
      add subtract 포화연산
      multiply divide scale 인수
      addWeighted 블렌딩
      uint8 나눗셈은 float32 변환 필수
    지수로그
      exp log sqrt pow
      입력은 ndarray float32
      ravel flatten transpose 출력 변환
    비트연산
      and 교집합 마스킹
      or 합집합
      xor 차집합
      not 반전
    절댓값
      absdiff 차분 절댓값 권장
      subtract uint8는 음수 손실 주의
      minMaxLoc 최솟값 최댓값 위치
    통계
      sumElems mean 튜플 반환
      meanStdDev float64 배열 반환
      sort sortIdx 행열 방향 정렬
      reduce dim0열방향 dim1행방향
    행렬
      gemm 일반화 행렬곱
      GEMM_1_T GEMM_2_T 전치 플래그
      invert DECOMP_LU SVD CHOLESKY
      solve 연립방정식 직접 풀이
```

---

## 중요 포인트 요약

| 주제 | 핵심 주의사항 |
|------|--------------|
| **포화 연산** | `cv2.add(uint8)`: 결과 > 255 → 255 클리핑, 결과 < 0 → 0 클리핑 |
| **나눗셈 정밀도** | `uint8`나눗셈은 소수 버림 → 정밀도 필요 시 `float32` 변환 필수 |
| **차분 절댓값** | `cv2.subtract(uint8)`는 음수를 0으로 버림 → `cv2.absdiff()` 사용 권장 |
| **수학 함수 입력** | `cv2.exp()` 등은 Python 리스트 불가 → 반드시 `np.ndarray` 전달 |
| **minMaxLoc 좌표** | 반환값이 `(x열, y행)` 순서 → 행렬 인덱스 `[행][열]`과 반대 |
| **reduce 자료형** | `cv2.reduce()`는 `float32` / `float64` 배열만 처리 가능 |
| **gemm 자료형** | `cv2.gemm()`은 `float32` / `float64` 배열, 최대 2채널까지 가능 |
| **split 반환값** | `cv2.split()` 반환 타입은 `tuple` (리스트 아님) |
