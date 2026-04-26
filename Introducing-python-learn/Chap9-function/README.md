# 9장 함수(Python)

## 9.3 인수와 매개변수

> 자바와 동일하게? 함수 외부에서는 인수라고 하지만 내부에서는 매개변수라고 한다.
> 함수로 전달한 값을 인수라고 부른다. 인수의 값은 함수 내에서 해당하는 매개변수에 복사된다.

> 함수가 명시적으로 return 을 호출하지 않으면, 호출자는 반환값으로 None을 얻는다.

### 9.3.1 유용한 None

> None은 아무것도 없다는 것을 뜻하는 파이썬의 특별한 값이다. 빠뜨린 빈 값을 구분하기 위해 None을 사용한다.

> 불리언 값 False와 None을 구분하기 위해 `is` 연산자를 사용한다.

### 9.3.2 위치 인수

> 파이썬은 다른 언어에 비해 함수의 인수를 유연하고 독특하게 처리한다. 인수의 가장 익숙한 유형은 값을 순서대로 상응하는 매개변수에 복사하는 위치 인수(positional argument)다.

### 9.3.3 키워드 인수

> 위치 인수의 혼란을 피하기 위해 매개변수에 상응하는 이름을 인수에 저장할 수 있다. 심지어 인수를 함수 정의와 다른 순서로 지정할 수 있다.

```python
menu(entree='beef', dessert='bagel', wine='bordeaux')
```

### 9.3.4 기본 매개변수 값 지정하기

> 매개변수에 기본값을 지정할 수 있다. 호출자가 대응하는 인수를 제공하지 않으면 기본값을 사용한다.

> 기본 인수는 함수가 실행될 때 계산되지 않고, 함수를 정의할 때 계산된다. 파이썬 초급(혹은 중급) 개발자는 리스트 혹은 딕셔너리와 같은 가변 데이터 타입을 기본 인수로 사용할 때 실수하게 된다.

```python
def buggy(arg, result=[]):
    result.append(arg)
    print(result)

buggy('a')
>>> ['a']
buggy('b') # expect ['b']
>>> ['a','b']
```

### 9.3.5 위치 인수 분해하기/모으기: \*

> 함수의 매개변수에 애스터리스크를 사용할 때, 애스터리스크는 매개변수에서 위치 인수 변수를 튜플로 묶는다.

```python
def print_args(*args):
    print("Positional tuple:", args)
```

### 9.3.6 키워드 인수 분해하기/모으기: \*\*

> 키워드 인수를 딕셔너리로 묶기 위해 두 개의 애스터리스크를 사용할 수 있다. 인수의 이름은 키고, 값은 이 키에 대응하는 딕셔너리 값이다.

```python
def print_kwargs(**kwargs):
    print("Keyword arguments:", kwargs)
```

> 함수 내에서 `kwargs`는 딕셔너리 매개변수다. 인수 순서는 다음과 같다.

- 위치 인수
- 위치 인수(\*args) - 옵션
- 키워드 인수(\*\*kwargs) - 옵션

### 9.3.7 키워드 전용 인수

> 위치 매개변수와 이름이 같은 키워드 인수를 전달하면 원하는 결과를 얻지 못할 수 있다. 파이썬 3에서는 키워드 전용 인수(keyword-only arguments)를 지정할 수 있다. 이름에서 알 수 있듯이 값을 위치적으로 제공하지 않고, '이름=값'으로 제공해야 한다. 아래의 함수 정의에서 단일 애스터리스크(\*)는 start 및 end 매개변수의 기본값을 사용하고 싶지 않은 경우 명명된 인수로 제공되야 함을 의미한다.

```python
def print_data(data, *, start=0, end=100):
    for value in (data[start:end]):
        print(value)

data = ['a','b','c','d','e','f']
print_data(data)
>> a
>> b
>> c
>> d
>> e
>> f

print_data(data, start=4)
>> e
>> f

print_data(data, end=2)
>> a
>> b
```

파이썬에서 함수의 인자를 전달할 때 **"이 값은 반드시 이름(키워드)을 명시해서 전달해야 한다"**고 강제하는 문법

---

#### 1. 핵심 개념: 키워드 전용 인수(Keyword-only arguments)란?

