import numpy as np, cv2
"""
cv2.sortIdx() 함수를 이용해서 다음 조건에 부합하도록 벡터의 원소를 정렬하시오
1) 벡터의 원소는 Rect 객체이다.
2) 벡터의 원소는 임의로 지정한다.
3) 정렬의 기준은 Rect 객체의 크기이다.
4) 오름차순으로 정렬하여 콘솔창에 출력한다.
"""
# rect : (x, y, w, h) 튜플
rects = np.array([(10,20,50,40), (30,40,20,10), (5,5,100,80)], np.int32)

# 면적 계산
areas = np.array([w*h for (_,_,w,h) in rects], np.int32).reshape(-1,1)

"""
.reshape(-1, 1) 의미 
-1 : 자동 계산. 전체 원소 개수를 기준으로 행 개수를 알아서 맞춰줍니다.
1 : 열 개수를 1로 고정합니다.
즉, 1차원 배열을 세로 방향(열 벡터)으로 바꿔주는 것입니다.
"""

# 면적 기준 정렬 인덱스
sort_idx = cv2.sortIdx(areas, cv2.SORT_EVERY_COLUMN + cv2.SORT_ASCENDING)

# 정렬된 Rect 벡터
sorted_rects = rects[sort_idx.flatten()]
print("원본 Rects:\n", rects)
print("면적:\n", areas.flatten())
print("정렬 인덱스:\n", sort_idx.flatten())
print("정렬된 Rects:\n", sorted_rects)

# 시각화 예시
canvas = np.zeros((200,200,3), np.uint8)
for (x,y,w,h) in sorted_rects:
    cv2.rectangle(canvas, (x,y), (x+w,y+h), (0,255,0), 2)

cv2.imshow("Sorted Rects", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()