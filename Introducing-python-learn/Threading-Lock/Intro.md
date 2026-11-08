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
   - `LOAD_CONST 1 (None)` : 코드 블록 종료 시 반환값 준비
     - None을 스택에 적재합니다.
   - `RETURN_VALUE` : 실행 종료
   - 예를 들어, counter = 100 이고 스레드 A, B 가 동시에 실행된다고 하자.
   - Thread A : LOAD_NAME -> 읽은 값 = 100 // 스레드 전환
   - Thread B : LOAD_NAME, LOAD_SMALL_INT, BINARY_OP, STORE_NAME 실행 -> counter = 101 // 스레드 전환
   - Thread A : 이미 읽어 둔 100을 사용해서 100 + 1 = 101 계산 후 저장 -> counter = 101
   - 최종 결과 : 101 이 되어 원래라면 102가 되어야 하지만 증가가 한 번 사라짐. 이것이 Lost Update(갱신 손실)
   - GIL이 보장하는 것은 같은 순간에 두 스레드가 Python 바이트코드를 동시에 실행하지 못한다는 것 뿐임.
     - 즉, LOAD_NAME, LOAD_SMALL_INT, BINARY_OP, STORE_NAME 전체를 연속적으로 한 묶음 단위로 실행되도록 보장해주지는 않는다.
     - 중간에 LOAD_NAME 까지만 실행하고 다른 스레드로 넘어갈 수 있다.
     - 따라서 `counter += 1` 은 여전히 원자적(atomic)이지 않는다.
   - 최근 CPython 3.11 ~ 3.13 계열은 바이트코드 실행 속도가 매우 빨라졌고, counter += 1 같은 짧은 구간은 GIL 을 쥔 상태에서 순식간에 끝나버림. 그래서 경쟁 상태가 존재는 하지만 잘 드러나지 않는 것뿐임.

3. `list.append`, `dict[k] = v` 같은 단일 연산은 CPython에서 사실상 원자적이지만 **구현 세부사항** 일 뿐 언어 보장이 아님. 게다가 Python 3.13부터 GIL 없는 free-threaded 빌드가 도입되어(3.14에서 정식 지원 단계), GIL에 기대는 코드는 더더욱 위험함.
   - 원자적 연산은 즉, 중간에 다른 스레드가 끼어들 수 없이 '한번에 끝나는 연산'을 말함.
   - 지금까지 안전했던 이유: 주로 쓰는 파이썬 인터프리터(CPython)는 C 언어로 만들어짐. `list.append(x)`를 실행하면, CPython 내부에서 단 하나의 바이트코드(`LIST_APPEND`)로 실행됨. 이때 GIL이 걸려 있으므로, CPython 내부 로직이 끝날 때까지 다른 스레드가 끼어들지 못해 **결과적으로 안전(Thread-safe)** 했음
   - 파이썬 공식 문서 어디에도 **스레드끼리 락 없이 `append` 나 `dict` 수정을 해도 안전하다** 고 보장한다는 내용은 없음. 단지 우리가 쓰는 CPython 인터프리터 구조 상 우연히 그렇게 작동했을 뿐임(즉, 구현 세부사항이지 원칙은 아님). 따라서 PyPy, JPython 같은 파이썬 구현체에서는 이미 깨질 수 있는 코드임.
   - 파이썬의 가장 큰 단점(스레드를 여러 개 만들어도 CPU 코어를 한 개밖에 못씀)을 해결하기 위해, **Python 3.13 부터 GIL을 완전히 제거할 수 있는 버전(Free-threaded Python, PEP 703)** 이 실험적으로 추가됨.
     - GIL 이 있을 때 : 스레드가 10개여도 동시에 실행되는 바이트코드는 1개뿐
     - GIL이 없을 때: CPU 코어가 8개라면, 진짜로 8개의 스레드가 동시에 CPython 내부 코드를 실행함
   - 예를 들어 두 스레드가 동시에 `list.append()` 를 할 때 파이썬 리스트는 내부적으로 크기가 고정된 C 배열임. 공간이 꽉 차면 메모리를 더 큰 곳으로 재할당(Reallocate)해서 이사해야 함.
     1. 과거(GIL있음)
     - A 스레드가 이사하고 데이터를 넣는 동안 GIL이 다른 스레드를 막아주므로 안전함.
     2. 미래(GIL 없음 - Free-threaded)
     - 스레드 A가 "리스트가 꽉 찼네, 더 큰 메모리로 옮겨야지" 하고 기존 메모리를 해제하는 순간
     - 스레드 B가 동시에 "나도 넣어야지" 하고 이미 해제된 메모리에 접근할 수 있음
     - 결과: 값이 덮어써지는 수준이 아니라, 프로그램이 `Segmentation fault` (강제 종료)로 뻗어버리거나 메모리가 오염됨

