# 파이썬 namespace 와 scope

> - 원문 정리: [참조-티스토리](https://yomangstartup.tistory.com/112)
> - 개정일: 2026-11-17 / 현재 안정 버전: **Python 3.15** (2026-10-09 출시)
> - 예제는 3.12.13 · 3.13.18 · 3.14.6 · 3.15.0b4 에서 직접 실행해 확인함 (3.11.18은 traceback 비교에만 사용, 3.15 전용 문법은 3.15.0b4 기준)


---

## 0. 한눈에 보기

| 개념 | 한 줄 정의 |
|---|---|
| name | 객체를 가리키는 이름 (변수·함수·클래스·모듈 이름) |
| object | 메모리에 올라간 데이터 또는 코드 |
| namespace | name → object **매핑** (이름표 보관소) |
| scope | namespace를 이름만으로 바로 찾을 수 있는 **코드상의 영역** |
| LEGB | 이름 탐색 순서: Local → Enclosing → Global → Built-in |

- 대입(`=`, `import`, `def`, `class` 등)은 `global`/`nonlocal` 선언이 없으면 항상 **가장 안쪽 scope**에 이름을 만든다.
- scope는 코드 모양(텍스트)으로 **정적으로 결정**되고, 이름 탐색은 **실행 중에** 일어난다.
- namespace는 대부분 dict로 구현되지만 **함수의 local은 dict가 아니다**.

---

## 1. 기본 개념: name, object, binding

- name은 object의 reference(참조)다. `=` 는 값을 복사하는 게 아니라 **이름을 객체에 묶는(binding) 것**이다.
- 하나의 객체에 이름이 여러 개 붙을 수 있다 (aliasing).
- 이름을 만드는(바인딩하는) 구문: 대입, 함수 매개변수, `def`, `class`, `import`, `for` 루프 변수, `with ... as`, `except ... as`, `:=` 등.

```python
a = [1, 2]
b = a                 # 복사가 아니라 같은 객체에 이름을 하나 더 붙임
b.append(3)
print(a, a is b)      # [1, 2, 3] True
```

---

## 2. namespace

### 2.1 정의

- 공식 문서 정의: "A namespace is a mapping from names to objects."
- **서로 다른 namespace에 있는 같은 이름은 아무 관계가 없다.** 두 모듈이 모두 `maximize` 함수를 정의해도 `mod1.maximize`, `mod2.maximize` 로 구분되어 충돌하지 않는다.
- 객체의 attribute 집합도 하나의 namespace다. (`z.real` 에서 `real` 은 `z` 의 attribute)

### 2.2 종류와 생명주기

| 종류 | 들어있는 것 | 생성 시점 | 소멸 시점 | 확인 방법 |
|---|---|---|---|---|
| built-in | `print`, `len`, `Exception` 등 내장 이름 | 인터프리터 시작 | 삭제되지 않음 (종료 시까지) | `dir(builtins)` |
| global (module) | 모듈 최상위에서 만든 이름 | 모듈이 처음 import(또는 실행)될 때 | 보통 인터프리터 종료 시까지 | `globals()` |
| local (function) | 매개변수와 함수 안에서 만든 이름 | 함수가 **호출될 때** | 함수가 반환되거나 처리되지 않은 예외로 끝날 때 | `locals()` |
| class body | 클래스 본문에서 만든 이름 | 클래스 정의가 실행되는 동안 | 클래스 객체의 `__dict__`로 이어짐 | `vars(Cls)` |
| 객체 attribute | 인스턴스/모듈의 attribute | 객체 생성 시 | 객체 소멸 시 | `vars(obj)` |

- 재귀 함수는 **호출마다 독립된** local namespace를 가진다.
- 모듈은 한 번 import되면 `sys.modules` 에 캐시되어, 다시 import해도 코드가 재실행되지 않는다.
- 함수가 끝나도 안쪽 함수(클로저)가 참조하는 변수는 살아남는다. (3.5 참고)

```python
def rec(n):
    x = n * 10
    if n:
        rec(n - 1)
    print("n =", n, "x =", x)    # 호출마다 자기 x를 가지고 있음

rec(2)
# n = 0 x = 0
# n = 1 x = 10
# n = 2 x = 20
```

### 2.3 구현 방식

- 공식 문서(3.15 문서에도 그대로): "대부분의 namespace는 현재 파이썬 dict로 구현되어 있고, 성능 외에는 눈에 띄지 않으며, 앞으로 바뀔 수 있다."
- **dict 기반**: global(module), built-in, class body, 객체 attribute
  - 모듈의 namespace는 `module.__dict__`, 클래스의 `__dict__`는 읽기 전용 뷰(`mappingproxy`)로 보인다.
- **dict가 아닌 것**: 함수의 local 변수
  - 어떤 이름이 local인지는 **컴파일 시점에 정해지고**, 실행 중에는 프레임 안의 배열(fast locals)에 저장된다.
  - `locals()` 는 필요할 때 이 배열에서 **만들어 주는 사본**이다.

```python
g = 1

def f():
    a = 1
    return a + g

print(f.__code__.co_varnames)    # ('a',)  ← 컴파일 때 정해진 local 이름
print("a" in globals())          # False   ← 함수의 local은 globals()에 없다
```

### 2.4 사용법

- name(key)으로 접근하고, 객체의 attribute/method는 `.`(점)으로 접근한다.
- 모듈의 attribute와 모듈의 global 이름은 **같은 namespace**다.

```python
import math

print(math.pi)                          # math 모듈의 namespace에서 'pi' 찾기
print(math.__dict__["pi"] == math.pi)   # True

z = 3 + 4j
print(z.real, z.imag)                   # 3.0 4.0  ← 객체 z의 attribute
```

### 2.5 `globals()` 로 namespace 확인하기

```pycon
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__builtins__': <module 'builtins' (built-in)>}
>>> import dis
>>> globals()
{..., 'dis': <module 'dis' from '.../lib/python3.14/dis.py'>}
>>> def test():
...     a = 3
...     print(a)
...
>>> globals()
{..., 'dis': <module ...>, 'test': <function test at 0x...>}
```

- `import dis` 를 하면 key `'dis'`, value **모듈 객체**가 global namespace에 추가된다.
- `def test()` 를 실행하면 key `'test'`, value 함수 객체가 추가된다.
- 출력되는 `__loader__` 등은 실행 환경(REPL/스크립트/IDE 콘솔)과 버전에 따라 다르다. 스크립트로 실행한 `__main__`의 `globals()` 키는 다음처럼 달라진다. (직접 실행한 결과)

| 버전 | 스크립트 실행 시 `__` 로 시작하는 키 |
|---|---|
| 3.13 이하 (3.11~3.13 확인) | `__annotations__`, `__builtins__`, `__cached__`, `__doc__`, `__file__`, `__loader__`, `__name__`, `__package__`, `__spec__` |
| 3.14 | 위에서 `__annotations__` 가 없음 |
| 3.15 | 3.14에서 `__cached__` 도 없음 (3.15 What's New: import 시스템이 `__cached__` 를 더 이상 설정하지 않음. 대신 `__spec__.cached`) |

### 2.6 `__name__` 과 `__main__`

- 모든 모듈은 자기 namespace에 **자기 이름의 `__name__`** 을 가진다.
- 파이썬이 처음 실행하는 최상위 코드는 `__main__` 이라는 이름의 모듈로 취급되고, 이 모듈이 **자기만의 global namespace**를 가진다. (`python test.py`, `python -m pkg`, 대화형 모드 모두 해당)
  - import되는 모듈은 import될 때 자기 `__name__` 을 받는다.
- 그래서 "직접 실행될 때만" 실행되는 코드를 구분할 수 있다.

```python
# mod_a.py
print("이 파일의 __name__ =", __name__)

if __name__ == "__main__":
    print("직접 실행됨")
```

```text
$ python mod_a.py
이 파일의 __name__ = __main__
직접 실행됨

$ python -c "import mod_a"
이 파일의 __name__ = mod_a
```

### 2.7 built-in namespace 와 `builtins` 모듈

- built-in namespace는 global namespace **안에 저장되는 게 아니라 별도의 namespace**다. 이름을 찾을 때 global 다음 마지막 순서로 조회될 뿐이다.
- 내장 이름들은 **`builtins`** 모듈에 들어 있다. (Python 3 이름)
- `globals()` 안에 보이는 `'__builtins__'` 는 CPython의 구현 세부사항이다. `__main__` 에서는 `builtins` 모듈 자체이고, import된 모듈에서는 그 모듈의 dict다. 공식 문서도 건드리지 말고, 필요하면 `import builtins` 를 쓰라고 한다.

```python
import builtins

print(builtins.len is len)        # True
builtins.print("builtins.print 로도 호출 가능")

# import __builtin__             # ModuleNotFoundError (Python 2 이름)
```

### 2.8 함수 호출로 보는 namespace의 생성과 소멸

```python
def local_test():
    a = 3
    print(a)

local_test()
# 3
```

1. 인터프리터가 시작되면 built-in namespace가 만들어진다 (`print`, `len` …).
2. `__main__` 모듈의 global namespace가 만들어진다.
3. `def local_test()` 를 만나면 함수 객체를 만들고 global namespace에 `'local_test'` 를 등록한다.
4. `local_test()` 를 호출하면 이 호출을 위한 실행 환경(프레임)과 **local namespace**가 만들어진다.
5. `a = 3` → local namespace에 `a` 가 등록된다.
6. `print(a)` 를 실행하면서 이름을 찾는다.
   - `a` : local에서 발견
   - `print` : local → (enclosing 없음) → global → **built-in** 에서 발견
7. `print` 는 C로 구현된 내장 함수라 파이썬 코드용 local namespace(프레임)가 따로 만들어지지 않는다.
8. 함수가 끝나면 `local_test` 의 local namespace가 사라진다.

```python
print(type(print).__name__, hasattr(print, "__code__"))   # builtin_function_or_method False
```

---

## 3. scope

> 원문 제목은 "namespaces 와 scopes" 인데 scope 내용이 없어서 새로 정리했다.

### 3.1 정의

- scope: "namespace를 **직접(이름만으로)** 접근할 수 있는 프로그램의 텍스트 영역"
- 관계: namespace는 **이름표 모음(데이터)**, scope는 **그걸 볼 수 있는 코드 영역**
- scope는 **코드가 쓰여진 위치로 정적으로 결정**된다. 함수를 어디서, 어떤 이름으로 호출하든 그 함수의 global scope는 **함수가 정의된 모듈**의 namespace다.
- 함수의 local 변수는 이미 정적으로 결정되지만, 이름 탐색 자체는 실행 중에 일어난다.

### 3.2 이름 탐색 순서: LEGB

| 순서 | 약자 | scope | 설명 |
|---|---|---|---|
| 1 | **L**ocal | 가장 안쪽 | 현재 함수의 local 이름 |
| 2 | **E**nclosing | 바깥 함수들 | 가까운 바깥 함수부터 차례로 |
| 3 | **G**lobal | 현재 모듈 | 모듈 최상위 이름 |
| 4 | **B**uilt-in | 내장 | `builtins` 의 이름 |

- 공식 문서는 "3개 또는 4개의 중첩된 scope"라고 설명한다. LEGB는 이를 외우기 위한 관용 약어다.
- 모듈 최상위(함수 밖)에서는 local scope = global scope다. (`locals() is globals()` 가 `True`)

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print("inner:", x)
    inner()
    print("outer:", x)

outer()
print("module:", x)
# inner: local
# outer: enclosing
# module: global
```

```python
def outer2():
    y = "enclosing"
    def inner():
        print(y, len("abc"))     # y: Enclosing 에서, len: Built-in 에서 발견
    inner()

outer2()    # enclosing 3
```

### 3.3 대입 규칙과 `UnboundLocalError`

- 대입, `del`, `import`, `def`, `class` 는 모두 **현재(가장 안쪽) scope에 이름을 만든다.** 데이터를 복사하지 않고 이름만 묶는다.
- 함수 안 **어디에든** 대입이 있으면 그 이름은 함수 **전체**에서 local이다. 대입 전에 읽으면 `UnboundLocalError` (`NameError`의 하위 클래스).
- 읽기만 하면 바깥 scope에서 찾는다.

```python
count = 0

def show():
    print(count)        # 읽기만 → Global 에서 찾음. OK

def inc():
    count += 1          # 대입이 있으니 count 는 inc 의 local → 읽는 시점에 값이 없음

try:
    inc()
except UnboundLocalError as e:
    print(type(e).__name__)     # UnboundLocalError
```

### 3.4 `global` 과 `nonlocal`

- `global x` : 이후 `x` 의 모든 참조·대입이 **모듈의 global namespace**로 간다. 아직 없는 이름이면 만들어진다.
- `nonlocal x` : 바깥 **함수**의 `x` 를 다시 바인딩한다. 바깥 함수에 이미 있는 이름만 가능하다.
- 선언이 없으면 바깥 변수는 **읽기 전용**이다. 쓰려고 하면 안쪽 scope에 같은 이름의 **새 local 변수**가 생긴다.

공식 문서의 예제 (출력 확인함):

```python
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)
# After local assignment: test spam
# After nonlocal assignment: nonlocal spam
# After global assignment: nonlocal spam
# In global scope: global spam
```

- `do_local` : `scope_test` 의 `spam` 을 바꾸지 못한다 (새 local 생성).
- `do_nonlocal` : `scope_test` 의 `spam` 을 바꾼다.
- `do_global` : 모듈 수준의 `spam` 을 새로 만든다. `scope_test` 의 `spam` 은 그대로다.

```python
# nonlocal 은 모듈 최상위 변수에는 쓸 수 없다
try:
    compile("zz = 1\ndef f():\n    nonlocal zz\n", "<demo>", "exec")
except SyntaxError as e:
    print(e.msg)        # no binding for nonlocal 'zz' found
```

### 3.5 클로저와 late binding

- 안쪽 함수는 바깥 변수의 **값**이 아니라 **변수(cell)** 를 참조한다. 그래서 바깥 함수가 끝난 뒤에도 값이 유지된다.
    - 컴파일할 때 "안쪽 함수가 이 변수를 쓴다"는 걸 알아채고, cell이라는 작은 상자에 따로 담음

```python
def make_counter():
    c = 0   # c 는 일반 local 칸이 아니라 cell(상자) 안에 들어감
    def inc():
        nonlocal c
        c += 1
        return c
    return inc

ctr = make_counter()
print(ctr(), ctr(), ctr())                        # 1 2 3
print(make_counter.__code__.co_cellvars)          # ('c',)
print(ctr.__code__.co_freevars)                   # ('c',)
print(ctr.__closure__[0].cell_contents)           # 3
```
1. `make_counter()`가 호출되면 프레임이 만들어지고 `c`의 cell(값0)이 생김.
2. `inc` 함수 객체가 만들어지면서 그 cell을 `inc.__closure__`에 저장함.
3. `return inc`로 `make_counter` 가 끝나면 프레임은 사라짐. 하지만 cell은 `inc`가 계속 쥐고 있어서 남음. 누군가 참조하는 객체는 지워지지 않음
4. `ctr()`을 부를 때마다 새 프레임이 만들어지지만, `c`는 프레임이 아니라 cell에서 읽고 씀. `c += 1`은 cell 안의 값을 바꾸므로 호출 사이에 값이 이어짐

```python
def outer():
    x = 1
    def inner():
        return x
    x = 2
    return inner

print(outer()()) # 2 
```
- 안쪽 함수는 만들어지는 순간의 값을 찍어 두지 않고, 상자를 쥐고 있다가 실행될 때 상자를 열어본다.
- 위와 같이 `inner`가 `x`라는 변수(상자)를 참조하기 때문에 `inner`가 실행될 때의 x를 열어보면 2가 된다.

---
- 하지만, 변수를 참조하므로 루프에서 만든 람다는 **호출 시점의 값**을 본다 (late binding).
    - 루프의 람다는 만들 때의 `i` 값이 아니라 **호출할 때 `i` 변수에 들어 있는 값** 을 읽는다. 루프 변수는 하나뿐이라 루프가 끝나면 모두 마지막 값을 본다.

```python
fs = [lambda: i for i in range(3)]

print(fs[0].__closure__[0] is fs[1].__closure__[0]) # True ← 세 람다가 같은 상자를 공유
print(fs[0].__closure__[0].cell_contents)           # 2 ← 루프가 끝난 뒤 상자 속 값
print([f() for f in fs])            # [2, 2, 2]  ← 모두 같은 i 를 봄

fs = [lambda i=i: i for i in range(3)]
print([f() for f in fs])            # [0, 1, 2]  ← 기본값으로 지금 값을 고정
```
시간 순서
| 시점 | 상자 `i` 속 값 | 일어나는 일 |
|---|---|---|
| 람다 0번 생성 | 0 | "i를 읽는 함수"를 만들었을 뿐, 0을 저장하지 않음 |
| 람다 1번 생성 | 1 | 마찬가지 |
| 람다 2번 생성 | 2 | 마찬가지 |
| 루프 종료 | 2 | 상자에 마지막 값이 남음 |
| `f()` 호출 | 2 | 세 람다가 모두 상자를 열어 2를 읽음 |

해결 방법: 상자를 따로 쓰게 만들기

**방법 1. 기본 인자로 값 고정**

```python
fs = [lambda i=i: i for i in range(3)]
print([f() for f in fs])      # [0, 1, 2]
print(fs[0].__defaults__)     # (0,)
print(fs[0].__closure__)      # None   ← 바깥 변수를 더 이상 참조하지 않음
```

- 기본값은 **함수를 만드는 순간** 평가되어 함수 객체에 저장됩니다. 
- 오른쪽 `i`는 그 순간의 값이고, 왼쪽 `i`는 람다 자신의 매개변수(local)입니다.
- 그래서 람다 안의 `i`는 바깥 변수가 아닌 자기 것입니다. 단 `f(100)`처럼 인자를 넘기면 덮어써지니(`100` 반환) 호출 방식을 아는 곳에서만 쓰는 게 좋습니다.

**방법 2. 함수를 한 번 더 호출해서 새 상자 만들기**

```python
def make(i):
    return lambda: i

fs = [make(i) for i in range(3)]
print([f() for f in fs])                                # [0, 1, 2]
print(fs[0].__closure__[0] is fs[1].__closure__[0])     # False  ← 각자 다른 상자
```

함수는 호출할 때마다 독립된 local namespace를 만든다는 2.2절의 성질을 이용한 방법입니다. `make(0)`, `make(1)`, `make(2)`가 각자 자기 `i` 상자를 만들어 람다에게 줍니다. 의도가 가장 분명해서 실무에서는 이쪽을 더 많이 씁니다.



|용어|의미|
|-|-|
|Frame|함수 호출 한 번에 대응되는 실행 환경(지역변수 저장소, 현재 실행 중인 위치, 호출한 함수 정보, 스택 정보 포함)|
|Cell|클로저 때문에 함수 종료 후에도 살아남아야 하는 변수를 담는 특별한 객체|
|Closure|함수 + 그 함수가 참조하는 cell들의 묶음|
|Late Binding|클로저가 값을 복사하는 것이 아니라 cell을 참조하기 때문에 나중 값이 보이는 현상|


### 3.6 클래스 scope의 특수 규칙

- 클래스 본문도 자기 namespace를 만들지만, **그 안의 메서드나 컴프리헨션 본문에서는 클래스 변수가 바로 보이지 않는다.** (enclosing scope로 취급되지 않음)
- 메서드에서는 `self.v` 또는 `클래스이름.v` 로 접근한다.
- 예외: 컴프리헨션의 **가장 바깥 iterable** 은 클래스 scope에서 평가된다.

```python
class A:
    v = 10
    def m(self):
        return v           # global 에서 찾으므로 NameError

try:
    A().m()
except NameError as e:
    print("method:", e)    # name 'v' is not defined

try:
    class B:
        v = 10
        w = [v + i for i in range(3)]     # 컴프리헨션 본문에서 v 가 안 보임
except NameError as e:
    print("comprehension:", e)            # name 'v' is not defined

class C:
    v = 10
    w = [i for i in range(v)]             # 컴프리헨션의 바깥 iterable(range(v))은 클래스 scope에서 평가 → OK
print(len(C.w))                           # 10
```

### 3.7 컴프리헨션 scope

- 컴프리헨션의 반복 변수는 **밖으로 새지 않는다** (Python 3).
- 단, 컴프리헨션 안의 **`:=`(walrus)는 바깥 scope에 바인딩**된다.

```python
y = "outer"
_ = [y for y in range(3)]
print(y)                    # outer  ← 바깥 y 는 그대로

try:
    [q for q in range(3)]
    print(q)
except NameError as e:
    print("NameError:", e)  # name 'q' is not defined

[(w := i) for i in range(3)]
print(w)                    # 2  ← walrus 는 바깥 scope 에 바인딩
```

- 3.12부터 구현이 바뀌었다 → 4.1 참고

### 3.8 built-in 이름 가리기(shadowing)

- built-in은 LEGB의 마지막이라, 같은 이름을 앞쪽 scope에서 만들면 **내장 이름이 가려진다.**
- `del` 로 가린 이름을 지우면 다시 내장 이름이 보인다.

```python
list = [1, 2]
try:
    list("abc")
except TypeError as e:
    print(e)                # 'list' object is not callable

del list
print(list("abc"))          # ['a', 'b', 'c']
```

---

## 4. 버전별 변경점

3.9 이후, namespace/scope에 영향을 준 변경들이다.

| 버전 | 변경 | 한 줄 요약 |
|---|---|---|
| 3.12 | PEP 709 | 컴프리헨션 인라인화 (별도 프레임 없음, scope 격리는 유지) |
| 3.12 | PEP 695 | 타입 파라미터 문법(`def f[T]`, `class C[T]`, `type X = ...`)과 annotation scope |
| 3.13 | PEP 667 | `locals()` / `frame.f_locals` 의미 확정 (스냅샷 vs write-through 프록시) |
| 3.14 | PEP 649 / 749 | 어노테이션 지연 평가, annotation scope 확대, `annotationlib` |
| 3.15 | PEP 810 | `lazy import` (namespace에 지연 프록시 객체가 들어감) |
| 3.15 | 기타 | `__cached__` 설정 중단, `types.FrameLocalsProxyType`, built-in `frozendict` · `sentinel` 추가 |

### 4.1 3.12 · 컴프리헨션 인라인화 (PEP 709)

- 3.11까지: list/dict/set 컴프리헨션이 **보이지 않는 중첩 함수**로 실행되었다.
- 3.12부터: 바깥 함수의 프레임에서 **인라인**으로 실행된다. 반복 변수의 격리(scope 분리)는 그대로이고, 함수 호출 비용만 없어졌다.
- 눈에 보이는 차이: traceback에서 `<listcomp>` 프레임이 사라졌다.

```python
import sys, traceback

def f():
    return [1 / 0 for _ in range(1)]

try:
    f()
except ZeroDivisionError:
    print([fs.name for fs in traceback.extract_tb(sys.exc_info()[2])])
# 3.11 : ['<module>', 'f', '<listcomp>']
# 3.12+: ['<module>', 'f']
```

- 3.6의 클래스 scope 규칙(컴프리헨션 본문에서 클래스 변수 안 보임)은 3.12 이후에도 그대로다. (3.11~3.15에서 모두 `NameError` 확인)

### 4.2 3.12 · 타입 파라미터와 annotation scope (PEP 695)

- `def f[T]`, `class C[T]`, `type X = ...` 는 **annotation scope**라는 새 종류의 scope를 만든다. 함수 scope와 비슷하지만 **둘러싼 클래스의 namespace를 볼 수 있다.**
- `T` 는 그 정의 안에서만 보인다.
- `type` 문의 값은 **지연 평가**되어, 아직 정의되지 않은 이름도 쓸 수 있다.

```python
def first[T](xs: list[T]) -> T:
    return xs[0]

print(first.__type_params__)         # (T,)
try:
    T
except NameError as e:
    print(e)                         # name 'T' is not defined   ← 밖에서는 안 보임

type Alias = list[Later]             # Later 는 아래에서 정의 → 지연 평가라 OK
class Later:
    pass
print(Alias.__value__)               # list[__main__.Later]
```

### 4.3 3.13 · `locals()` 와 `frame.f_locals` (PEP 667)

- 3.12 이하에서 함수 안 `locals()` 는 프레임마다 **같은 dict를 재사용하며 호출할 때마다 갱신**했고, 거기에 쓴 값이 변수에 반영될지는 구현에 달려 있었다.
- 3.13부터 의미가 확정되었다.

| 상황 | 3.12 이하 | 3.13 이상 |
|---|---|---|
| 함수/제너레이터/컴프리헨션의 `locals()` | 같은 dict를 호출마다 갱신 | **호출마다 독립된 스냅샷** (써도 변수에 반영 안 됨) |
| 모듈/클래스 본문의 `locals()` | 실제 namespace dict | 동일 (변경 없음) |
| 함수의 `frame.f_locals` | 쓰기가 변수에 반영 안 됨 | **write-through 프록시** (`FrameLocalsProxy`), 쓰면 변수가 바뀜 |
| 함수 안 `exec()` 의 기본 namespace | 호출 간 값이 공유됨 | 호출마다 스냅샷 → 앞 `exec` 의 변수가 안 보임 |

```python
import sys

def f1():
    x = 1
    d = locals()
    x = 2
    locals()                 # 3.12 이하: 같은 dict 를 갱신 / 3.13+: 별도 스냅샷
    return d["x"]

def f2():
    x = 1
    sys._getframe().f_locals["x"] = 99    # 디버거/도구용 API. 일반 코드에서는 쓰지 말 것
    return x

print(f1())    # 3.12 이하: 2 / 3.13+: 1
print(f2())    # 3.12 이하: 1 / 3.13+: 99
```

```python
import sys

def g():
    exec("a = 0")
    try:
        exec("print(a)")
    except NameError as e:
        print(e)                                       # 3.13+: name 'a' is not defined (3.12 이하: 0 출력)

    ns = {}
    exec("a = 0", locals=ns)                           # namespace 를 명시하면 공유됨 (locals= 키워드는 3.13+)
    exec("print(a)", locals=ns)                        # 0

    x = 1
    exec("x = 2", locals=sys._getframe().f_locals)     # 실제 변수를 바꾸려면 프록시를 넘김
    print(x)                                           # 2

g()
```

- 정리: **함수 안에서 `locals()` 에 값을 써서 변수를 바꾸려 하지 않는다.** 읽기 용도(디버깅·출력)로만 쓴다.
- 3.15에서는 이 프록시 타입이 `types.FrameLocalsProxyType` 으로 공개되었다.

### 4.4 3.14 · 어노테이션 지연 평가 (PEP 649 / 749)

- 3.13까지는 어노테이션이 정의 시점에 평가되어, 아직 없는 클래스를 가리키면 따옴표(`"Node"`)나 `from __future__ import annotations` 가 필요했다.
- 3.14부터는 **어노테이션을 처음 접근할 때 평가**한다. 이때 쓰이는 것이 annotation scope이고, 공식 문서도 "3.14부터 어노테이션에도 annotation scope를 쓴다"고 설명한다.

```python
class Node:
    next: Node | None = None       # 3.13 이하: NameError / 3.14+: OK

print(Node.__annotations__)        # {'next': __main__.Node | None}
```

- 새 모듈 `annotationlib` 로 평가 방식을 고를 수 있다.

```python
import annotationlib

class C:
    x: Undefined                   # 어디에도 정의되지 않은 이름

print(annotationlib.get_annotations(C, format=annotationlib.Format.STRING))
# {'x': 'Undefined'}
print(annotationlib.get_annotations(C, format=annotationlib.Format.FORWARDREF))
# {'x': ForwardRef('Undefined', is_class=True, owner=<class '__main__.C'>)}
try:
    C.__annotations__              # 기본(VALUE): 실제로 평가 → NameError
except NameError as e:
    print(e)                       # name 'Undefined' is not defined
```

- `from __future__ import annotations` 는 당분간 유지되지만 이후 deprecated 예정이다 (PEP 749).
- 런타임에 어노테이션을 읽는 라이브러리(FastAPI 등)는 3.14에서 영향을 받을 수 있다. 라이브러리 버전을 확인한다.

### 4.5 3.15 · lazy import (PEP 810)

- `lazy` 소프트 키워드를 붙이면 import가 **첫 사용 시점까지 미뤄진다.**
- namespace 관점에서 보면:
  - 사용 전: 이름이 실제 모듈이 아니라 **지연 프록시 객체**(`types.LazyImportType`)에 묶여 있다.
  - 첫 사용: 실제로 import하고, 모듈 global namespace의 프록시를 **실제 객체로 교체**한다.
  - `globals()` / `__dict__` 접근은 프록시를 풀지 않는다. 그대로 프록시가 보인다. (PEP 810)

```python
import sys, types

lazy import colorsys
print("colorsys" in sys.modules)                                   # False
print(isinstance(globals()["colorsys"], types.LazyImportType))     # True  ← 프록시

print(colorsys.rgb_to_hsv(1, 0, 0))                                # (0.0, 1.0, 1)  ← 여기서 실제 import
print("colorsys" in sys.modules)                                   # True
print(type(globals()["colorsys"]).__name__)                        # module  ← 실제 객체로 교체됨

lazy from math import sqrt                                         # from-import 도 가능
print(isinstance(globals()["sqrt"], types.LazyImportType))         # True   ← 아직 프록시
print(sqrt(4), type(globals()["sqrt"]).__name__)                   # 2.0 builtin_function_or_method  ← 실제 함수로 교체
```

- **제약**
  - **모듈 최상위에서만** 가능하다. 함수, 클래스 본문, `try` 블록 안에서는 `SyntaxError`. `lazy from x import *` 도 불가.
  - 3.14 이하에서는 문법 자체가 `SyntaxError` 다.
  - 모듈이 없거나 import에 실패하는 오류는 import 줄이 아니라 **처음 사용하는 지점**에서 발생한다.
- **전역 제어**: `-X lazy_imports=all|normal`, 환경변수 `PYTHON_LAZY_IMPORTS`, `sys.set_lazy_imports()` / `sys.get_lazy_imports()`, `sys.set_lazy_imports_filter()`
- **하위 호환용**: 모듈에 `__lazy_modules__ = ["json", "pathlib"]` 를 적으면 일반 `import json` 문도 3.15에서 lazy가 된다. 3.15 미만에서는 무시되어 평소처럼 즉시 import된다.
- 주의: import되는 모듈의 최상위 코드 실행(부작용)도 **첫 사용 시점으로 미뤄진다.**

### 4.6 3.15 · 그 밖의 namespace 관련 변화

- `__cached__` 모듈 attribute를 import 시스템이 더 이상 설정하지 않는다. `__spec__.cached` 를 쓴다.
- `__loader__` 는 3.16에서 import 시스템과 표준 라이브러리가 더 이상 설정·참조하지 않을 예정이다 (3.15 문서의 Pending removal). `__spec__.loader` 를 쓴다.
- built-in namespace에 `frozendict`, `sentinel` 이 추가되었다. (같은 이름의 변수를 이미 쓰고 있어도 앞쪽 scope가 우선이라 충돌하지 않는다.)


---

## 5. 자주 하는 실수와 확인 도구

### 5.1 자주 하는 실수

```python
items = []

def add(x):
    items.append(x)     # OK: 객체를 바꾸는 것이지 이름을 다시 묶는 게 아님 (global 불필요)

def reset():
    items = []          # 함수의 새 local 이 생길 뿐, 전역 items 는 그대로

add(1); reset()
print(items)            # [1]
```

- 읽기만 하는 바깥 변수를 **대입**하는 순간 local이 되어 `UnboundLocalError` (3.3)
- 변수 이름을 `list`, `id`, `type`, `input`, `sum` 으로 지어 내장 이름을 가림 (3.8)
- 클래스 변수를 메서드에서 이름만으로 접근 (3.6)
- 루프에서 만든 람다/클로저가 모두 마지막 값을 봄 (3.5)
- 함수 안에서 `locals()["x"] = ...` 로 변수를 바꾸려 함 → 3.13+에서는 반영되지 않음 (4.3)
- 3.15 `lazy import` 를 함수 안에 씀 → `SyntaxError` (4.5)

### 5.2 확인 도구

| 도구 | 용도 |
|---|---|
| `globals()` | 현재 모듈의 global namespace (dict) |
| `locals()` | 현재 local namespace. 함수: 스냅샷 dict(3.13+), 모듈/클래스: 실제 namespace |
| `vars(obj)` / `obj.__dict__` | 객체(모듈 포함)의 attribute namespace |
| `dir()` / `dir(obj)` | 현재 scope / 객체의 이름 목록 |
| `dir(builtins)` | 내장 이름 목록 |
| `sys.modules` | import된 모듈 캐시 |
| `func.__code__.co_varnames` | 함수의 local 이름 (컴파일 때 결정) |
| `func.__code__.co_freevars`, `func.__closure__` | 클로저가 참조하는 바깥 변수와 cell |

---

## 6. 참고 자료

- 원문 블로그: https://yomangstartup.tistory.com/112
- Python Tutorial 9.2 Python Scopes and Namespaces: https://docs.python.org/3/tutorial/classes.html
- Language Reference, Execution model (Naming and binding, Annotation scopes): https://docs.python.org/3/reference/executionmodel.html
- What's New in Python 3.15: https://docs.python.org/3/whatsnew/3.15.html
- PEP 667 – Consistent views of namespaces: https://peps.python.org/pep-0667/
- PEP 709 – Inlined comprehensions: https://peps.python.org/pep-0709/
- PEP 695 – Type Parameter Syntax: https://peps.python.org/pep-0695/
- PEP 649 – Deferred Evaluation Of Annotations Using Descriptors: https://peps.python.org/pep-0649/
- PEP 749 – Implementing PEP 649: https://peps.python.org/pep-0749/
- PEP 810 – Explicit lazy imports: https://peps.python.org/pep-0810/