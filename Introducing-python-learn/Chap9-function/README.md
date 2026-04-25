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

> 각 함수는 자신의 네임스페이스를 정의한다.
