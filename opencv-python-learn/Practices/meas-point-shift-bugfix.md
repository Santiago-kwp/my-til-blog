# 측점 우측 시프트 버그 수정 보고서

**날짜**: 2026-04-29  
**버전**: v1.1.x  
**수정 파일**: `app/src/main/python/RiverSivAngle.py`  
**수정 내용**: `makeCrsFile()` 내 `getStartPoint(n, ...)` → `getStartPoint(n + 2, ...)`

---

## 1. 현상

태블릿 현장 실험에서 다음 미스매치가 발생했다.

```
[녹화 전 프리뷰 측점]
------x-x-x-x-x-x-x-x-x-x------   (중앙 대칭)

[녹화 후 *_VEL.jpg 결과 측점]
----------x-x-x-x-x-x-x-x-x-x--   (우측 치우침)
```

- 프리뷰의 `AnglePointView` 오버레이에는 측점이 화면 중앙에 대칭으로 표시됨
- 분석 결과 이미지(`*_VEL.jpg`)에는 동일 측점이 우측으로 편향되어 그려짐
- 편향 크기는 카메라 세팅(높이·경사각)에 따라 달라짐

---

## 2. 코드 흐름 요약

### 프리뷰 경로 (녹화 전)

```
CameraFragment.updatePointsAndParameters()
  └─ AnalysisPython.getPoints(cam, gid)
       └─ RiverStiv.makePts(yws, theta, mu, md, nz, dx, dz)   ← XYZ 직접 생성
       └─ RiverStiv.getGridPoints(ptXYZ)
            └─ Camera2Image.convXYZ2CR()  → (col, row)
  └─ AnglePointView.setPointList(pts)   ← 화면에 점 표시
```

### 분석 경로 (녹화 후)

```
AnalysisPython.videoAnalysis()
  └─ RiverStiv.calcVel(videoPath, ...)
       └─ StivAngle.calcVel()
            └─ StivAngle.setCameraCoord(Hws=0)
                 └─ CrossSection.getMeasPts()          ← 횡단면 JSON에서 NEH 읽기
                 └─ Global2Device.convNEH2XYZ()        ← NEH → XYZ 변환
                 └─ Camera2Image.convXYZ2CRD2()        → (col, row, dir)
            └─ drawVectors(firstFrame, ...)   ← VEL.jpg에 점 표시
```

두 경로 모두 최종적으로 `Camera2Image.convXYZ2CR()`를 거쳐 동일한 카메라 모델을 사용한다.  
그러나 **입력 XYZ 좌표의 중심 위치가 서로 달랐다.**

---

## 3. 근본 원인

### 3-1. 횡단면 구조

`makeCrsFile(h, theta, gid, n=20)` 에서 생성하는 횡단면 DataFrame:

```python
crs = pandas.DataFrame([
    [baseM,  n+1,  0.1],   # (N, E, H) 좌안 제방  E = 21
    [baseM,  n,   -1  ],   # 좌측 물 가장자리     E = 20
    [baseM,  0,   -1  ],   # 우측 물 가장자리     E =  0
    [baseM, -1,   0.1 ],   # 우안 제방            E = -1
])
```

| 구간          | E 범위        | 너비           |
| ------------- | ------------- | -------------- |
| 수면(하천 폭) | 0 ~ n = 20    | **n = 20 m**   |
| 횡단면 전체   | -1 ~ n+1 = 21 | **n+2 = 22 m** |

`CrossSection.__correctCrossPts()`는 첫 번째 행(E=21)을 S=0으로 잡고 거리를 계산한다.  
따라서 S좌표계에서 각 위치는 다음과 같다.

```
S=0   ← E=21  (좌안 제방, 기점)
S=1   ← E=20  (물 가장자리)
S=11  ← E=10  ← 카메라 위치 (E = n/2 = 10)
S=21  ← E=0   (물 가장자리)
S=22  ← E=-1  (우안 제방, 종점)
```

### 3-2. 버그: 잘못된 측점 시작 위치 계산

```python
# 버그 코드 (수정 전)
stPoint = self.getStartPoint(n, *gid[2:4])   # n = 20
```

`getStartPoint(n, nz, dx)`의 동작:

```python
def getStartPoint(self, n: float, nz: int, dx: float):
    occLen = (nz - 1) * dx
    return (n/2) - (occLen/2)   # "n이 횡단면 총 너비"라고 가정
```

