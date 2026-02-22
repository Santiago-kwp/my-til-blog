import numpy as np, cv2

def calc_histo(image, hsize, ranges=[0, 256]):
    hist = np.zeros((hsize, 1), np.float32)  # 히스토그램 누적 행렬
    gap = ranges[1]/hsize   # 계급 간격, hsize : 간격 수 -> hsize=256 → gap=1, 즉 각 밝기 값마다 하나의 bin.

    for i in (image/gap).flat: # .flat → NumPy 배열을 1차원 반복자로 펼쳐서 모든 화소를 순회.
        hist[int(i)] += 1 # 예: 화소값이 200이고 gap=4라면 200/4 = 50, 즉 50번째 bin에 속함.
    return hist

image = cv2.imread("images/pixel.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise ValueError("Cannot read the image")

histSize, ranges = [32], [0, 256] # 히스토그램 간격수, 값 범위
gap = ranges[1]/histSize[0]       # 계급 간격
ranges_gap = np.arange(0, ranges[1]+1, gap) # 넘파이 계급범위 & 간격
hist1 = calc_histo(image, histSize[0], ranges) # User 함수
hist2 = cv2.calcHist([image], [0], None, histSize, ranges)
hist3, bins = np.histogram(image, ranges_gap)   # numpy 모듈 함수

print("User 함수: \n", hist1.flatten())
print("OpenCV 함수: \n", hist2.flatten())
print("numpy 함수: \n", hist3)