보통 파이썬 함수에서 인자를 넘길 때는 두 가지 방법이 있습니다.

- **위치 기반:** `func(100)` (순서대로 전달)
- **키워드 기반:** `func(start=100)` (이름을 지정해서 전달)

보통은 이 두 방식을 섞어서 쓰는데, **"함수를 호출할 때 무조건 `이름=값` 형태로 써야만 동작하게"** 하고 싶을 때 사용하는 것이 `*` 기호입니다.

#### 2. 예시 코드 해석

```python
def print_data(data, *, start=0, end=100):
```

여기서 `*`가 아주 중요한 역할을 합니다. 이 별표는 **"여기 뒤에 오는 인자들(`start`, `end`)은 반드시 키워드(이름)를 붙여서 호출해야 해!"**라는 경계선 역할을 합니다.

#### 왜 이렇게 할까요?

만약 `def print_data(data, start=0, end=100):`이라고 썼다면(별표 없음):

- 사용자가 `print_data(data, 5, 10)`이라고 호출할 수 있습니다.
- 이때 파이썬은 `start=5`, `end=10`이라고 판단합니다.
- 하지만 만약 인자가 많아지면, 사용자가 "어디가 `start`고 어디가 `end`지?" 헷갈릴 수 있습니다.

**`*`를 사용하면:**

- 사용자가 `print_data(data, 5, 10)`이라고 쓰면 **에러**가 납니다.
- 반드시 `print_data(data, start=5, end=10)`처럼 써야만 합니다.
- 이렇게 하면 코드의 **가독성**이 확 올라가고, **실수(인자 순서 착각 등)를 방지**할 수 있습니다.

#### 3. 요약

- **`*`의 역할:** 이 기호를 기준으로 뒤에 나오는 인자들은 반드시 `이름=값` 형식(키워드 인수)으로만 입력해야 합니다.
- **장점:** 함수를 호출할 때 인자의 의미가 명확해집니다. `start=4`라고 쓰면 누구든 "아, 4는 시작 위치구나"라고 바로 알 수 있으니까요.
- **결론:** "위치에 의존해서 값을 넣지 말고, 반드시 이름을 밝혀서(키워드 전용으로) 값을 넣어라"라고 강제하는 문법입니다.

## 9.4 독스트링(docstring)

> 함수 바디 시작 부분에 문자열을 포함시켜 함수 정의에 문서를 붙일 수 있다.

```python
def print_if_true(thing, check):
    '''
    Prints the first argument if a second argument is true.
    The operation is:
        1. Check whether the second argument is true.
        2. If it is, print the first argument'.
        '''
        if check:
            print(thing)
```

> 함수의 독스트링을 출력하려면 `help()` 함수를 호출한다.

> 서식 없는 독스트링을 그대로 보고 싶다면 다음과 같이 작성한다.

```python
print(echo.__doc__)
echo returns its input argument
```

> `__doc__`은 docstring의 내부 이름인 함수 내의 변수다. 더블 언더바(던더dunder라고도 함)는 파이썬에서 내부 사용 목적으로 만들어진 변수다.

## 9.5 일등 시민: 함수

> '모든 것은 객체다'는 파이썬 철학은 파이썬의 만트라mantra(기도, 명상 때 외우는 주문)이기도 하다. 객체는 숫자, 문자열, 튜플, 리스트, 딕셔너리, 함수를 포함한다. 파이썬에서 함수는 일등 시민(first-class citizen)이다. 함수를 변수에 할당하고, 다른 함수에서 이를 인수로 사용하고, 함수에서 이를 반환할 수 있다는 것이다. 이와 같이 파이썬은 다른 언어에서는 구현하기 힘든 기능을 제공한다.

```python
def run_something_with_args(func, arg1, arg2):
    func(arg1, arg2)

def add_args(arg1, arg2):
    print(arg1+arg2)

run_something_with_args(add_args, 5, 9)
>>> 14
```

```python
def sum_args(*args):
    return sum(args)

def run_with_positional_args(func, *args):
    return func(*args)

run_with_positional_args(sum_args, 1, 2, 3, 4)
>>> 10
```

## 9.6 내부 함수

