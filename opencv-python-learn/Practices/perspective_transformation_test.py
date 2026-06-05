"""
사영 변환 (Projective Transformation) - OpenCV Python 구현
원본: Java 코드 (https://kszkaivdm.doorblog.jp/archives/33580591.html)

[조작 방법]
  Enter     : 초기화
  ← → 키   : Y축 회전
  ↑ ↓ 키   : X축 회전
  s / x     : Z축 회전
  z / a     : 확대 / 축소
  g / h     : 오른쪽 / 왼쪽 평행이동
  r / v     : 위 / 아래 평행이동
  q / ESC   : 종료
"""

import cv2
import numpy as np
import sys
import os


# ── 설정값 ────────────────────────────────────────────────────────────────────
IMAGE_PATH  = "images/ortho_frame0.jpg"   # ← 변환할 이미지 경로로 수정하세요
FOCUS       = 1480           # 초점거리 (pixel) — 원본과 동일
WINDOW_NAME = "Projective Transform"

# 회전 각도 변화량 (degree)
ANGLE_STEP  = 1
# 평행이동 / 줌 변화량 (pixel)
TRANS_STEP  = 10
ZOOM_STEP   = 10


# ── 회전 행렬 ─────────────────────────────────────────────────────────────────
def rotation_matrix(ax: float, ay: float, az: float) -> np.ndarray:
    """
    X → Y → Z 순서로 회전 행렬을 합성합니다.
    원본 Java: R = Rz @ Ry @ Rx  (왼쪽 곱 순서 동일하게 재현)
    """
    ax_r, ay_r, az_r = np.radians(ax), np.radians(ay), np.radians(az)

    Rx = np.array([
        [1,            0,             0],
        [0,  np.cos(ax_r), -np.sin(ax_r)],
        [0,  np.sin(ax_r),  np.cos(ax_r)],
    ], dtype=np.float64)

    Ry = np.array([
        [ np.cos(ay_r), 0, np.sin(ay_r)],
        [0,             1,            0],
        [-np.sin(ay_r), 0, np.cos(ay_r)],
    ], dtype=np.float64)

    Rz = np.array([
        [np.cos(az_r), -np.sin(az_r), 0],
        [np.sin(az_r),  np.cos(az_r), 0],
        [0,             0,            1],
    ], dtype=np.float64)

    return Rz @ Ry @ Rx   # 원본과 동일한 합성 순서


