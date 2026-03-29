import numpy as np, math, cv2

def contain(p, shape):  # 좌표가 (y,x)가 범위 내 인지 검사
    return 0<= p[0] < shape[0] and 0<= p[1] < shape[1]


def scaling(img, size):
    dst = np.zeros(size[::-1], img.dtype)   # size와 shape는 원소 역순
    ratioY, ratioX = np.divide(size[::-1], img.shape[:2])   # 비율 계산
    y = np.arange(0, img.shape[0], 1)   # 입력 영상 세로(y) 좌표 생성
    x = np.arange(0, img.shape[1], 1)   # 입력 영상 가로(x) 좌표 생성
    y, x = np.meshgrid(y, x)            # i, j 좌표에 대한 좌표 행렬 생성
    i, j = np.int32(y * ratioY), np.int32(x * ratioX)   # 목적 영상 좌표
    dst[i, j] = img[y, x]               # 정방향 사상 -> 목적 영상 좌표 계산
    return dst

def scaling_nearest(img, size):
    """
    OpenCV나 일반적인 그래픽스에서 이미지의 크기(size)를 지정할 때는 x축(가로, Width) 먼저, y축(세로, Height) 
    예: 해상도가 800x600인 이미지라면 size = (800, 600)

    반면, 파이썬의 NumPy 배열에서 형태(shape)를 정의할 때는 행(Row, 세로, y축) 먼저, 열(Column, 가로, x축) 나중의 순서로 표현합니다.
    예: 높이가 600, 폭이 800인 빈 이미지를 만들려면 행렬 크기는 (600, 800)이 되어야 합니다.
    """
    dst = np.zeros(size[::-1], img.dtype)   # 행렬과 크기는 원소가 역순
    ratioY, ratioX = np.divide(size[::-1], img.shape[:2])   # 변경 크기 비율
    i = np.arange(0, size[1], 1)    # 목적 영상 세로(i) 좌표 생성
    j = np.arange(0, size[0], 1)    # 목적 영상 가로(j) 좌표 생성
    i, j = np.meshgrid(i, j)
    y, x = np.int32(i / ratioY), np.int32(j / ratioX)   # 입력 영상 좌표
    dst[i, j] = img[y, x]       # 역방향 사상 -> 입력 영상 좌표 계산

    return dst

def bilinear_value(img, pt):    # 단일 화소 양선형 보간 수행 함수
    x, y = np.int32(pt)
    if x >= img.shape[1]-1: x = x - 1 # 영상 범위 벗어남 처리
    if y >= img.shape[0]-1: y = y - 1

    P1, P2, P3, P4 = np.float32(img[y:y+2,x:x+2].flatten()) # 4개 화소 - 관심 영역을 접근
    ## 4개 화소 - 화소 직접 접근
    # P1 = float(img[y,x])        # 좌상단 화소
    # P2 = float(img[y+0, x+1])   # 우상단 화소
    # P3 = float(img[y+1, x+0])   # 좌하단 화소
    # P4 = float(img[y+1, x+1])   # 우하단 화소


    alpha, beta = pt[1] - y, pt[0] - x
    M1 = P1 + alpha * (P3 - P1)     # 1차 보간
    M2 = P2 + alpha * (P4 - P2)
    P = M1 + beta * (M2 - M1)       # 2차 보간
    return np.clip(P, 0, 255)   # 화소값 saturation 후 반환

def rotate_pt(img, degree, pt):                 # pt 기준 회전 변환 함수
    dst = np.zeros(img.shape[:2], img.dtype)    # 목적 영상 생성
    radian = (degree/180) * np.pi               
    sin, cos = math.sin(radian), math.cos(radian)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            jj, ii = np.subtract((j, i), pt)    # 중심 좌표로 평행이동
            y = -jj * sin + ii * cos
            x = jj * cos + ii * sin
            x, y = np.add((x,y), pt)        # 중심 좌표로 평행 이동
            if contain((y,x), img.shape):   # 입력 영상의 범위 확인
                dst[i, j] = bilinear_value(img, (x, y))
    return dst


def affine_transform(img, mat): # 어파인 변환 수행 함수
    rows, cols = img.shape[:2]
    invMat = cv2.invertAffineTransform(mat) # 어파인 변환의 역행렬
    size = img.shape[::-1]
    ## 리스트 생성 방식
    pts = [np.dot(invMat, (j, i, 1)) for i in range(rows) for j in range(cols)]
    dst = [bilinear_value(img, p) if contain(p, size) else 0 for p in pts]
    dst = np.reshape(dst, (rows, cols)).astype('uint8') # 1차원 -> 2차원

    return dst
