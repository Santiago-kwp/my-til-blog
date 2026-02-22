import numpy as np, cv2

def make_palette(rows): # hue 채널 팔레트 행렬 생성 함수로, 막대그래의 각 막대에 칠할 무지개색 물감(팔레트)를 만드는 함수
    ## 리스트 생성 방식
    hue = [round(i * 180 / rows) for i in range(rows)]  # hue 값 리스트 계산, hue는 0~180까지의 값을 갖는다. rows = 막대개수, 막대개수만큼 hue를 일정한 간격으로 쪼개어 색상 값 리스트를 만듦
    hsv = [[[h, 255, 255]] for h in hue]    # (hue, 255, 255) 화소값 계산 > HSV 색상 공간에서 S(채도)와 V(명도)를 최고치인 255로 설정합니다. 즉, 탁하거나 어둡지 않은 가장 순수하고 쨍한 원색을 만듭니다.
    hsv = np.array(hsv, dtype=np.uint8)     # 정수형 행렬 변환 : OpenCV 이미지 형식에 맞추기 위해 넘파이의 8비트 정수 배열(np.uint8)로 변환합니다.

    ## 반복문 방식
    #hsv = np.full((rows, 1, 3), (255, 255, 255), np.uint8)
    #for i in range(0, rows):            # 행수만큼 반복
    #    hue = round(i / rows * 180)     # 색상 계산
    #    hsv[i] = (hue, 255, 255)        # HSV 컬러 지정

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) # HSV 컬러 -> BGR 컬러 : HSV 색상들을 OpenCV가 알아먹을 수 있게 BGR 색상으로 변환해서 반환합니다.


def draw_hist_hue(hist, shape=(200, 256, 3)):
    hsv_palette = make_palette(hist.shape[0])   # 색상 팔레트 생성: 막대 개수(hist.shape[0])만큼의 색상 물감을 hsv_palette에 준비합니다.
    hist_img = np.full(shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX) # 영상 높이값으로 정규화 : 픽셀 개수가 1만 개, 10만 개든 상관없이, 가장 높은 막대의 높이가 도화지의 천장(shape[0], 즉 200)에 딱 닿도록 비율을 압축/조절(정규화)합니다.

    gap = hist_img.shape[1] / hist.shape[0] # 도화지의 가로 길이(shape[1])를 막대 개수(hist.shape[0])로 나누어 **막대 1개의 두께(gap)**를 계산합니다.
    for i, h in enumerate(hist):
        x, w = int(round(i * gap)), int(round(gap))
        color = tuple(map(int, hsv_palette[i][0]))  # 정수형 튜플로 변환
        cv2.rectangle(hist_img, (x, 0, w, int(h[0])), color, cv2.FILLED)

    return cv2.flip(hist_img, 0)

image = cv2.imread("images/hue_hist.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("Could not open image")

hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hue_hist = cv2.calcHist([hsv_img], [0], None, [18], [0, 180])
hue_hist_img = draw_hist_hue(hue_hist, (200, 360, 3)) # 히스토그램 그래프

cv2.imshow("image", image)
cv2.imshow("hue_hist_img", hue_hist_img)
cv2.waitKey(0)
cv2.destroyAllWindows()