# ── 사영 변환 렌더링 ──────────────────────────────────────────────────────────
def render(src: np.ndarray,
           xangle: float, yangle: float, zangle: float,
           tx: float, ty: float, tz: float,
           focus: int = FOCUS) -> np.ndarray:
    """
    Backward mapping 방식으로 사영 변환을 수행합니다.

    Java 원본은 Forward mapping(src→dst)이라 홀이 생기는 문제가 있었습니다.
    여기서는 Backward mapping(dst→src)을 사용해 완전한 화질을 얻습니다.

    수식 (원본과 동일한 원근 투영):
        R = rotation_matrix(xangle, yangle, zangle)
        [u, v, w]^T = R @ [x-hw, y-hh, z]^T
        dst_x = focus * (u + tx) / (w + tz) + hw
        dst_y = focus * (v + ty) / (w + tz) + hh

    Backward mapping 이므로 dst 좌표 → src 좌표를 역산합니다.
    """
    h, w = src.shape[:2]
    hw, hh = w // 2, h // 2
    z_offset = 100          # 원본 고정값

    R = rotation_matrix(xangle, yangle, zangle)
    R_inv = np.linalg.inv(R)

    # dst 출력 크기: 원본과 동일 (필요 시 변경 가능)
    out_h, out_w = h, w
    dst = np.zeros((out_h, out_w, 3), dtype=np.uint8)

    # dst 픽셀 좌표 격자 생성
    dx = np.arange(out_w, dtype=np.float64) - hw
    dy = np.arange(out_h, dtype=np.float64) - hh
    DX, DY = np.meshgrid(dx, dy)   # (out_h, out_w)

    # dst 좌표로부터 src 좌표를 역산
    # dst_x = focus * (R[0]·p + tx) / (R[2]·p + tz) + hw
    # → (dst_x - hw) / focus = (R[0]·p + tx) / (R[2]·p + tz)
    # 역 투영:  normalized 좌표 = [(dst_x-hw)/f,  (dst_y-hh)/f,  1]
    # 3D 방향벡터 d = R_inv @ [nd_x, nd_y, 1]
    # src 교차 평면 z=z_offset → t = (z_offset - tz·?) ...
    # 
    # 더 직관적인 역산: R·[sx-hw, sy-hh, z]^T = [u, v, w] 이므로
    #   w + tz = ... 를 연립해서 sx, sy를 구합니다.
    #
    # 실질적으로는 normalized image plane에서의 역투영입니다:
    #   let nd_x = (dst_x - hw) / focus,  nd_y = (dst_y - hh) / focus
    #   R·p + [tx, ty, tz]^T = lambda·[nd_x, nd_y, 1]^T  (lambda: 깊이)
    #   p[2] = z_offset 조건으로 lambda를 구합니다.

    nd_x = (DX) / focus   # (out_h, out_w)
    nd_y = (DY) / focus

    # R_inv @ ([nd_x, nd_y, 1] - t/lambda) = p
    # p[2] = z_offset  →  풀기:
    #   [sx-hw, sy-hh, sz] = R_inv @ (lambda*[nd_x, nd_y, 1] - [tx,ty,tz])
    #   sz = z_offset  →
    #   R_inv[2,0]*(lambda*nd_x - tx) + R_inv[2,1]*(lambda*nd_y - ty) + R_inv[2,2]*(lambda - tz) = z_offset
    #   lambda*(R_inv[2,0]*nd_x + R_inv[2,1]*nd_y + R_inv[2,2]) = z_offset + R_inv[2,0]*tx + R_inv[2,1]*ty + R_inv[2,2]*tz

    ri = R_inv
    denom = ri[2, 0] * nd_x + ri[2, 1] * nd_y + ri[2, 2]
    numer = z_offset + ri[2, 0] * tx + ri[2, 1] * ty + ri[2, 2] * tz

    with np.errstate(divide='ignore', invalid='ignore'):
        lam = np.where(np.abs(denom) > 1e-9, numer / denom, 0.0)

    # src 좌표 계산
    px = ri[0, 0] * (lam * nd_x - tx) + ri[0, 1] * (lam * nd_y - ty) + ri[0, 2] * (lam - tz) + hw
    py = ri[1, 0] * (lam * nd_x - tx) + ri[1, 1] * (lam * nd_y - ty) + ri[1, 2] * (lam - tz) + hh

    # 유효 범위 마스크
    mask = (lam > 0) & (px >= 0) & (px < w - 1) & (py >= 0) & (py < h - 1)

    # Bilinear interpolation용 좌표 변환
    map_x = px.astype(np.float32)
    map_y = py.astype(np.float32)

    # remap으로 한 번에 처리 (bilinear 보간 포함)
    remapped = cv2.remap(
        src, map_x, map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0)
    )

    # 유효 영역만 복사
    dst[mask] = remapped[mask]

    return dst


