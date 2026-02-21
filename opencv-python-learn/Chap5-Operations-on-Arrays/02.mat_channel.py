import numpy as np
import cv2

## numpy.ndarray를 이용해 행렬 생성 및 초기화 방법
ch0 = np.zeros((2, 4), np.uint8) + 10
ch1 = np.ones((2, 4), np.uint8) * 20
ch2 = np.full((2, 4), 30, np.uint8)

list_bgr = [ch0, ch1, ch2]  # 단일채널 행렬들을 모아 리스트로 구성
merge_bgr = cv2.merge(list_bgr) # 채널 합성
split_bgr = cv2.split(merge_bgr) # 채널 분리: 컬러 영상 -> 3채널 분리

print("split_bgr 행렬 형태", np.array(split_bgr).shape) # (3, 2, 4)
print("merge_bgr 행렬 형태", merge_bgr.shape) # (2, 4, 3)
print("[ch0] = \n%s" % ch0) # 단일채널 원소 출력
print("[ch1] = \n%s" % ch1) # 단일채널 원소 출력
print("[ch2] = \n%s" % ch2) # 단일채널 원소 출력
print("[merge_bgr] = \n %s\n" % merge_bgr) # 다채널 원소 출력 : 2행, 4열, 3개 채널

print("[split_bgr[0]] = \n %s\n" % split_bgr[0]) # 분리 채널 결과 출력 = ch0과 같음
print("[split_bgr[1]] = \n %s\n" % split_bgr[1]) # 분리 채널 결과 출력 = ch1과 같음
print("[split_bgr[2]] = \n %s\n" % split_bgr[2]) # 분리 채널 결과 출력 = ch2과 같음

