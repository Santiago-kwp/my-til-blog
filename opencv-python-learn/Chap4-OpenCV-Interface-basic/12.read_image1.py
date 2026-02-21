import numpy as np
import cv2

def print_matInfo(name, image):
    match image.dtype:
        case 'uint8':
            mat_type = 'CV_8U'
        case 'int8':
            mat_type = 'CV_8S'
        case 'uint16':
            mat_type = 'CV_16U'
        case 'int16':
            mat_type = 'CV_16S'
        case 'float32':
            mat_type = 'CV_32F'
        case 'float64':
            mat_type = 'CV_64F'
    nchannel = 3 if image.ndim == 3 else 1

    ## depth, channel 출력
    print("%12s: depth(%s), channel(%s) -> mat_type(%sC%d)"
          % (name, image.dtype, nchannel, mat_type, nchannel))

title1, title2 = 'gray2gray', 'gray2color'                              # 윈도우 이름
gray2gray = cv2.imread("images/read_gray.jpg", cv2.IMREAD_GRAYSCALE)    # 명암도
gray2color = cv2.imread("images/read_gray.jpg", cv2.IMREAD_COLOR)       # 컬러 영상

## 예외처리 - 영상파일 읽기 여부 조사
if gray2gray is None or gray2color is None:
    raise Exception("gray2gray and gray2color are None")
print("행렬 좌표 (100, 100) 화소값")
print("%s %s" % (title1, gray2gray[100, 100]))                          # 행렬 내 한 화소값 표시
print("%s %s" % (title2, gray2color[100, 100]))

print_matInfo(title1, gray2gray)                                        # 행렬 정보 출력 함수 호출
print_matInfo(title2, gray2color)

cv2.imshow(title1, gray2gray)                                           # 행렬 정보를 영상으로 띄우기
cv2.imshow(title2, gray2color)
cv2.waitKey(0)