# ── 상태 정보 오버레이 ────────────────────────────────────────────────────────
def draw_overlay(img: np.ndarray, state: dict) -> np.ndarray:
    vis = img.copy()
    lines = [
        f"X-rot: {state['xangle']:+.0f} deg",
        f"Y-rot: {state['yangle']:+.0f} deg",
        f"Z-rot: {state['zangle']:+.0f} deg",
        f"Zoom (tz): {state['tz']:.0f}",
        f"Translate: ({state['tx']:.0f}, {state['ty']:.0f})",
        "",
        "[Enter]=Reset  [Arrow]=X/Y rot",
        "[S/X]=Z rot  [Z/A]=Zoom",
        "[G/H]=Tx  [R/V]=Ty  [Q]=Quit",
    ]
    x0, y0 = 10, 20
    for i, line in enumerate(lines):
        cv2.putText(vis, line, (x0, y0 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(vis, line, (x0, y0 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return vis


# ── 메인 루프 ─────────────────────────────────────────────────────────────────
def main():
    # 이미지 로드
    img_path = sys.argv[1] if len(sys.argv) > 1 else IMAGE_PATH
    src = cv2.imread(img_path)
    if src is None:
        # 이미지 없으면 테스트용 체커보드 생성
        print(f"[경고] '{img_path}' 를 찾을 수 없어 테스트 이미지를 생성합니다.")
        src = np.zeros((400, 600, 3), dtype=np.uint8)
        tile = 50
        for row in range(src.shape[0] // tile):
            for col in range(src.shape[1] // tile):
                color = (220, 220, 220) if (row + col) % 2 == 0 else (40, 40, 40)
                src[row*tile:(row+1)*tile, col*tile:(col+1)*tile] = color
        # 격자 선 추가
        cv2.putText(src, "TEST IMAGE", (150, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 180, 255), 3)

    # 상태 초기화
    state = dict(xangle=0.0, yangle=0.0, zangle=0.0,
                 tx=100.0, ty=100.0, tz=float(FOCUS))

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 900, 600)

    # 초기 렌더링
    result = render(src, **{k: state[k] for k in ('xangle','yangle','zangle','tx','ty','tz')})
    cv2.imshow(WINDOW_NAME, draw_overlay(result, state))

    print("사영 변환 데모 시작. 조작 방법은 화면 왼쪽 상단을 참고하세요.")

    while True:
        key = cv2.waitKey(0) & 0xFF
        dirty = True

        # ── 키 처리 ──────────────────────────────────────────────────────────
        if key in (ord('q'), 27):          # Q / ESC → 종료
            break

        elif key == 13:                    # Enter → 리셋
            state.update(xangle=0, yangle=0, zangle=0,
                         tx=100, ty=100, tz=float(FOCUS))
            print("[RESET]")

        elif key == 82 or key == 0:        # ↑ → X+ 회전
            state['xangle'] = min(state['xangle'] + ANGLE_STEP, 180)
        elif key == 84 or key == 1:        # ↓ → X- 회전
            state['xangle'] = max(state['xangle'] - ANGLE_STEP, -180)
        elif key == 83 or key == 3:        # → → Y+ 회전
            state['yangle'] = min(state['yangle'] + ANGLE_STEP, 180)
        elif key == 81 or key == 2:        # ← → Y- 회전
            state['yangle'] = max(state['yangle'] - ANGLE_STEP, -180)

        elif key == ord('s'):              # S → Z+ 회전
            state['zangle'] = min(state['zangle'] + ANGLE_STEP, 180)
        elif key == ord('x'):              # X → Z- 회전
            state['zangle'] = max(state['zangle'] - ANGLE_STEP, -180)

        elif key == ord('z'):              # Z → 확대 (tz 감소)
            state['tz'] -= ZOOM_STEP
        elif key == ord('a'):              # A → 축소 (tz 증가)
            state['tz'] += ZOOM_STEP

        elif key == ord('g'):              # G → 오른쪽 이동
            state['tx'] += TRANS_STEP
        elif key == ord('h'):              # H → 왼쪽 이동
            state['tx'] -= TRANS_STEP
        elif key == ord('v'):              # V → 아래 이동
            state['ty'] += TRANS_STEP
        elif key == ord('r'):              # R → 위 이동
            state['ty'] -= TRANS_STEP

        else:
            dirty = False

        # ── 재렌더링 ──────────────────────────────────────────────────────────
        if dirty:
            print(f"  xangle={state['xangle']:+.0f}  yangle={state['yangle']:+.0f}  "
                  f"zangle={state['zangle']:+.0f}  tz={state['tz']:.0f}")
            result = render(src, **{k: state[k] for k in ('xangle','yangle','zangle','tx','ty','tz')})
            cv2.imshow(WINDOW_NAME, draw_overlay(result, state))

    cv2.destroyAllWindows()
    print("종료.")


if __name__ == "__main__":
    main()