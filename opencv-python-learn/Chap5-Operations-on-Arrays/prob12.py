import cv2, numpy as np

# 영상 파일을 읽어서 메인 윈도우에 다음과 같이 출력하시오
# 1) 메인 윈도우의 특정 부분 2곳을 관심 영역으로 지정한다.
# 2) 관심 영역1는 영상의 밝기를 50만큼 밝게 한다.
# 3) 관심 영역2은 영상의 화소대비를 증가시킨다.

image = cv2.imread("images/flip_test.jpg", cv2.IMREAD_COLOR)
cv2.imshow("Image", image)
print(image.shape) # (267, 360, 3)

# img[y:y+h, x:x+w]
roi1 = image[50:150, 150:250] # (150, 50)부터 가로 100, 세로 100 영역
roi2 = image[150:200, 250:300]

# 50만큼 밝게
bright = cv2.add(roi1, 50)

# 명암비 조절 (s > 1 : 대비 증가, 0 < s < 1 : 대비 감소)
sc = 1.5
scale = cv2.multiply(roi2, sc) # 또는 np.clip(src * scale, 0, 255).astype(np.uint8)


# 원본 영상에 덮어쓰기
image[50:150, 150:250] = bright
image[150:200, 250:300] = scale

# 결과 출력
cv2.imshow("Modified Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()