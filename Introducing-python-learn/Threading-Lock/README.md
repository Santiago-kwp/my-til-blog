# Threading

## 핵심 개념

### 1) Process vs Thread
- 프로세스 : 운영체제로부터 자원을 할당받아 실행중인 프로그램 (예: 하나의 식당 건물)
- 스레드 : 프로세스 내부에서 실제로 작업을 수행하는 실행 흐름의 단위 (예: 식당 안에서 요리하는 요리사들). 하나의 프로세스 내 스레드들은 **메모리(변수, 데이터)를 공유**함.

### 2) 파이썬의 특수성: GIL(Global Interpreter Lock)
- 파이썬(CPython)에는 한 번에 하나의 스레드만 파이썬 코드를 실행할 수 있도록 막는 GIL이라는 제약이 있음.
- CPU 집약적 작업(연산, 머신러닝): 멀티스레드로속도가 빨라지지 않으며, 오히려 오버헤드가 생김. (이 경우 `multiprocessing` 사용 권장)
- I/O 집약적 작업(웹 요청, 파일 읽기/쓰기, 네트워크 통신): 대기 시간 동안 다른 스레드가 일할 수 있어 **멀티스레드가 매우 효과적**임.

### 3) 락(Lock)이 필요한 이유
- 스레드들은 메모리를 공유하기 때문에, 두 개 이상의 스레드가 **동일한 변수에 동시에 쓰기/수정 작업을 할 때 데이터가 꼬이는 경쟁 상태(Race Condition)** 가 발생함.
- 락(Lock): 식당의 제한된 화장실을 들어가는 열쇠와 같이 한 스레드가 공유 자원을 사용하는 동안(임계 구역: Critical Section), 다른 스레드는 기다리게 만든다.

---

## 멀티 스레드 예제
```
import threading
import time

def worker(worker_id):
    print(f"[작업자 {worker_id}] 작업 시작")
    # 네트워크 요청이나 파일 I/O를 흉내 내는 대기 시간
    time.sleep(2)
    print(f"[작업자 {worker_id}] 작업 완료!")

if __name__ == "__main__":
    start_time = time.time()

    threads = []
    # 3개의 스레드 생성
    for i in range(1, 4):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start() # 스레드 실행 시작 (비동기)

    # 모든 스레드가 끝날 때까지 메인 스레드가 대기(join)
    for t in threads:
        t.join()

    # (예상) 2초 / (결과) 2초
    print(f"총 소요 시간: {time.time() - start_time:.2f}초")
```

- 결과 확인: 순차 실행이라면 6초가 걸려야 할 작업이 스레드를 통해 약 2초만에 끝남을 알 수 있다.
- 핵심 함수:
    - `t.start()`: 스레드에게 작업을 시작하도록 지시.
    - `t.join()`: 해당 스레드가 끝날 때까지 다음 줄로 넘어가지 않고 대기.
    - `for t in threads: t.join()`: 각 스레드를 순서대로 감시하지만, 이미 종료된 스레드에 대한 `join()`은 즉시 반환되므로 결과적으로 "가장 늦게 끝나는 스레드가 종료될 때까지 메인 스레드가 대기"하는 효과를 냄.

- 운영체제 관점에서 보면, `t.join()`은 내부적으로 대략 다음과 비슷한 의미
    ```python
    while t.is_alive():
        잠들기()
    ```
- 물론 실제 구현은 더 효율적인 동기화 객체(조건 변수, 락 등)를 사용하지만 개념적으로는:
    1. 메인 스레드가 `join()` 호출
    2. OS가 메인 스레드를 **Sleep/Waiting 상태** 로 전환
    3. 대상 스레드 종료
    4. OS가 메인 스레드를 깨움
    5. `join()` 반환
- 그래서 `join()`은 CPU를 계속 쓰면서 확인하는 바쁜 대기(Busy Waiting)가 아니라, **메인 스레드를 잠재웠다가 대상 스레드가 종료되면 다시 깨우는 동기화 메커니즘**이라고 이해하면 됨.

