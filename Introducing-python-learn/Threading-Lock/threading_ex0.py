import threading, time

balance = 100

def withdraw(amount):
    global balance
    if balance >= amount:
        time.sleep(0.001) # time.sleep() 있는 경우는 -900 , 없는 경우는 0
        balance -= amount

"""
withdraw()를 CPU가 실제로 실행하는 단계로 쪼개보면 다음과 같음

if balance >= amount:
    balance -= amount

대략 다음 과정으로 이루어짐
1. balance 읽기
2. amount와 비교
3. 조건 통과 여부 결정
4. balance 읽기
5. balance - amount 계산
6. balance에 저장

초기값은 balance = 100 이고 스레드 10개가 모두 withdraw(100)을 수행함

---
### sleep이 있을 떄
- 스레드A 실행
- balance >= 100 # True 확인
- 그 직후 time.sleep : `time.sleep(0.001)`
- 그러는 동안 스레드 B도 실행
- balance >= 100 # True 확인 후 sleep
- 스레드 C 실행
- balance >= 100 # True 확인 후 sleep
- 이런 식으로 10개 스레드가 전부 balance == 100 인 시점에 조건 검사를 끝냄
- 즉, 모든 스레드가 돈이 충분하다고 판단함
- 결과적으로 10번의 잔액 인출이 실행되어 100 -> -900이 됨

### sleep이 없을 때
- 스레드 A가 `if balance >= amount: balance -= amount` 까지 즉, 조건 검사 및 잔액 차감까지 연속으로 수행해버림
- 스레드 B가 `if balance >= 100`을 검사하면 이미 balance=0 이므로 False가 됨
- 나머지 모든 스레드도 조건 검사에 실패하며 100 -> 0으로 종료

--- 
### GIL 때문인가?
파이썬의 GIL(Global Interpreter Lock)은 '한 순간에 하나의 스레드만 Python 바이트코드를 실행'하게 할 뿐임
즉, '조건 검사 + 차감'을 하나의 원자 연산(atomic operation)으로 만들어주지는 않음
다음과 같은 순서도 가능함
```
Thread A : balance >= 100 확인
(컨텍스트 스위치)

Thread B : balance >= 100 확인
(컨텍스트 스위치)

Thread A : balance -= 100
(컨텍스트 스위치)

Thread B : balance -= 100
그래서 GIL 이 있어도 race condition은 발생할 수 있음.
---
### 왜 sleep이 race condition을 더 잘 드러내는가?
- `time.sleep()`은 현재 스레드가 CPU를 포기하게 만듦
- `if balance >= amount: time.sleep(0.001)` 여기서 확실하게 다른 스레드들이 실행될 기회를 얻음
- 그래서 검사(check) -> 차감(update) 사이의 간격이 매우 넓어짐. 
- 결과적으로 여러 스레드가 조건은 모두 True로 보는 상태가 되어버리고, 이후 차감만 중복 실행됨
"""
# 인출 스레드 10개 생성
threads = [threading.Thread(target=withdraw, args=(100,)) for _ in range(10)]

for t in threads: t.start()
for t in threads: t.join()

# 그 결과 if 조건에 상관없이 인출이 10번 되어버림
print(balance)

"""
실제로 안전하게 만들려면
조건 검사와 차감을 하나의 임계 구역(Critical Section)으로 묶어야 함
"""

balance = 100
lock = threading.Lock()

def withdraw2(amount):
    global balance

    with lock:
        if balance >= amount:
            balance -= amount


# 인출 스레드 10개 생성
threads = [threading.Thread(target=withdraw2, args=(100,)) for _ in range(10)]

for t in threads: t.start()
for t in threads: t.join()

print(balance)