`n=20`을 전달했을 때의 결과 (nz=11, dx=1 기준):

```
stPoint = 20/2 - 10/2 = 10 - 5 = 5
측점 S값: 5, 6, 7, ..., 15
측점 E값: 16, 15, 14, ..., 6    ← E중심 = 11
카메라 E: 10                    ← 1 m 불일치!
```

### 3-3. 프리뷰는 왜 맞아 보였나

`makePts()`는 횡단면 없이 XYZ를 직접 생성한다.

```python
Xij = 0 - ((nz-1)/2 - j) * dx   # X = 0 중심 = E=10 (카메라 위치)
```

프리뷰 측점 X중심 = 0 → col = cx = 960 (이미지 중앙)  
분석 측점 X중심 = +1 → col = cx + fx/baseM > 960 (우측 시프트)

### 3-4. 시프트 크기

물리 좌표계에서의 E 오프셋은 nz·dx에 무관하게 **항상 +1 m(동쪽)** 고정.

영상 내 픽셀 오프셋:

```
Δcol = fx × 1m / baseM
     = 1920 / (h / tan(θ))
```

| 카메라 높이 h | 경사각 θ | baseM  | Δcol (픽셀) |
| ------------- | -------- | ------ | ----------- |
| 2 m           | 30°      | 3.46 m | ~555 px     |
| 2 m           | 20°      | 5.49 m | ~350 px     |
| 3 m           | 30°      | 5.20 m | ~369 px     |
| 3 m           | 20°      | 8.24 m | ~233 px     |

현장 조건에 따라 수백 픽셀 단위의 우측 편향이 발생할 수 있다.

---

## 4. 수정 내용

**파일**: `app/src/main/python/RiverSivAngle.py`, line 47

```python
# 수정 전
stPoint = self.getStartPoint(n, *gid[2:4])

# 수정 후
stPoint = self.getStartPoint(n + 2, *gid[2:4])
```

`n+2`는 횡단면의 실제 총 너비(제방 포함)이므로,  
`getStartPoint`가 올바르게 **S=n/2+1** 을 중심으로 측점을 배치한다.

```
수정 후 (nz=11, dx=1 기준):
stPoint = (20+2)/2 - 5 = 11 - 5 = 6
측점 S값: 6, 7, 8, ..., 16
측점 E값: 15, 14, 13, ..., 5    ← E중심 = 10 ✓
카메라 E: 10                    ← 일치!
```

`makePts()`와 횡단면 분석이 동일한 물리 좌표를 사용하게 된다.

---

## 5. 검증

- 수정 후 앱 빌드 및 태블릿 재설치 완료
- 현장 실험 재실시 결과, 프리뷰 측점 위치와 VEL.jpg 측점 위치 일치 확인
- nz·dx 기본값(11개, 1m 간격) 기준으로 우측 편향 해소됨

---

## 6. 영향 범위

| 항목                         | 영향 여부    | 비고                                              |
| ---------------------------- | ------------ | ------------------------------------------------- |
| 측점 위치 (VEL.jpg)          | ✅ 수정됨    | 기존 결과 대비 좌측으로 이동                      |
| 유속 추정값                  | ✅ 향상 기대 | 실제 수면 위치에서 STI 추출                       |
| PC 분석 (`run_core_test.py`) | ⚠️ 무관      | PC는 별도 `*_crs.json` 사용                       |
| 측점 번호 순서               | ❌ 변경 없음 | 번호 배열 로직 미수정                             |
| 기존 저장된 `TBL_crs.json`   | ⚠️ 갱신 필요 | 앱 재실행 시 `setParameters()` 호출로 자동 재생성 |

---

## 7. 재발 방지 노트

`makeCrsFile`의 횡단면 DataFrame과 `getStartPoint`의 인자가 항상 **동일한 기준(제방 포함 전체 너비)**을 사용해야 한다.

현재 횡단면 구조:

- 좌안: E = `n+1`, 우안: E = `-1` → 총 너비 = `n+2`
- `getStartPoint`에 전달하는 인자도 `n+2`

만약 향후 `makeCrsFile`의 제방 여유폭(현재 1m)을 변경하면  
`getStartPoint`의 인자도 함께 조정해야 한다.