### 1.3 임계 구역(Critical Section)

"읽고-판단하고-쓰기"가 한 덩어리로 실행되어야 하는 구간. 락은 이 구간에 한 번에 한 스레드만 들어가도록 보장함.

```python
lock = threading.Lock()

def withdraw(amount):
    global balance
    with lock:
        if balance >= amount:
            time.sleep(0.001)
            balance -= amount
                                # 블록을 벗어나면 자동 release
```

## 2. `threading` 동기화 도구 정리

| 도구                           | 용도                                 | 상황                                      |
| ------------------------------ | ------------------------------------ | ----------------------------------------- |
| `Lock`                         | 기본 상호배제                        | 거의 모든 상황                            |
| `RLock`                        | 같은 스레드가 재진입 가능            | 락 잡은 메서드가 다른 락 잡는 메서드 호출 |
| `Condition`                    | 조건이 만족될 때까지 대기/깨우기     | 생산자-소비자, "재고 생기면 처리"         |
| `Semaphore`/`BoundedSemaphore` | 동시 진입 개수 N개 제한              | 외부 API 동시 호출 제한, 커넥션 풀        |
| `Event`                        | 플래그 하나로 여러 스레드에 신호     | 종료 신호, 초기화 완료 신호               |
| `Barrier`                      | N개 스레드가 모두 도착하면 동시 출발 | 동시성 테스트 코드                        |
| `queue.Queue`                  | 스레드 안전 큐(내부에 락 내장)       | 작업 큐, 워커 풀                          |

### 2.1 Lock vs RLock

```python
lock = threading.Lock()

def a():
    with lock:
        b() # b도 락을 잡으려고 함

def b():
    with lock: # Lock이면 자기 자신을 기다리며 영원히 멈춤(self-deadlock)
        ...

```

- `RLock`은 Re-entrant Lock으로 재진입 가능한 락. 한 스레드가 자기 자신이 이미 보유한 락을 중복해서 획득할 수 있음
- 동작 방식
  1. RLock은 내부적으로 "락을 소유한 스레드"와 "획득횟수(Recursion level)"를 기록함.
  2. 어떤 스레드가 rlock.acquire() 를 처음 호출하면, 해당 스레드가 락의 소유자가 되고 획득 횟수는 1이 됨.
  3. 동일한 스레드가 acquire()를 다시 호출하면, blocking되지 않고 획득 횟수만 1 증가함.
  4. 다른 스레드가 acquire()를 호출하면, 기존 `Lock`과 같이 블로킹됨
  5. 락을 획득한 스레드는 `release()`를 호출할 때마다 획득 횟수가 1 감소하며, 획득 횟수가 0이 되어야만 락이 완전히 해제되어 다른 스레드가 획득할 수 있음.

`RLock`은 "누가 몇 번 잡았는지"를 기억해서, 같은 스레드면 다시 들어갈 수 있고 잡은 횟수만큼 풀어야 해제됨.

- `RLock`은 편하지만 락 구조가 꼬였다는 신호일 수 있어서, 가능하면 락을 잡는 public 메서드와 락 없이 동작하는 private `_unlocked` 메서드로 분리하는 편을 선호한다.

```python
class Service:
    def __init__(self):
        self._lock = threading.lock()

    def withdraw(self, aid, amt):
        with self._lock:
            self._withdraw_unlocked(aid, amt)

    def bulk_withdraw(self, items):
        with self._lock:
            for aid, amt in items:
                self._withdraw_unlocked(aid, amt)

    def _withdraw_unlocked(self, ait, amt):
        ... # 호출자가 락을 잡고 있다고 가정
```