> 함수 안에 또 다른 함수를 정의할 수 있다.

```python
def outer(a, b):
    def inner(c, d):
        return c+d
    return inner(a, b)

outer(4, 7)
>>> 11
```

> 내부 함수는 반복문이나 코드 중복을 피하고자 또 다른 함수 내에 어떤 복잡한 작업을 한 번 이상 수행할 때 유용하게 사용된다. 다음 문자열 예제에서 내부 함수는 인수에 텍스트를 붙여 준다.

```python
def knights(saying):
    def inner(quote):
        return "We are the knights who say: '%s'" % quote
    return inner(saying)

knights('Ni!')
>>> "We are the knights who say: 'Ni!'"
```

### 9.6.1 클로저

> 내부 함수는 클로저(closure)처럼 동작할 수 있다. 클로저는 다른 함수에 의해 동적으로 생성된다. 그리고 외부 함수로부터 생성된 변수값을 변경하고, 저장할 수 있는 함수다.

**클로저(Closure)란 무엇인가?**
클로저는 다음 세 가지 조건을 만족하는 함수를 말합니다.

1. 중첩 함수: 함수 내부에 또 다른 함수(내부 함수)가 정의되어 있다.
2. 참조: 내부 함수가 외부 함수의 변수(자유 변수)를 참조한다.
3. 반환: 외부 함수가 내부 함수를 결과값으로 반환한다.

> 다음 예제는 앞 절 '내부 함수'에서 작성한 knights() 예제다. 이 함수를 새로운 knights2() 함수로 정의한다. 이 함수는 이전과는 달리 inner2()라는 클로저를 사용하기 때문에 똑같은 함수가 아니다.

- inner2()는 인수를 취하지 않고, 외부 함수의 변수를 직접적으로 사용한다.
- knights2()는 inner2 함수 이름을 호출하지 않고, 이를 반환한다.

```python
def knights2(saying):
    def inner2():
        return         return "We are the knights who say: '%s'" % saying
    return inner2
```

> inner2() 함수는 knights2() 함수가 전달받은 saying 변수를 알고 있다. 코드의 `return inner2` 부분은 (호출되지 않은) inner2 함수의 특별한 복사본을 반환한다. 이것이 외부 함수에 의해 동적으로 생성되고, 그 함수의 변수값을 알고 있는 함수인 클로저다.

> 다른 인수를 넣어서 knights2() 함수를 두 번 호출해보자.

```python
a = knights2('Duck')
b = knights2('Hasenpfeffer')

type(a)
>>> <class 'function'>
type(b)
>>> <class 'function'>

a
>>> <function knights2.<local>.inner2 at 0x10193e158>

b
>>> <function knights2.<local>.inner2 at 0x10193e1e0>

a()
>>> "We are the knights who say: 'Duck'"
b()
>>> "We are the knights who say: 'Hasenpfeffer'"
```

## 9.8 제너레이터

> 제너레이터는 시퀀스를 생성하는 객체다. 제너레이터로 전체 시퀀스를 한 번에 메모리에 생성하고 정렬할 필요 없이, 잠재적으로 아주 큰 시퀀스를 순회할 수 있다. 제너레이터는 이터레이터에 대한 데이터의 소스로 자주 사용된다. 우리는 이전에 이미 제너레이터 중 하나인 `range()` 함수를 사용했다. range() 는 일련의 정수를 생성한다. 파이썬2의 range()는 메모리에 제한적인 리스트를 반환한다(제너레이터가 아닌 리스트). 또한 파이썬2에서 xrange()가 있는데(제너레이터), 이는 파이썬3의 일반적인 range()가 됐다.

### 9.8.1 제너레이터 함수

> 잠재적으로 큰 시퀀스를 생성하고, 제너레이터 컴프리헨션에 대한 코드가 아주 길다면 제너레이터 함수를 사용하면 된다. 이것은 일반 함수지만 return 문으로 값을 반환하지 않고 yield 문으로 값을 반환한다. 우리만의 range() 함수를 작성해보자.

