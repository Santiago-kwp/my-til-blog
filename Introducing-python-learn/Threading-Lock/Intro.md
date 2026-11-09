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

### 2.4 Semaphore: 동시 실행 개수 제한

> 세마포어를 비유적으로 설명한다면 **열쇠가 여러 개 걸려있는 화장실**


```python
api_slots = threading.BoundedSemaphore(3)

def call_external_api(x):
    with api_slots:     # 최대 3개 스레드만 동시에 진입
        return requests.get(...)
```

- 일반 락(Lock):
    - 화장실 칸이 딱 1개
    - 열쇠도 1개뿐이라, 오직 1명만 들어갈 수 있음
- 세마포어(Semaphore):
    - 화장실 칸이 3개
    - 벽에 걸린 열쇠도 3개
    - 사람이 올 때마다 열쇠를 하나씩 집어 들고 들어감 (남은 열쇠: 3 $\rarr$ 2 $\rarr$ 1 $\rarr$ 0 )
    - 열쇠가 0개가 되면, 4번째 사람부터는 **앞사람이 나와서 열쇠를 걸어둘 때까지 줄을 서서 기다려야(대기) 함**
    - 안에서 볼일을 다 본 사람이 나와서 열쇠를 제자리에 걸어두면(`release`), 기다리던 다른 사람이 그 열쇠를 쥐고 들어감

#### 세마포어를 왜 쓰는가?

스레드를 쓰면 네트워크 요청이나 파일 다운로드 같은 I/O 작업을 빠르게 처리할 수 있음. 하지만, 스레드를 여러 개 띄워서 외부 API를 동시에 여러 번 호출하는 경우 다음과 같은 문제가 생길 수 있다.

1. 상대방 서버의 차단 (DDoS 오인 / Rate Limit):
외부 서버(OpenAI, 구글, 결제사 등)에 1초에 1,000개의 요청을 쏟아부으면, 상대 서버는 디도스 공격으로 간주하고 우리 IP를 차단하거나 `429 Too Many Requests` 에러를 냄
2. 소켓 및 메모리 고갈
컴퓨터가 한 번에 열 수 있는 네트워크 연결(Socket) 수와 메모리에는 한계가 있어서 우리 서버 자체가 뻗어버림
3. DB 커넥션 풀 고사
DB는 보통 동시에 붙을 수 있는 최대 연결 수(예: 20 ~ 30개)가 정해져 있는데, 100개의 스레드가 동시에 쿼리를 날리면 DB 커넥션 에러를 내며 멈춤

> 이때 세마포어를 쓰면 **스레드는 100개, 1000개를 자유롭게 띄우되, 실제로 병목이 생기는 위험 구간(임계 자원)에는 딱 N개씩만 순서대로 들어가라** 고 안전 밸브를 달아줄 수 있다.

#### 세마포어 활용 사례

1. 외부 API 호출 속도 조절(Rate Limiting)

```python
api_slots = threading.BoundedSemaphore(5) # 무료 티어라 초당 최대 5개 동시 호출만 지원

def fetch_data(url):
    with api_slots: # 6 번째 스레드는 앞선 5개 중 하나가 끝날 때까지 얌전히 대기
        return requests.get(url)
```

2. 웹 스크래핑/크롤러 (타겟 사이트 부하 방지)

수 만 개의 웹페이지를 긁어와야 할 때, 너무 빠르게 긁으면 타겟 서버가 마비되거나 내 IP가 밴(Ban)당함. 동시 접속자수를 3~5명 수준으로 제한할 때 씀

3. 제한된 리소스 풀(Pool) 접근 관리
- 회사 내부의 GPU 머신이 2장밖에 없을 때: `BoundedSemaphore(2)`로 감싸서 최대 2개의 학습 스레드만 GPU를 점유하도록 제어
- 라이선스가 3개뿐인 고가의 상용 소프트웨어를 호출 할 때: `BoundedSemaphore(3)` 적용

