import numpy as np, cv2

m = np.random.randint(0, 100, 15).reshape(3, 5) # 임의 난수 생성
## 행렬 원소 정렬
sort1 = cv2.sortIdx(m, cv2.SORT_EVERY_ROW) # 행 단위(가로 방향) 오름차순
sort2 = cv2.sortIdx(m, cv2.SORT_EVERY_COLUMN)   # 열 방향 정렬
sort3 = np.argsort(m, axis=0)           # y축 방향 정렬

titles = ['m','sort1','sort2','sort3']
for title in titles:
    print("[%s] = \n%s\n" %(title, eval(title)))