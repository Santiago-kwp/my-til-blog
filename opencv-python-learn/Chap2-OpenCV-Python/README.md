[← OpenCV-Python 학습 목차로 돌아가기](../README.md)

# 2. OpenCV-Python 환경 설정 및 기초

## 목차

- [2.1 OpenCV란?](#21-opencv란)
- [2.2 환경 설치](#22-환경-설치)
- [2.3 OpenCV 기본 구조](#23-opencv-기본-구조)
- [2.4 기본 사용법](#24-기본-사용법)
- [2.5 NumPy와 OpenCV](#25-numpy와-opencv)

---

## 2.1 OpenCV란?

> **Open Source Computer Vision Library**
> Intel이 개발하고 오픈소스로 공개된 컴퓨터 비전 및 영상처리 라이브러리

```mermaid
graph LR
    A["OpenCV"] --> B["영상 처리\n(Image Processing)"]
    A --> C["컴퓨터 비전\n(Computer Vision)"]
    A --> D["머신 러닝\n(Machine Learning)"]
    A --> E["딥 러닝\n(Deep Learning)"]

    style A fill:#4a90d9,color:#fff
```

| 항목 | 내용 |
|------|------|
| 최초 배포 | 2000년 (Intel) |
| 언어 지원 | C++, Python, Java, MATLAB |
| 주요 모듈 | core, imgproc, highgui, video, ml, dnn |
| 라이선스 | Apache 2.0 (상업적 이용 가능) |

### OpenCV의 역사
> OpenCV의 주요 개발자는 인텔 퍼포먼스 라이브러리 팀과 인텔의 러시아 라이브러리 팀이다. OpenCV의 초창기 목표는 컴퓨터 비전 기술의 기초 인프라 확립을 위해 무료로 최적화된 코드를 제공함으로써 컴퓨터 비전 분야를 발전시키는 것. OpenCV는 1999년도에 공식적으로 개발이 시작됐고, 첫 알파 버전은 IEEE 컨퍼런스인 CVPR에서 공개됐다. 이후 5개의 베타 버전이 공개된 후 공식적인 1.0 버전이 2006년에 처음 배포됐다. 

> 윌로우 개러지(Willow Garage)의 도움을 받아 2009년부터 배포된 OpenCV 2.X 버전은 iOS 및 안드로이드를 포함한 새로운 플랫폼에 대한 지원과 CUDA 및 OpenCL을 통해 GPU 가속 기능이 추가됐다. 파이썬 및 자바 사용자에게 완벽에 가까운 인터페이스를 제공하고 깃허브 저장소를 통한 배포가 가능해졌다. 

> 2015년부터 OpenCV 3.x 버전이 배포됐으며, 프로젝트 구조 변경과 프로젝트 기여자들을 통해 최첨단 알고리즘이 적용됐다. 또한 인텔과 AMD의 지원으로 컴퓨터 비전 알고리즘의 GPU 가속화와 인텔 IPP(Intel Integrated Performance Primitives) 라이브러리를 저작관료를 지불하지 않고도 사용할 수 있게 됐다. 인텔 IPP가 적용되면서 OpenCV의 함수들이 최소 1.2배에서 최대 8배 이상 속도가 향상됐다. 

> OpenCV는 다수의 기업, 개발자, 기여자의 전폭적인 지원과 개발 덕분에 현재 4.0 버전이 릴리스 됐다. OpenCV 4.x에서는 코어 모듈의 지속성이 늘어나고 (지속성 : 프로그램을 오랜 시간 구동해도 프로그램이 비정상적으로 종료되지 않는다는 것을 의미), 메모리 소비량이 감소했으며, 더는 사용되지 않는 OpenCV 1.x의 여러 C API가 제거됐다. 또한 효율적인 그래프 기반의 이미지 파이프라인 엔진인 G-API, Deep Learning Development Toolkit 등을 포함해서 배포됐다. 
---

## 2.2 환경 설치

### 설치 방법

```bash
# 가상환경 생성 (권장)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# OpenCV 설치
pip install opencv-python       # 기본 패키지 (highgui 포함)
pip install opencv-python-headless  # 서버 환경 (GUI 없음)

# 필수 의존 패키지
pip install numpy
```

### 설치 확인

```python
import cv2
import numpy as np

print(f"OpenCV 버전: {cv2.__version__}")
print(f"NumPy 버전: {np.__version__}")
```

---

## 2.3 OpenCV 기본 구조

```mermaid
graph TD
    OCV["OpenCV (cv2)"]
    OCV --> CORE["core\n핵심 자료구조 및 기본 연산"]
    OCV --> IMGPROC["imgproc\n영상 처리 (필터, 변환 등)"]
    OCV --> HIGHGUI["highgui\n윈도우, 이벤트, I/O"]
    OCV --> VIDEO["video\n영상/영화 처리"]
    OCV --> ML["ml\n머신러닝 알고리즘"]
    OCV --> DNN["dnn\n딥러닝 추론"]

    HIGHGUI --> H1["imshow() - 영상 출력"]
    HIGHGUI --> H2["imread() - 영상 읽기"]
    HIGHGUI --> H3["imwrite() - 영상 저장"]
    HIGHGUI --> H4["waitKey() - 키 입력 대기"]
```

### OpenCV 좌표 시스템

```
(0,0) ──────────────→ x축 (열, col)
  │  ┌─────────────────┐
  │  │                 │
  │  │   영상(Image)   │
  │  │                 │
  ↓  └─────────────────┘
 y축
(행, row)
```

> OpenCV에서 좌표는 **(x, y) = (열, 행)** 순서이지만,
> NumPy 배열은 **(row, col) = (행, 열)** 순서임에 주의!

---

## 2.4 기본 사용법

### 영상 읽기 / 출력 / 저장

```python
import cv2

# 영상 읽기
img = cv2.imread('image.jpg')           # 컬러 (BGR)
img_gray = cv2.imread('image.jpg', 0)   # 그레이스케일
img_alpha = cv2.imread('image.png', -1) # 알파 채널 포함

# 영상 출력 (윈도우)
cv2.imshow('Window Title', img)
cv2.waitKey(0)          # 0: 키 입력 무한 대기, n: n ms 대기
cv2.destroyAllWindows() # 모든 윈도우 닫기

# 영상 저장
cv2.imwrite('output.jpg', img)
```

### `imread()` 플래그

| 플래그 | 값 | 설명 |
|--------|----|------|
| `cv2.IMREAD_COLOR` | 1 (기본값) | 컬러 BGR로 읽기 |
| `cv2.IMREAD_GRAYSCALE` | 0 | 그레이스케일로 읽기 |
| `cv2.IMREAD_UNCHANGED` | -1 | 원본 그대로 (알파 포함) |

### OpenCV 기본 영상 프로그램 패턴

```mermaid
flowchart TD
    A["프로그램 시작"] --> B["cv2.imread() / np.zeros()\n영상 생성 또는 읽기"]
    B --> C["영상 처리\n알고리즘 적용"]
    C --> D["cv2.imshow()\n영상 출력"]
    D --> E["cv2.waitKey()\n키 입력 대기"]
    E --> F{종료 키?}
    F -- "Yes (예: 'q' 또는 ESC)" --> G["cv2.destroyAllWindows()\n종료"]
    F -- "No" --> C
```

### Hello OpenCV (02.opencvtest.py 기반)

```python
import numpy as np
import cv2

# 검은 배경 영상 생성 (300행 × 400열, uint8 타입)
image = np.zeros((300, 400), np.uint8)
image.fill(200)  # 밝기값 200으로 채우기 (밝은 회색)

cv2.imshow("Window title", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 2.5 NumPy와 OpenCV

> OpenCV의 영상 데이터는 내부적으로 **NumPy ndarray**로 표현된다.

### 영상과 NumPy 배열의 관계

```mermaid
graph LR
    IMG["영상 (Image)"] -- "cv2.imread()" --> ARR["NumPy ndarray"]
    ARR -- "cv2.imshow()" --> IMG

    ARR --> SHAPE["shape: (행, 열, 채널)"]
    ARR --> DTYPE["dtype: uint8 (0~255)"]
```

### 주요 속성 확인

```python
import cv2

img = cv2.imread('image.jpg')

print(img.shape)   # (height, width, channels) → 예: (480, 640, 3)
print(img.dtype)   # uint8
print(img.size)    # 전체 원소 수 = height × width × channels
```

### 그레이스케일 vs 컬러

| 구분 | shape | dtype | 채널 |
|------|-------|-------|------|
| 그레이스케일 | `(H, W)` | uint8 | 1 (밝기) |
| 컬러 (BGR) | `(H, W, 3)` | uint8 | 3 (Blue, Green, Red) |
| 알파 포함 | `(H, W, 4)` | uint8 | 4 (BGR + Alpha) |

> OpenCV는 RGB가 아닌 **BGR** 순서로 채널을 저장한다!

### 자주 사용하는 NumPy 영상 생성

```python
import numpy as np

# 검은 영상 (300 × 400, 그레이스케일)
black = np.zeros((300, 400), np.uint8)

# 흰 영상 (300 × 400, 컬러)
white = np.ones((300, 400, 3), np.uint8) * 255

# 특정 밝기값으로 채운 영상
gray = np.full((300, 400), 128, np.uint8)
```

---

## 핵심 함수 정리

| 함수 | 용도 | 주요 인수 |
|------|------|-----------|
| `cv2.imread(path, flag)` | 영상 파일 읽기 | path, flag (0/1/-1) |
| `cv2.imshow(winname, img)` | 윈도우에 영상 출력 | 윈도우 이름, ndarray |
| `cv2.imwrite(path, img)` | 영상 파일 저장 | 저장 경로, ndarray |
| `cv2.waitKey(delay)` | 키 입력 대기 | delay(ms), 0=무한 |
| `cv2.destroyAllWindows()` | 모든 윈도우 닫기 | — |