4. 대용량 파일 다운로더
100개의 파일을 받아야 하는데 100개를 동시에 받으면 네트워크 대역폭이 쪼개져서 전체가 다 느려짐. 세마포어로 3~4개씩 끊어서 안정적으로 다운로드할 때 유용

#### Semaphore vs BoundedSemaphore

- 일반 `Semaphore`: 실수로 `release()`를 집어간 횟수보다 더 많이 호출하면, 원래 3개였던 열쇠가 4개, 5개로 영구히 불어나 버리는 심각한 버그가 생김
- `BoundedSemaphore`: 처음에 정해준 최대치(3개)보다 더 많이 `release()`하려고 하면 `ValueError` 예외 발생시켜 버그를 잡을 수 있음.



## 3. 세분화된 락
```python
import threading
from dataclasses import dataclass, field

class InsufficientFunds(Exception):
    raise ValueError

class AccountNotFound(Exception):
    raise KeyError



@dataclass
class Account:
    id: str
    balance: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

class BankService:
    def __init__(self):
        self._accounts: dict[str, Account] = {}
        self._registry_lock = threading.Lock() # 계좌 "목록" 보호용

    # 계좌 생성
    def create(self, aid: str, initial: int = 0) -> None:
        with self._registry_lock:
            if aid in self._accounts:
                raise ValueError("duplicate")
            self._accounts[aid] = Account(aid, initial)

    # 계좌 조회
    def _get(self, aid: str) -> Account:
        acc = self._accounts.get(aid)
        if acc is None:
            raise AccountNotFound(aid)
        return acc

    # 계좌 출금
    def withdraw(self, aid: str, amount:int) -> None:
        acc = self._get(aid)
        with acc.lock:  # 이 계좌만 잠금
            if acc.balance < amount:
                raise InsufficientFunds(aid)
            acc.balance -= amount

    # 계좌 이체
    def transfer(self, src: str, dest: str, amount:int) -> None:
        if src == dst:
            raise ValueError("same amount")
        
        a = self._get(src)
        b = self.get(dest)

        # 교착 상태 방지: 항상 같은 순서(id 오름차순)로 락 획득
        first, second = sorted((a, b), key=lambda x: x.id)
        with fisrt.lock, second.lock:
            if a.balance < amount:
                raise InsufficientFunds(aid)
            a.balance -= amount
            b.balance += amount


```

### 정렬을 안하면 생기는 일(교착상태):
- 스레드 1: transfer(A->B) A락 획득 -> B락 대기 ...
- 스레드 2: transfer(B->A) B락 획득 -> A락 대기 ...
- 서로 상대가 가진 락을 영원히 기다림
- 교착상태 4가지 필요조건 : 상호배제, 점유와 대기, 비선점, 순환대기. 
- 락 순서 정렬은 순환 대기를 깨는 방법
- `acqure(timeout=...)` 후 포기하고 재시도하는 건 점유와 대기를 깨는 방법

### 사용자 ID 같은 임의 키별 락이 필요할 때

#### 왜 필요한가?
> 만약 전 세계 유저가 1,000만 명인데, `user_service_lock = threading.Lock()` 하나로 모든 유저의 요청을 처리한다고 가정하자

- `user_1`이 닉네임을 변경하는 0.1초 동안, 지구 반대편에 있는 아무 상관없는 `user_9999`는 프로필 사진도 못 바꾸고 대기해야 함. 전체 서비스 처리량(Throughput)이 바닥을 침
- 그렇다고 락을 아예 안 걸면, `user_1`이 동시에 폰과 PC에서 결제 버튼을 눌렀을 때 중복 결제(Race condition)가 발생함.
- 즉, 서로 다른 사용자(키)끼리는 동시에 병렬 처리되어야 하지만, '같은 사용자(키)'에 대한 동시 요청은 줄을 세워야 한다.