1. 락의 본질적인 목적은 단순히 코드를 줄 세우는 것이 아니라, **연산 도중의 불완전한 상태의 데이터를 다른 스레드에게 절대 보여주지 않는 것(불변식 보장)** 임.

- 만약 `RLock`을 쓰고 메서드들이 서로 복잡하게 얽혀서 호출한다고 가정하면,
  - A 함수가 데이터 수정을 50%만 해둔 불완전한 상태에서,
  - B 함수를 호출하고, B 함수가 또 RLock을 잡고...
  - 중간에 예외(Error)가 발생하면?
- 개발자는 도대체 락이 정확히 어느 시점에 완전히 해제(Count 가 0이 됨)되어 다른 스레드에게 데이터가 공개되는가? 를 머릿속으로 추적하기가 어려움

2. 원자적 단위의 범위가 명확해짐
   [예시: RLock을 믿고 그냥 호출할 때]

```python
# RLock을 썼다고 가정
def withdraw(self, aid, amt):
    with self._rlock:   # 매번 락을 잡았다 풂
        ...

def bulk_withdraw(self, items):
    for aid, amt in items:
        self.withdraw(aid, amt) # 1번 출금(락 풀림) -> 2번 출금(락 풀림) -> ...


```

    - 이러면 1번 계좌 출금하고 락이 풀린 찰나의 순간에 다른 스레드가 끼어 들어 계좌 잔액을 바꿔 버릴 수 있음. 즉, "10개의 계좌에서 한 번에 돈을 빼낸다"는 전체 작업의 원자성이 깨짐

[예시: 분리 패턴을 쓸 때]

```python
def bulk_withdraw(self, items):
    with self._lock: # 1. 문을 한 번 잠그고
        for aid, amt in items:
            self._withdraw_unlocked(aid, amt) # 2. 내부 로직들을 방해 없이 연속 실행
        # 3. 10개 다 끝난 뒤에 문을 열어줌
```

    - 락을 잡는 책임(`with self._lock`)을 바깥에 두고, 순수 작업(`_unlocked`)을 분리했기 때문에 "어디서부터 어디까지가 한 묶음인지" 코드 구조 상 명확해짐.

3. 코드 악취(Code smell)

- 한 스레드가 이미 잡은 락을 또 잡아야 하는 상황이 발생했다는 것은, 사실 객체 설계나 책임 분리가 잘못되었다는 경고 신호임.

4. 사소하지만 성능 문제(Overhead)

- 일반 `Lock`: "잠겼다/열렸다"만 체크하는 C언어 수준의 매우 가벼운 뮤텍스(Mutex)
- `RLock`: "현재 이 락을 잡은 스레드 ID가 누구인가?", "몇 번이나 중첩해서 들어왔는가(Counter)?"를 매번 조회하고 연산해야 함

### 2.2 타임아웃이 있는 acquire

```python
if not lock.acquire(timeout=1.0):
    raise TimeoutError("lock busy")
try:
    ...
finally:
    lock.release() # 작업 도중 에러가 나더라도 finally가 실행되어 잡았던 락을 반드시 풀어줌(release).


```

- 일반적인 `lock.acquire()`나 `with lock:`은 타임아웃이 없음(무한 대기)
- 만약 어떤 스레드가 락을 쥐고 있는 상태에서 버그로 무한 루프에 빠지거나 데드락에 걸리면, 그 뒤에 줄 서 있는 모든 스레드들도 프로그램이 종료될 때까지 영원히 멈춰(Hang) 버림
- 시스템 완전 마비 방지: 락을 못 잡아도 최소한 에러를 띄우고 다른 작업(예: "잠시 후 다시 시도해주세요" 사용자 응답)을 처리할 수 있게 함
- 데드락 조기 발견: 어디선가 락이 안풀리고 있다는 것을 타임아웃 에러 로그를 통해서 바로 인지할 수 있음

### 2.3 Condition: "조건이 될 때까지 기다리기"

```python
class BoundedBuffer:
    def __init__(self, capacity):
        self._items = []
        self._cap = capacity
        self._cond = threading.Condition()

    def push(self, item):
        with self._cond:
            while len(self._items) >= self._cap: # if가 아니라 while! (spurious wakeup 대비)
                self._cond.wait()
            self._items.append(item)
            self._cond.notify_all()

    def get(self):
        with self._cond:
            while not self._items:
                self.cond_wait()
            item = self._items.pop(0)
            self._cond.notify_all()
            return item

```

