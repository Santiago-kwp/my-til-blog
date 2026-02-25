import numpy as np, cv2
from Common.histogram import draw_histo

def search_value_idx(hist, bias=0): # 값 있는 첫 계급 함수
    for i in range(hist.shape[0]):
        idx = np.abs(bias - i)          # 검색 위치(처음 또는 마지막)
        if hist[idx] > 0: return idx    # 위치 반환
    return -1                           # 대상 없으면 반환

image = cv2.imread("images/dst.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Could not read image")

bsize, ranges = [64], [0,256] # 계급 개수 및 화소 범위
hist = cv2.calcHist([image], [0], None, bsize, ranges)

bin_width = ranges[1]/bsize[0]                              # 한 계급 너비 ex. 256/64 : 4
low = search_value_idx(hist, 0) * bin_width             # 최저 화소값
high = search_value_idx(hist, bsize[0] - 1) * bin_width     # 최고 화소값

idx = np.arange(0, 256)     # 룩업 인덱스(0~255) 생성
idx = (idx - low) / (high - low) * 255     # 수식 적용하여 룩업 인덱스 완성
idx[0:int(low)] = 0          # 히스토그램 하위 부분
idx[int(high+1):] = 255      # 히스토그램 상위 부분

print("idx =\n", idx)
dst = cv2.LUT(image, idx.astype("uint8"))   # image 행렬의 모든 화소값을 idx의 첨자로 원소값을 가져오며, 가져온 모든 값들을 결과 행렬의 원소값으로 저장해서 dst 행렬을 생성한다.

hist_dst = cv2.calcHist([dst], [0], None, bsize, ranges)    # 결과 히스토그램 재계산
hist_img = draw_histo(hist, (200, 360))     # 원본 영상 히스토그램 그리기
hist_dst_img = draw_histo(hist_dst, (200, 360))     # 결과 영상 히스토그램 그리기

print("high value=", high)
print("low value=", low)
cv2.imshow("image", image); cv2. imshow("hist_img", hist_img)
cv2.imshow("dst", dst); cv2.imshow("hist_dst_img", hist_dst_img)
cv2.waitKey(0)
cv2.destroyAllWindows()



    


