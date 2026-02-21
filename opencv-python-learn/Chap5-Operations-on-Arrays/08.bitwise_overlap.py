import numpy as np, cv2

image = cv2.imread("images/bit_test.jpg", cv2.IMREAD_COLOR)
logo = cv2.imread("images/logo.jpg", cv2.IMREAD_COLOR)
if image is None or logo is None: raise Exception("Invalid image")

print(logo.shape, type(logo)) # 308, 250, 3 <class 'numpy.ndarray'> -> 넘파이 배열
masks = cv2.threshold(logo, 220, 255, cv2.THRESH_BINARY)[1] # 로고 영상 이진화 : 기준값 220 보다 작은 화소는 0으로 큰 화소는 255로 만든다. 각 채널별로 이진화를 수행하며 결과 행렬도 3채널 행렬
print(masks.shape, type(masks)) # 308, 250, 3 <class 'numpy.ndarray'> -> 넘파이 배열
masks = cv2.split(masks) # 3채널인 행렬을 분리하여 단일채널 3개를 갖는 행렬로 만든다.
print(np.shape(masks), type(masks)) # 3, 308, 250 <class 'tuple'> -> 길이 3인 튜플

fg_pass_mask = cv2.bitwise_or(masks[0], masks[1])       # blue 채널, green 채널 마스크부터 생성
fg_pass_mask = cv2.bitwise_or(masks[2], fg_pass_mask)   # 전경 통과 마스크 -> 컬러 영상의 각 채널에서 220보다 큰 값을 갖는 부분만 흰색으로 만들어 전경 통과 마스크를 생성한다.
bg_pass_mask = cv2.bitwise_not(fg_pass_mask)            # 배경 통과 마스크

(H, W), (h, w) = image.shape[:2], logo.shape[:2]    # 전체 영상, 로고 영상 크기
x, y = (W-w)//2, (H-h)//2   # 시작 좌표 계산
roi = image[y:y+h, x:x+w]   # 관심 영역(roi) 지정

## 행렬 논리곱과 마스킹을 이용한 관심 영역 복사
foreground = cv2.bitwise_and(logo, logo, mask=fg_pass_mask)     # 로고의 전경만 복사
background = cv2.bitwise_and(roi, roi, mask=bg_pass_mask)       # 원본 roi의 배경만 복사

dst = cv2.add(background, foreground)   # 로고 전경과 원본 배경 간 합성
image[y:y+h, x:x+w] = dst               # 합성 영상을 원본에 복사

cv2.imshow("background", background); cv2.imshow("foreground", foreground)
cv2.imshow("dst", dst); cv2.imshow("image", image)
cv2.waitKey()
cv2.destroyAllWindows()

