# Python Thread Lock Intro

## 1. 기초 개념
### 1.1 왜 락이 필요한가: Race Condition
> 여러 스레드가 공유 상태를 읽고 $\rarr$ 판단하고 $\rarr$ 쓰는 사이에 다른 스레드가 끼어들면 결과가 깨짐 가장 흔한 형태가 **check-then-act**

```python
import threading, time

balance = 100

def withdraw(amount):
    global balance
    if balance >= amount:      # 1) check
        time.sleep(0.001)      # 컨텍스트 스위칭을 일부러 유도
        balance -= amount      # 2) act

threads = [threading.Thread(target=withdraw, args=(100,)) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()

print(balance)  # 100이 한 번만 빠져야 하는데 -900 같은 값이 나옴
```

### 1.2 파이썬은 GIL(Global Interpreter Lock) 있는데 왜 락이 필요하죠?

1. GIL은 인터프리터 내부(참조 카운터 등)를 보호할 뿐, 내 코드의 불변식을 보호하지 않는다. GIL은 바이트코드 단위로 스레드를 바꿈(기본 전환 주기 5ms, `sys.getswitchinterval()`). I/O나 `sleep` 중에는 GIL이 풀림
2. `counter += 1` 조차 원자적이지 않음. 바이트코드를 보면 `LOAD -> ADD -> STORE` 3단계라 중간에 끊길 수 있음

    ```python
    import dis
    dis.dis("counter += 1") # 파이썬 소스 코드를 CPython이 실제로 어떤 바이트코드로 변환해서  실행하는지 보여주는 함수
    #  0           RESUME                   0

    #  1           LOAD_NAME                0 (counter)
    #              LOAD_SMALL_INT           1
    #              BINARY_OP               13 (+=)
    #              STORE_NAME               0 (counter)
    #              LOAD_CONST               1 (None)
    #              RETURN_VALUE
    ```
    - `RESUME 0` : Python 3.11 이후에 추가된 바이트코드. 인터프리터가 함수나 코드 실행을 시작할 때 사용하는 내부 명령
    - `LOAD_NAME 0 (counter)`: counter 값을 스택에 올려라
        - 예를 들어, `counter = 100` 이라면, `스택 | 100` 상태가 됨.
    - `LOAD_SMALL_INT 1`: 정수 1을 스택에 올려라
        - 결과, `스택 | 100 | 1` 상태가 됨
    - `BINARY_OP 13 (+=)`: 스택에서 두 값을 꺼내 계산합니다.
        - 결과, `스택 | 101` 상태가 됨
    - `STORE_NAME 0 (counter)` : 스택의 결과를 변수에 저장합니다.
        - 즉, `counter = 101`이 수행 됨


3. `list.append`, `dict[k] = v` 같은 단일 연산은 CPython에서 사실상 원자적이지만 **구현 세부사항** 일 뿐 언어 보장이 아님. 게다가 Python 3.13부터 GIL 없는 free-threaded 빌드가 도입되어(3.14에서 정식 지원 단계), GIL에 기대는 코드는 더더욱 위험함.