```python
def my_range(first=0, last=10, step=1):
    number = first
    while number < last:
        yield number
        number += step

my_range
>>> <function my_range at 0x10193e268>
ranger = my_range(1, 5)
ranger
>>> <generator object my_rage at 0x101a0a168>

for x in ranger:
    print(x)

>>> 1
>>> 2
>>> 3
>>> 4
```

> 제너레이터는 한 번만 순회할 수 있다. 리스트, 셋, 문자열, 딕셔너리는 메모리에 존재한다. 그러나 제너레이터는 해당 값을 즉석에서 생성하고, 이터레이터를 통해 한 번에 하나씩 전달한다. 제너레이터는 모든 값을 기억하지 않으므로 제너레이터를 다시 시작하거나 되돌릴 수 없다.

### 9.8.2 제너레이터 컴프리헨션

> 제너레이터 컴프리헨션은 대괄호, 중괄호 대신 괄호로 묶어서 사용한다. 제너레이터 컴프리헨션은 제너레이터 함수의 축약 버전이며, 안보이게 yield 문을 실행하고, 제너레이터 객체를 반환한다.

```python
genobj = (pair for pair in zip(['a', 'b'], ['1', '2']))
genobj
>>> <generator object <genexpr> at 0x10308fde0>
for thing in genobj:
    print(thing)

>>> ('a', '1')
>>> ('b', '2')
```

## 9.9 데커레이터

> 가끔 코드를 바꾸지 않고, 사용하고 있는 함수를 수정하고 싶을 때가 있다. 일반적인 예는 함수에 전달된 인수를 보기 위해 디버깅 문을 추가하는 것이다.

> 데커레이터(decorator)는 하나의 함수를 취해서 또 다른 함수를 반환하는 함수다. 이 파이썬 트릭을 사용하기 위해서는 다음 기술을 사용한다.

- \*args와 \*\*kwargs
- 내부 함수
- 함수 인수

> document_it() 함수는 다음과 같이 데커레이터를 정의한다.

- 함수 이름과 인수를 출력한다.
- 인수로 함수를 실행한다.
- 결과를 출력한다.
- 수정된 함수를 사용하도록 반환한다.

코드는 다음과 같다.

```python
def document_it(func):
    def new_function(*args, **kwargs):
        print('Running function:', func.__name__)
        print('Positional argument:', args)
        print('Keyword arguments:', kwargs)
        result = func(*arg, **kwargs)
        print('Result:', result)
        return result
    return new_function
```

> document_it() 함수에 어떤 func 함수 이름을 전달하든지 간에 document_it() 함수에 추가 선언문이 포함된 새 함수를 얻는다. 데커레이터는 실제로 func 함수로부터 코드를 실행하지 않는다. 하지만 document_it() 함수로부터 func를 호출하여 결과뿐만 아니라 새로운 함수를 얻는다.

그러면 데커레이터를 어떻게 사용할까? 수동으로 데커레이터를 적용해보자.

```python
def add_ints(a, b):
    return a+b

cooler_add_ints = document_it(add_ints) # 데커레이터 수동 할당
coooler_add_ints(3, 5)
>>> Running function: add_ints
>>> Positional arguments: (3, 5)
>>> Keyword arguments: {}
>>> Result: 8
>>> 8
```

위와 같이 수동으로 데커레이터를 할당하는 대신, 다음과 같이 데커레이터를 사용하고 싶은 함수에 그냥 **@데커레이터\_이름** 을 추가한다.

```python
@document_it
def add_int(a, b):
    return a + b

add_ints(3, 5)

>>> Running function: add_ints
>>> Positional arguments: (3, 5)
>>> Keyword arguments: {}
>>> Result: 8
>>> 8
```

**데커레이터와 클로저의 관계**

```python
def document_it(func):  # 외부 함수
    def new_function(*args, **kwargs):  # 1. 중첩 함수
        # 2. 외부 함수의 인자인 func를 내부에서 사용(참조)하고 있음
        print('Running function:', func.__name__)
        result = func(*args, **kwargs)
        return result
    return new_function  # 3. 내부 함수 자체를 반환
```