종료 시간이 같은 경우는 다음과 같이 1번 깨워질 수 있고,
```
Sleep 
  ↓ 
t1 종료 
  ↓ 
Wake-up (1회) 
  ↓ 
t2.join() 즉시 반환
  ↓ 
t3.join() 즉시 반환
```
종료 시간이 만약 다른 경우라면, 총 3번 깨워질 수 있음 
```
t1 -> 1초
t2 -> 3초
t3 -> 5초
```
```
Sleep 
  ↓ 
t1 종료 
  ↓ 
Wake-up (1회) 
  ↓ 
Sleep 
  ↓ 
t2 종료
  ↓ 
Wake-up (2회) 
  ↓ 
Sleep 
  ↓ 
t3 종료
  ↓ 
Wake-up (3회) 
```
- OS 입장에서는 `t.join()` 마다 **해당 스레드 종료 이벤트를 기다리는 대기 큐** 에 메인 스레드를 넣어둠
- 대상 스레드가 종료되면 상태 전이가 일어남
    ```
    RUNNING
      ↓ 
    WATING
      ↓ 
    RUNNABLE (OS가 깨움)
      ↓ 
    RUNNING
    ```

### 문제 상황 (경쟁 상태: Race Condition)
여러 스레드가 하나의 공유 변수(`shared_counter`)를 동시에 증가시키려 할 때 발생하는 문제

```python
import threading
import time

shared_counter = 0

def increase():
    global shared_counter
    for _ in range(100000):
        # 파이썬 내부에서 `shared_counter += 1`은
        # (1) 값 읽기 -> (2) 1 더하기 -> (3) 저장하기의 과정을 거침
        # 이 과정 중간에 다른 스레드로 제어권이 넘어가면 값이 유실됨
        shared_counter += 1

if __name__ == "__main__":
    t1 = threading.Thread(target=increase)
    t2 = threading.Thread(target=increase)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"기대 결과: 200000")
    print(f"실제 결과: {shared_counter}")
```
- 예상 결과: 결과 확인: 실행할 때마다 실제 결과가 200,000보다 작은 불규칙한 숫자가 나온다.
- 예상 원인: 두 스레드가 같은 시점의 이전 값을 읽어서 덮어쓰면서 연산 결과가 유실되었기 때문에
- 실제 실행 결과: 항상 같은 200,000이 나온다.
- 실제 원인: `shared_counter += 1` 자체는 원자적(atomic) 연산이 아니지만, CPython의 GIL 때문에 두 스레드가 거의 직렬적으로 실행되어 결과가 계속 200,000이 나옴.
    - 한 순간에는 `하나의 스레드만 파이썬 바이트코드를 실행`
    - 즉, `shared_counter += 1`를 수행하는 동안 스레드 전환이 잘 안 일어난다면, 아래와 같이 거의 순차 실행되어 결과가 100000 + 100000 = 200000
    ```
    T1
    T1
    T1
    ...
    T1
    T2
    T2
    T2
    ...
    T2
    ```
- 실제로 바이트코드를 보면
    ```python
    def increase():
        global shared_counter
        shared_counter += 1
    ```
    를 disassemble 하면 대략:
    ```
    LOAD_GLOBAL
    LOAD_CONST
    BINARY_OP
    STORE_GLOBAL
    ```
    여러 단계로 나뉨. 그래서 원자적이지 않음. 
    하지만 각 단계 사이에 항상 스레드 전환이 일어나는 것은 아님
- 최근 CPython에서는 GIL 스케쥴링이 달라지고 최적화도 되어 있어서 생각보다 잘 안깨짐. 그래서 요즘은 일부로 스레드 전환 지점을 만들어줌
    ```python
    def increase():
        global shared_counter

        for _ in range(100000):
            tmp = shared_counter
            time.sleep(0)   # 강제로 양보
            shared_counter = tmp + 1
    ```

---

### 락(Lock)으로 문제 해결
`threading.Lock`을 사용하여 한 번에 한 스레드만 카운터를 수정하도록 보호합니다.
추천 방식 : `with lock` 컨텍스트 매니저 사용
```python
import threading

shared_counter = 0 

# 1. 락 개체 생성
lock = threading.Lock()

def safe_increase():
    global shared_counter
    for _ in range(100000):
        # 2. 'with lock'을 쓰면 자동으로 acquire()(락 획득)과 release()(락 해제)를 처리해 준다.
        # 예외가 발생해도 안전하게 락이 해제되므로 가장 권장되는 패턴
        with lock:
            shared_counter += 1

if __name == "__main__"":
    t1 = threading.Thread(target=safe_increase)
    t2 = threading.Thread(target=safe_increase)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"기대 결과: 200000")
    print(f"실제 결과: {shared_counter}")

```

- 결과 확인: 매번 정확히 200000이 나옴
- 참고(수동 제어):
    ```python
    lock.acquire()  # 락 획득(누군가 쥐고 있으면 풀릴 때까지 대기)
    try:
        shared_counter += 1
    finally:
        lock.release()  # 반드시 해제해야 데드락(DeadLock)에 안 걸림
    ```
    - `with` 구문이 내부적으로 이 `try-finally`를 대신 처리해줌