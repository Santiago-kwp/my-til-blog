# 05. 기본 배열 연산(Operations on Arrays) 함수

## 5.1 기본 배열(Array) 처리 함수

> 영상처리 프로그래밍을 하다보면, 카메라에서 사용자의 얼굴을 검출해서 윈도우에 표시해야 한다. 이때, 보통 카메라가 사용자를 향하므로 윈도우에 표시되는 얼굴의 영상은 사용자의 실제 모습과 달리 좌우가 뒤바뀐 영상이 나타난다. 이런 경우 입력영상의 행렬 원소를 좌우로 뒤집도록 해서 문제를 간단히 해결할 수 있다.

`cv2.flip(src, flipCode[, dst])`

- 설명: 입력된 2차원 배열을 수직, 수평, 양축으로 뒤집는다.
  `cv2.repeat(src, ny, nx[, dst])`
- 설명: 입력 배열의 반복된 복사본으로 출력 배열을 채운다.
  `cv2.transpose(src[, dst])`
- 설명: 입력 행렬의 전치 행렬을 출력으로 반환한다.

<details>
<summary> `[, dst]` 의미 </summary>

예시

```python
import cv2
import numpy as np

img = np.ones((100,100), np.uint8)*255

# dst를 생략하면 새로운 배열 반환
flipped = cv2.flip(img, 1)

# dst를 지정하면 결과가 그 배열에 저장됨
dst = np.empty_like(img)
cv2.flip(img, 1, dst)
print(np.array_equal(flipped, dst))  # True

```

정리
[dst] → 선택적으로 줄 수 있는 인자

생략하면 OpenCV가 알아서 새 배열을 만들어 반환

지정하면 결과가 그 배열에 저장되어 메모리 재사용 가능
👉 즉, 책에서 [dst]라고 쓴 건 “이 인자는 있어도 되고 없어도 된다”는 뜻

</details>

## 5.2 채널 처리 함수

`cv2.merge(mv[, dst])`

- 설명: 여러 개의 단일채널 배열을 다채널 배열로 합성한다. - `mv`: 합성될 입력 배열 혹은 벡터, 합성될 단일채널 배열들의 크기와 깊이가 동일해야 함 - `dst`: 입력 배열과 같은 크기와 같은 깊이의 출력 배열
  `cv2.split(m[, mv])`
- 설명: 다채널 배열을 여러 개의 단일채널 배열로 분리한다.
  - `m`: 입력되는 다채널 배열
  - `mv`: 분리되어 반환되는 단일채널 배열들의 벡터

## 5.3 산술 연산 함수

### 5.3.1 사칙 연산

`cv2.add(src1, src2[, dst[, mask[, dtype]]])`
`cv2.subtract(src1, src2[, dst[, mask[, dtype]]])`

> 두 개의 배열 혹은 배열과 스칼라의 각 원소 간 합, 차분을 계산한다.

- src1 : 첫 번째 입력 배열 혹은 스칼라
- src2 : 두 번째 입력 배열 혹은 스칼라
- dst : 계산된 결과의 출력 배열
- mask : 연산 마스크: 0이 아닌 마스크 원소의 위치만 연산 수행(8비트 단일 채널)
- dtype: 출력 배열의 깊이

`cv2.multiply(src1, src2[, dst[, scale[, dtype]]])`

> 두 배열의 각 원소 간 곱을 계산한다.

- scale: 두 배열의 원소 간 곱할 때 추가로 곱해주는 배율

`cv2.divide(src1, src2[, dst[, scale[, dtype]]])`

> 두 배열의 각 원소 간 나눗셈을 계산한다.

`cv2.divide(scale, src2[, dst[, dtype]])`

> 스칼라값과 행렬원소간 나눗셈을 수행한다.

`cv2.addWeighted(src1, alpha, src2, beta, gamma[, dst[, dtype]])`

> 두 배열의 각 원소에 가중치를 곱한 후에 각 원소 간 합 즉, 가중된(weighted) 합을 계산한다.

- alpha : 첫 번째 배열의 모든 원소에 대한 가중치
- beta : 두 번째 배열의 모든 원소에 대한 가중치
- gamma : 두 배열의 원소 간 합에 추가로 더해주는 스칼라

### 5.3.2 지수, 로그, 제곱근 관련 함수

`cv2.exp(src[, dst])`

> 모든 배열 원소의 지수(exponent)를 계산한다.

`cv2.log(src[, dst])`