- 외부 함수의 환경 기억: `document_it` 함수가 실행을 마치고 종료되면, 일반적인 경우라면 `func`라는 변수는 메모리에서 사라져야 합니다. 하지만 `new_function`이 `func`를 참조하고 있기 때문에, 파이썬은 이 `func`를 클로저 환경에 저장하여 보존합니다.
- 데커레이터의 역할: 데커레이터는 단순히 함수를 꾸미는 도구가 아니라, **함수(func)를 전달받아 그 함수를 포함하는 더 큰 기능의 함수(new_function)를 만들어 반환하는 '함수 공장'** 과 같습니다. 이때 전달받은 `func`가 클로저를 통해 계속 유지되기 때문에, 나중에 `new_function`이 호출될 때 원래의 함수를 안전하게 실행할 수 있는 것입니다.

> 함수는 여러 데커레이터를 가질 수 있다. result를 제곱하는 square_it() 데커레이터를 작성해보자

```python
def square_it(func):
    def new_function(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * result
    return new_function
```

함수에서 가장 가까운(def 바로 위) 데커레이터를 먼저 실행한 후, 그 위의 데커레이터가 실행된다. 이 예제에서 순서를 바꿔도 똑같은 result를 얻지만, 중간 과정이 바뀐다.

```python
@document_it
@square_it
def add_ints(a, b):
    return a + b

add_ints(3, 5)
>>> Running function: new_function
>>> Positional arguments: (3, 5)
>>> Keyword arguments: {}
>>> Result: 64
>>> 64

```

## 9.10 네임스페이스와 스코프

> 이름은 사용되는 위치에 따라 다른 것을 참조할 수 있다. 파이썬 프로그램에는 다양한 네임스페이스가 있다. 네임스페이스는 특정 이름이 유일하고, 다른 네임스페이스에서의 같은 이름과 관계가 없는 것을 말한다.

> 각 함수는 자신의 네임스페이스를 정의한다. 메인 프로그램에서 x라는 변수를 정의하고, 함수에서 x라는 변수를 정의했을 때 이들은 서로 다른 것을 참조한다. 하지만 이 경계를 넘을 수 있다. 다양한 방법으로 다른 네임스페이스의 이름을 접근할 수 있다.

> 메인 프로그램은 전역 네임스페이스를 정의한다. 메인 프로그램의 네임스페이스에서 선언된 변수는 전역 변수다. 

> 함수 내의 지역 변수가 아닌 전역 변수를 접근하기 위해 global 키워드를 사용해서 전역 변수의 접근을 명시해야 한다.(파이썬의 철학: 명확한 것이 함축적인 것보다 낫다)

## 9.11 이름에 _와 __ 사용하기

> 언더바 두 개(__)로 시작하고 끝나는 이름은 파이썬 내부 사용을 위해 예약되어 있다. 그러므로 변수를 선언할 때 두 언더바를 사용하면 안 된다. 개발자들이 이와 같은 변수 이름을 선택할 가능성이 낮아서, 이러한 네이밍 패턴을 선택한 것이다. 

> 함수 이름은 시스템 변수 function.__name__에 있다. 그리고 함수 docstring은 function.__doc__에 있다.

파이썬에서 변수나 함수 이름에 붙는 언더스코어(`_`)는 특별한 의미를 가집니다. 일반적으로 개발자들 간의 **컨벤션(관례)**이나 파이썬 인터프리터가 동작하는 방식과 관련이 있습니다. 크게 다음과 같이 분류하여 설명할 수 있습니다.

---

### 1. 단일 언더스코어 (`_`)

단일 언더스코어는 여러 가지 용도로 사용됩니다.

#### 1.1. `_name` (선행 단일 언더스코어: "내부용" 또는 "비공개"로 간주)
*   **의미:** 이 변수나 함수는 해당 모듈이나 클래스 내부에서만 사용되어야 하며, 외부에서는 직접 접근하지 않는 것이 좋다는 **개발자 간의 암묵적인 약속**입니다. 파이썬은 C++, Java와 같은 언어의 `private` 키워드처럼 강제적인 접근 제한을 두지 않습니다.
*   **효과:**
    *   `from module import *` 구문을 사용하여 모듈을 임포트할 때, `_`로 시작하는 이름은 임포트되지 않습니다. (단, `import module` 후 `module._name`으로 접근하는 것은 가능합니다.)