사용 사례
1. 중복 결제/주문 방지: 동일 유저(`user_id`)가 따닥(더블 클릭)을 눌렀을 때 혹은 다른 PC나 다른 기기로 로그인 후 동시에 결제 버튼을 눌렀을 때 1번만 결제되도록 할 때
2. 좌석 예매 시스템: 좌석 번호(`seat_id`)별로 락을 걸어, A구역 1번을 예매하는 사람과 B구역 5번을 예매하는 사람은 서로 방해받지 않게 할 때.
3. 캐시 스탬피드(Cache Stampede) 방지: 여러 스레드가 동시에 캐시가 만료된 특정 상품(`item_id`)을 조회할 때, 딱 1개 스레드만 DB에 다녀와서 캐시를 채우고 나머지는 기다리게 할 때.
    (※ 서버가 여러 대인 분산 환경에서는 이를 `threading.Lock` 대신 `Redis 분산 락`으로 키별 락을 구현합니다.)

```python
from collections import defaultdict

class KeyedLocks:
    def __init__(self):
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)
        self._gaurd = threading.Lock() # 락 딕셔너리 자체도 공유 상태다

    def get(self, key: str) -> threading.Lock:
        with self._guard:
            return self._locks[key]
```

- "락을 담는 dict도 동시에 수정되니 그걸 보호하는 락이 또 필요하다"
- 이러면 유저가 만약 1억 명이 접속할 때마다 `_locks` 딕셔너리에 락 객체가 1억 개나 생성된다.
- 한 번 가입하고 다신 안 오는 탈퇴 회원용 락까지 메모리에 영원히 남아 **메모리 누수(OOM, Out Of Memory)** 가 난다.
- 그리고 "키가 무한히 늘면 메모리 누수 -> 고정 개수 버킷으로 해싱하는 lock striping(`locks[hash(key) % N]`)으로 해결 가능하다.

#### Lock Striping (락 스트라이핑)
> 핵심 아이디어: 유저가 1억명이어도, 락은 딱 64개만 미리 만들어 두고 나눠 쓰자!

1. 서버가 뜰 때 고정된 크기(예: 64개)의 락 리스트(버킷)을 만듦

```python
NUM_BUCKETS = 64
self._buckets = [threading.Lock() for _ in range(NUM_BUCKETS)]
```

2. 사용자 ID(`key`)가 들어오면, 파이썬 내장 해시 함수를 돌려 `0 ~ 63` 사이의 숫자로 변환함
```python
bucket_index = hash(key) % NUM_BUCKETS
lock_to_use = self._buckets[bucket_index]
```

3. 그 인덱스에 해당하는 락을 꺼내서 씀
```
[유저 ID]                 [해시 계산]            [64개의 락 버킷]
"user_alice"   -->  hash() % 64 = 12   -->  _buckets[12] 락 사용
"user_bob"     -->  hash() % 64 = 45   -->  _buckets[45] 락 사용
"user_charlie" -->  hash() % 64 = 12   -->  _buckets[12] 락 사용 (우연히 겹침)
```

- 장점: 메모리 완벽 통제 가능 - 유저가 1명이어도, 10억 명이어도, 메모리에는 정확히 64개의 Lock 객체만 존재하므로 메모리 누수가 100% 방지됨.
- 단점: 해시 충돌: 아주 낮은 확률로 위와 같이 `alice`와 `charlie`가 우연히 같은 12번 락을 배정받을 수 있음. 하지만 64개 정도로 쪼개두면 충돌 확률이 낮아서, 단일 락을 쓸 때보다 동시 처리 성능이 수십 배 향상됨. (Java의 고성능 `ConcurrentHashMap`도 내부적으로 이 방식을 씀)

## 4. 읽기-쓰기 락 (RW Lock)
파이썬 표준 라이브러리에는 RW 락이 없어서, `Condition`으로 직접 만들 수도 있다.

