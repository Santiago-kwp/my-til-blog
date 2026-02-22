import numpy as np, cv2

def draw_histo(hist, shape=(200, 256)):
    hist_img = np.full(shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX) # 정규화
    gap = hist_img.shape[1]/hist.shape[0]   # 한 계급 너비

    for i, h in enumerate(hist):
        x = int(round(i * gap))
        w = int(round(gap))
        # 1. h는 [값] 형태의 배열이므로 h[0]으로 숫자를 꺼냅니다.
        h_val = int(h[0])
        cv2.rectangle(hist_img, (x, 0, w, h_val), 0, cv2.FILLED)

    return cv2.flip(hist_img, 0) # 영상 상하 뒤집기 후 반환

image = cv2.imread("images/pixel.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Could not open image")

hist = cv2.calcHist([image], [0], None, [32], [0, 256]) # hist는 (32, 1) 형태의 2차원 넘파이 배열
hist_img = draw_histo(hist)

cv2.imshow("image", image)
cv2.imshow("hist_img", hist_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