*   **예시:**
    ```python
    class MyClass:
        def __init__(self):
            self.public_var = "나는 공개 변수"
            self._internal_var = "나는 내부용 변수 (접근하지 마세요)"

        def _internal_method(self):
            print("나는 내부용 메서드")

    def _private_function_in_module():
        print("나는 모듈 내부용 함수")

    obj = MyClass()
    print(obj.public_var)
    print(obj._internal_var) # 경고 없이 접근 가능하지만, 권장되지 않음
    obj._internal_method()    # 경고 없이 접근 가능하지만, 권장되지 않음
    ```
    *대부분의 경우, `_` 접두사를 사용하는 것으로도 충분히 "이것은 건드리지 마세요"라는 의도를 전달할 수 있습니다.*

#### 1.2. `name_` (후행 단일 언더스코어: 파이썬 키워드와의 이름 충돌 방지)
*   **의미:** 변수나 함수의 이름이 파이썬의 예약어(keyword)와 충돌할 때, 이를 피하기 위해 사용됩니다.
*   **예시:**
    ```python
    def my_function(class_): # 'class'는 예약어이므로 'class_' 사용
        print(f"클래스 이름이 될 수 있었던 인자: {class_}")

    my_function("TestClass")

    # print_ = 10 # 과거 Python 2에서 print는 함수가 아닌 키워드였으므로 사용
    ```

#### 1.3. `_` (단일 언더스코어: 임시 또는 무시하는 변수)
*   **의미 1 (무시):** 어떤 값을 반환받거나 할당받지만, 그 값을 사용하지 않을 때 임시 변수처럼 사용합니다.
*   **예시:**
    ```python
    # 반복문에서 인덱스 값이 필요 없을 때
    for _ in range(5):
        print("Hello")

    # 함수가 여러 값을 반환하지만 일부만 필요할 때
    data = ("apple", 10, True)
    name, count, _ = data # 마지막 True 값은 무시
    print(name, count) # apple 10

    # 예외 처리에서 예외 객체가 필요 없을 때
    try:
        # ...
    except ValueError as _: # 또는 except ValueError:
        print("값이 잘못되었습니다.")
    ```
*   **의미 2 (인터프리터):** 파이썬 대화형 인터프리터(REPL)에서 마지막으로 실행된 표현식의 결과값을 저장하는 변수입니다.
*   **예시 (인터프리터에서):**
    ```
    >>> 2 + 2
    4
    >>> _
    4
    >>> "hello" + " world"
    'hello world'
    >>> _
    'hello world'
    ```
*   **의미 3 (숫자 리터럴 구분자, PEP 515):** 큰 숫자의 가독성을 높이기 위해 사용됩니다. (파이썬 3.6부터)
*   **예시:**
    ```python
    population = 7_000_000_000 # 70억
    hex_value = 0x_FF_FF_FF_FF
    print(population) # 7000000000
    ```

---

### 2. 이중 언더스코어 (`__`)

이중 언더스코어는 파이썬에서 더 특별하고, 강력한 의미를 가집니다.

#### 2.1. `__name` (선행 이중 언더스코어: "이름 맹글링(Name Mangling)")
*   **의미:** 클래스 내부에서 사용될 때, 이 변수나 메서드의 이름이 클래스 외부에서 직접 충돌하는 것을 방지하기 위해 파이썬 인터프리터가 **자동으로 이름을 변경**합니다. 이는 상속 시 서브클래스에서 부모 클래스의 메서드를 실수로 오버라이딩하는 것을 막는 목적으로 주로 사용됩니다. (완벽한 private는 아닙니다.)
*   **작동 방식:** `__name`은 `_ClassName__name` 형태로 변경됩니다.
*   **예시:**
    ```python
    class MyClass:
        def __init__(self):
            self.public = "public"
            self._protected = "protected"
            self.__private = "private (mangled)" # 이름 맹글링 적용

        def get_private(self):
            return self.__private # 클래스 내부에서는 원래 이름으로 접근

    obj = MyClass()
    print(obj.public)
    print(obj._protected)

    # print(obj.__private) # Error: AttributeError: 'MyClass' object has no attribute '__private'

    # 맹글링된 이름으로 접근은 가능 (하지만 권장되지 않음)
    print(obj._MyClass__private) # private (mangled)
    ```
    *   `__private`는 클래스 외부에서 `obj.__private`로 접근할 수 없습니다. 대신 `obj._MyClass__private`와 같이 변경된 이름으로 접근해야 합니다.
    *   이것은 "비밀"을 유지하는 것이 아니라, "실수로 변경하는 것을 막는" 메커니즘에 가깝습니다.

