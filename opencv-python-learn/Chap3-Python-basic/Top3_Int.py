import numpy as np

class NumCnt:
    def __init__(self, num):
      self.num = num
      self.cnt = 0

    def addCnt(self):
        self.cnt+=1

    def __repr__(self): return f"NumCnt(num={self.num}, cnt={self.cnt})"

# 난수 생성
a = np.random.randint(0,50, 500)

# 0~50까지 객체 생성
num_objs = [NumCnt(i) for i in range(51)]

# 카운트 업데이트
for val in a:
    num_objs[val].addCnt()

# 가장 많이 나온 3개 찾기
top3 = sorted(num_objs, key=lambda x: x.cnt, reverse=True)[:3]

# 출력
for obj in top3:
    print(f"숫자 {obj.num} : {obj.cnt}회")