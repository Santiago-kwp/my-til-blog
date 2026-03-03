# Plan: 3D Horizontal Axis Image Rotation

## Feature Overview
이미지의 높이 중앙의 가로축(수평축)을 회전축으로 하여 3D 원근 효과가 적용된 회전 이미지를 생성한다.
`image_3d_rotation.png` 다이어그램 기준: 하단이 넓어지고 상단이 좁아지는 사다리꼴 형태.

## Goals
- OpenCV Python으로 3D 원근 투영(Perspective Projection)을 활용한 수평축 회전 구현
- Jupyter Notebook으로 시각적 테스트 제공
- 검증 테스트 코드 작성

## Requirements

### FR-01: 3D Rotation Function
- 입력: 이미지, 회전각(degree), 초점거리(f, 원근 강도)
- 출력: 원근 투영이 적용된 변환 이미지
- 회전축: 이미지 높이 중앙의 가로축 (y = H/2)
- 수식:
  - dy = y - H/2
  - z_world = dy * sin(θ)
  - scale(y) = f / (f - z_world) = f / (f - dy * sin(θ))
  - proj_x = W/2 + (x - W/2) * scale
  - proj_y = H/2 + dy * cos(θ) * scale
- 4 꼭짓점 매핑 → `cv2.getPerspectiveTransform` + `cv2.warpPerspective`

### FR-02: Jupyter Notebook
- `Practice/3d_rotation_notebook.ipynb`
- 샘플 이미지(`Practice/images/test.jpg`) 사용
- 여러 각도(0°, 15°, 30°, 45°) 시각화

### FR-03: 검증 테스트
- θ=0° 시 원본과 동일한 결과 확인
- 상단 너비 < 원본 너비 < 하단 너비 확인 (θ > 0°)
- 회전축(y=H/2) 픽셀의 x 좌표 불변 확인

## Out of Scope
- 세로축(수직축) 회전
- 실시간 영상 처리

## Tech Stack
- Python, OpenCV (cv2), NumPy, Matplotlib
- Jupyter Notebook

## Acceptance Criteria
- [ ] 변환 후 이미지가 사다리꼴 형태로 출력됨
- [ ] θ=0° 시 원본과 동일
- [ ] 테스트 3개 이상 통과