#### 2.2. `__name__` (선행 및 후행 이중 언더스코어: "매직 메서드" 또는 "던더(Dunder) 메서드")
*   **의미:** 파이썬이 내부적으로 특정 상황에서 호출하도록 약속된 특별한 메서드 및 속성들입니다. "Dunder"는 "Double Under"의 줄임말로, `__init__`처럼 이중 언더스코어가 양쪽에 붙는 것을 지칭하는 용어입니다.
*   **용도:** 클래스의 동작을 사용자 정의하거나, 파이썬의 내장 함수(예: `len()`, `str()`)나 연산자(예: `+`, `==`)와 상호작용할 때 사용됩니다.
*   **절대 주의사항:** **직접 이런 이름의 변수나 함수를 새로 만들지 마십시오.** 파이썬 언어 자체의 기능 확장을 위한 것이므로, 기존에 정의된 Dunder 메서드를 오버라이딩(재정의)하는 방식으로만 사용해야 합니다.
*   **예시:**
    *   `__init__`: 객체가 생성될 때 호출되는 생성자.
    *   `__str__`: `str()` 함수나 `print()` 함수로 객체를 문자열로 표현할 때 호출.
    *   `__repr__`: 객체의 "공식적인" 문자열 표현을 반환할 때 호출.
    *   `__len__`: `len()` 함수가 객체의 길이를 반환할 때 호출.
    *   `__add__`: `+` 연산자를 오버로딩할 때 호출.
    *   `__name__` (모듈 레벨): 현재 모듈의 이름. 메인 스크립트일 경우 `'__main__'` 값을 가집니다.
    ```python
    class MyNumber:
        def __init__(self, value):
            self.value = value

        def __str__(self): # print() 시 호출
            return f"MyNumber with value: {self.value}"

        def __add__(self, other): # + 연산 시 호출
            return MyNumber(self.value + other.value)

    num1 = MyNumber(10)
    num2 = MyNumber(20)

    print(num1)          # MyNumber with value: 10
    num3 = num1 + num2
    print(num3)          # MyNumber with value: 30

    # 모듈 레벨의 __name__
    # 이 스크립트가 직접 실행될 때만 'Hello from __main__!' 출력
    if __name__ == '__main__':
        print("Hello from __main__!")
    ```

---

### 요약 및 결론

| 언더스코어 패턴        | 의미                                      | 강제성           | 주요 용도                                        |
| :-------------------- | :---------------------------------------- | :--------------- | :----------------------------------------------- |
| `_name` (선행 1개)    | **내부 사용용** (private by convention)   | **약속(컨벤션)** | 모듈/클래스 내부 헬퍼 함수/변수                 |
| `name_` (후행 1개)    | **키워드 이름 충돌 회피**                 | **문법(필요)**   | `class_`, `lambda_` 등 예약어와 겹칠 때           |
| `_` (단독 1개)        | **무시/임시 변수** 또는 **REPL의 마지막 결과** | **문법/관례**    | 값 무시, REPL에서 이전 결과 참조, 숫자 구분자   |
| `__name` (선행 2개)   | **이름 맹글링**                           | **인터프리터**   | 상속 시 서브클래스의 **우발적 오버라이딩 방지** |
| `__name__` (양쪽 2개) | **매직/던더 메서드**                      | **언어 내장**    | 파이썬 내부 동작 사용자 정의 (생성자, 연산자 등) |


## 9.13 비동기 함수

> 비동기 함수를 정의하고 실행하기 위해 async와 await 키워드가 파이썬 3.5에서 추가됐다. 

> 지금은 함수를 정의하는 def 앞에 async 키워드가 붙으면 비동기 함수라는 것을 알면 된다. 마찬가지로 함수를 호출하기 전에 await 키워드가 있으면 해당 함수는 비동기적이다. 
