import numpy as np, cv2

image = cv2.imread("images/color_model.jpg", cv2.IMREAD_COLOR)

print(image.shape)

# RGB to HSV

image_hsv = cv2.cvtColor(image,  cv2.COLOR_BGR2HSV)
print(image_hsv[:,:,0].shape)

cv2.imshow("image-hue", image_hsv[:,:,0])
cv2.imshow("image-saturation", image_hsv[:,:,1])
cv2.imshow("image-value", image_hsv[:,:,2])
"""
2차원 히스토그램의 Hue(세로)와 Saturation(가로)을 2개 축으로 구성하고, 
빈도값을 밝기로 표현해서 오른쪽 그림과 같이 2차원 그래프로 그리시오
"""

histo2d = cv2.calcHist([image_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
print(histo2d.shape) # (180, 256) 해당 (H,S) 조합의 빈도 수

# 정규화
cv2.normalize(histo2d, histo2d, 0, 255, cv2.NORM_MINMAX)

h, s = np.indices(histo2d.shape)
# h.shape = (180, 256), 값은 행 인덱스 = Hue
# s.shape = (180, 256), 값은 열 인덱스 = Saturation
v = histo2d * 256# 정규화된 빈도수

hsv_img = np.stack([h, s, v], axis=2).astype(np.uint8)
print(hsv_img[:,:,2])
bgr_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

def draw_histo2(hist):
    if hist.ndim != 2: print('2차원 히스토그램 아님')
    h, w = hist.shape[:2]
    graph = [[(i, j, hist[i,j]) for j in range(w)] for i in range(h)]
    ratios = (180/h, 256/w, 256 )
    graph= np.multiply(graph, ratios).astype('uint8')
    bgr = cv2.cvtColor(graph, cv2.COLOR_HSV2BGR)
    bgr = cv2.resize(bgr, None, fx=10, fy=10, interpolation=cv2.INTER_AREA)

    return bgr

print(histo2d.dtype)   # float32 아닌가요?
print(histo2d.max())   # 255.0?
print(histo2d[histo2d > 0][:10])  # 0보다 큰 값들


cv2.imshow("histo2d", histo2d)

dst = draw_histo2(histo2d)
cv2.imshow("dst", dst)

cv2.imshow("bgr", bgr_img)


cv2.waitKey(0)
cv2.destroyAllWindows()