> 실전에서는 이걸 직접 짜기보다 `queue.Queue(maxsize=N)`을 쓰는 게 정답이고, "직접 구현하면 이렇게 된다"는 걸 알고 있으면 충분합니다. `wait()`을 `while`로 감싸는 이유는 꼭 설명할 수 있어야 한다.

- Condition은 "락 + 신호등(대기실)"로 내부에 Lock을 품고 있음
- Condition 객체를 만들 때 아무 인자도 안 주면(`threading.Condition()`), 파이썬은 내부적으로 `RLock`을 하나 자동으로 생성해서 품고 있음.
- 일반 Lock: "내가 일할 동안 아무도 들어오지 마!" (상호 배제만 가능)
- Condition: "내가 들어오긴 했는데 ... 내가 원하는 상황(버퍼에 자리가 생김 등)이 아니네? 락을 잠시 내려놓고 저기 대기실 구석에서 자고 있을게. 상황이 바뀌면 깨워줘"가 가능함.

`with self._cond:` 와 `wait()`의 동작 원리

1. `with self._cond:`: 락을 획득하고 들어감
2. `self._cond.wait()`을 호출하는 순간, 파이썬 내부에서는
   - 잡고 있던 락을 풀어서 다른 스레드에게 양보함. (그래야 `get` 스레드가 들어와서 아이템을 빼가고 자리를 만들어 줄 수 있음)
   - 그리고 자신은 잠시 잠에 빠져 대기 상태가 됨.
3. 다른 스레드가 `notify_all()`로 깨워주면,
   - 잠에서 깨어나자마자 다시 락을 획득하려고 경쟁함.
   - 락을 다시 쥐는 데 성공해야 비로소 `wait()` 다음 줄로 넘어감.

#### 왜 `if` 가 아니라 `while`을 써야 하는가?

[버퍼 용량이 1개(`capacity=`)인 상태의 시나리오]
현재 버퍼가 꽉 차 있음: `len(_items) == 1`

1. 스레드 A (Push 하러 옴): `if len >= cap:` 조건이 참이므로 `wait()`를 호출하고 잠듬 (대기실로 감)
2. 스레드 B (Push 하러 옴): 얘도 조건이 참이라 `wait()`를 호출하고 잠듬 (대기실로 감)
3. 스레드 C (Get 하러 옴): 아이템을 하나 꺼내서 버퍼가 빔(`len == 0`). 그리고 `notify_all()`을 외쳐서 대기실의 A와 B를 깨움
4. 문제 발생
   - 스레드 A가 먼저 재빨리 락을 잡고 깨어남
   - 만약 `if`문이었다면: 이미 조건을 통과했다고 생각하고 바로 다음 줄로 넘어가서 아이템을 넣음. 이제 버퍼는 다시 꽉 참(`len == 1`)
   - A가 작업을 끝내고 락을 놓자, 스레드 B가 다음 차례로 락을 잡음.
   - 만약 `if`문이었다면: 스레드 B도 자기가 자다 깬 지점부터 그냥 실행해버림. 이미 A가 채워놔서 자리가 없는데도 불구하고 또 아이템을 밀어 넣음(`append`)
   - 결과: 버퍼 용량이 1개인데 2개가 들어가며 불변식이 깨짐
5. `while`을 쓰면 스레드 B가 잠에서 깨어났을 때, 곧바로 다음 코드로 가는 게 아니라 루프를 다시 돌며 조건을 한 번 더 검사하므로 스레드 B는 다시 `wait()`로 들어가 대기실로 감.

#### Spurious Wakeup 문제

아무도 깨우지 않았는데(심지어 OS 수준의 이유 없는 신호로 인해) 스레드가 혼자 갑자기 잠에서 깨어나는 현상을 말함
OS와 하드웨어 설계상 극히 드물게 발생할 수 있는데, 이때 `while`문으로 조건을 다시 검사하게 해 두지 않으면, 아무런 조건도 충족되지 않았는데 혼자서 깨어나서 엉뚱한 코드를 실행하게 됨.