```python
class RWLock:
    def __init__(self):
        self._cond = threading.Condition()
        self._readers = 0       # 현재 데이터를 읽고 있는 스레드의 수(카운터)
        self._writer = False    # 현재 데이터를 쓰고 있는 스레드가 있는지 여부(T/F)

    @contextmanager
    def read(self):
        with self._cond:
            while self._writer:
                self._cond.wait() # 누가 쓰고 있으면 대기
            self._readers += 1  # 누가 쓰고 있지만 않으면, 10명이든 1,000명이든 그냥 통과 (동시 읽기 허용)
        try:
            yield   # 읽기 수행
        finally:
            with self._cond:
                self._readers -= 1
                if self._readers == 0: # 마지막으로 나가는 읽기 스레드라면 기다리고 있을 쓰기 스레드 깨우기
                    self._cond.notify_all()

    @contextmanager
    def write(self):
        with self._cond:
            while self._writer or self._readers > 0: # 아무도 쓰지 않고, 읽지 않아야 들어갈 수 있음
                self._cond.wait()
            self._writer = True # 문 잠그기
        try:
            yield # 데이터 쓰기
        finally:
            with self._cond:
                self._writer = False # 다 썼으면 문 열고 밖에서 기다리던 읽기/쓰기 스레드에게 노티
                self._cond.notify_all()

# 사용
rw = RWLock()
with rw.read(): ... # 여러 스레드 동시 진입 가능
with rw.write(): ... # 단독 진입
```

### 한계
- 위의 구현은 읽기 선호라 읽기가 계속 들어오면 쓰기가 영원히 못 들어가는 writer starvation이 생길 수 있음
- 해결 방안은 "대기 중인 writer가 있으면 새 reader를 막는" 방식
- 파이썬에서는 GIL 때문에 읽기 병렬화 이득이 작아서, 실제로는 측정 후 도입하는게 좋음

### 해결책: 공평한 RWLock (Fair RWLock / Writer-preference)
- writer starvation을 해결하려면 **"대기실에서 기다리고 있는 Writer가 몇 명인지"** 를 세는 변수(`self._waiting_writers`)를 추가해야 함.

```python
# read() 의 진입 조건을 다음과 같이 바꾼다.
while self._writer or self._waiting_writers > 0:
    self._cond.wait()
```

- 이렇게 하면, 누군가 쓰려고 대기실에 줄을 서는 순간 뒤이어 도착하는 신규 Reader들의 진입을 차단하여, 기존 Reader들이 다 빠져나간 뒤 Writer가 우선적으로 들어갈 수 있게 보장해줌.

### 파이썬의 한계
- C++나 Java에서는 `RWLock`을 쓰면 성능이 많이 올라감. 왜냐하면 CPU 코어 8개가 진짜로 동시에 데이터를 읽기 때문
- 하지만 파이썬(CPython with GIL)은 다름.
    - `RWLock`으로 스레드 100개가 동시에 `read()` 구간에 들어갔다고 치자.
    - 하지만 GIL(Global Interpreter Lock) 때문에, 물리적인 CPU 코어에서는 여전히 바이트코드가 한 번에 딱 1스레드만 돌아감
    - 즉, 진정한 의미의 "동시 병렬 CPU 읽기"가 발생하지 않음
    - 오히려 `Condition`, `wait()`, `notify_all()`을 거치면서 **컨텍스트 스위칭 오버헤드**가 그냥 일반 `Lock()` 1개 썼을 때보다 더 커져서 시스템이 더 느려질 수도 있음
- Python 3.13부터 GIL을 없애는 Free-threaded 빌드가 도입되면 C++/Java 처럼 Python도 멀티코어를 100% 활용할 수는 있음


### 언제 써야할까?
1. 읽기 작업 내부에서 GIL이 풀릴 때:
    - 읽는 로직이 순수 파이썬 계산이 아니라, C 확장 모듈(Numpy, Pandas, 암호화 연산 등)을 호출하거나 I/O(네트워크/디스크 읽기) 작업이라서 GIL을 스스로 내려놓을 때 (이때는 진짜 멀티코어로 병렬 읽기가 됨)
2. 읽는 시간이 엄청나게 길 때:
    - 읽는 작업 한 번에 1초씩 걸린다면, 일반 `Lock`을 썼을 때 다른 읽기 스레드들이 1초씩 밀리게 됨. 이럴 때는 GIL 오버헤드를 감수하더라도 `RWLock`으로 동시에 진입시키는게 나음,.