> 모든 배열 원소의 절대값에 대한 자연 로그를 계산한다.

`cv2.sqrt(src[, dst])`

> 모든 배열 원소에 대해 제곱근을 계산한다.

`cv2.pow(src, power[, dst])`

> 모든 배열 원소에 대해서 제곱 승수를 계산한다.

`cv2.magnitude(x, y[, magnitude])`

> 2차원 배열들의 크기(magnitude)를 계산한다.
> $$magnitude(i) = \sqrt{x(i)^2 + y(i)^2}$$

- x,y : x, y 좌표들의 입력 배열
- magnitude: 입력 배열과 같은 크기의 출력 배열

`cv2.phase(x, y[, angle[, anglenDegrees]])`

> 2차원 배열의 회전 각도를 계산한다.
> 수식 : $$angle(i) = atan2(y(i), x(i)) \cdot [180/\pi]$$

- angle: 각도들의 출력 배열
- anglenDegrees: True -> 각을 도(degree)로 측정, False -> 각을 라디안으로 측정

`cv2.cartToPolar(x, y[, magnitude[, angle[, anglenDegrees]]])`

> 2차원 배열들의 크기와 각도를 계산한다.

`cv2.polarToCart(magnitude, angle[, x[, y[, anglenDegrees]]])`

> 각도와 크기로부터 2차원 배열들의 좌표를 계산한다.

### 5.3.3 논리(비트) 연산 함수

`cv2.bitwise_and(src1, src2[, dst[, mask]])`

> 두 배열의 원소 간 혹은 배열 원소와 스칼라 간의 비트별(bit-wise) 논리곱(AND) 연산을 수행한다. 인수 src1, src2 중 하나는 스칼라값일 수 있다.

`cv2.bitwise_or(src1, src2[, dst[, mask]])`

> 두 배열의 원소 간 혹은 배열 원소와 스칼라 간의 비트별(bit-wise) 논리합(OR) 연산을 수행한다. 인수 src1, src2 중 하나는 스칼라값일 수 있다.

`cv2.bitwise_xor(src1, src2[, dst[, mask]])`

> 두 배열의 원소 간 혹은 배열 원소와 스칼라 간의 비트별(bit-wise) 배타적 논리합(XOR) 연산을 수행한다. 인수 src1, src2 중 하나는 스칼라값일 수 있다.

`cv2.bitwise_not(src[, dst[, mask]])`

> 입력 배열의 모든 원소마다 비트 보수 연산을 한다.

## 5.4 원소의 절댓값 연산

> 보통 동영상 프레임을 처리하는 과정에서 행렬의 차분 연산을 종종 하게 된다. 이때 행렬의 원소값이 음수를 허용하지 않을 경우도 있다. 이런 경우 `cv2.abs()` 함수를 적용한다면 쉽게 다음 영상처리 과정으로 넘어갈 수 있다.

`cv2.absdiff(src1, src2[, dst])`

> 두 배열간 각 원소간(per-element) 차분 절댓값을 계산한다. src1, src2 중 하나는 스칼라값이 될 수 있다.

`cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])`

> 입력 배열의 각 원소에 alpha만큼 배율을 곱하고 beta 만큼 더한 후에 절대값을 계산한 결과를 8비트 자료형으로 변환한다.

- alpha: 입력 배열의 각 원소에 곱해지는 스케일 팩터(scale factor)
- beta: 스케일된 값에 더해지는 델타 옵션

### 5.4.1 원소의 최솟값과 최댓값

`cv2.min(src1, src2[, dst])`

> 두 입력 배열의 원소 간 비교하여 작은 값을 출력 배열로 반환한다.

`cv2.max(src1, src2[, dst])`

> 두 입력 배열의 원소 간 비교하여 큰 값을 배열로 반환한다.

`cv2.minMaxLoc(src, [, mask])` $\rarr$ `minVal, maxVal, minLoc, maxLoc`

> 입력 배열에서 최솟값과 최댓값, 최솟값과 최댓값을 갖는 원소 위치를 반환한다.

- minVal, maxVal : 최솟값, 최댓값
- minLoc, maxLoc : 최솟값, 최댓값을 갖는 원소 위치(정수형 튜플)

## 5.5 통계 관련 함수

> OpenCV는 행렬 원소들의 합, 평균, 표준편차와 같은 통계적인 요소를 계산하는 함수를 제공한다. 또한, 행렬 원소들의 오름차순 혹은 내림차순으로 정렬하는 함수도 있다.
