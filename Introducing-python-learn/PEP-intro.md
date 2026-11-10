# PEP(Python Enhance Proposal)
> 파이썬은 자유로움이 강력한 언어지만, 규모가 커질수록 개인의 자유보다는 조직을 위한 방향이어야 더 강력한 힘을 발휘할 수 있다. 파이썬 소프트웨어 재단(PSF)는 python official docs로 파이썬 개선 제안, PEP라는 것을 작성한다.[PEP 공식 링크](https://peps.python.org/)

## PEP8
- python의 syntax, coding 스타일 가이드라인에 대한 제안서로 

### 0. 대원칙(The Philosophy)
- 일관성(Consistency): 스타일 가이드의 목적은 일관성을 유지하는 것. 프로젝트 전체, 모듈, 함수 단위에서 스타일이 통일되어야 한다.
- 무조건적인 맹종 금지: 때로는 스타일 가이드를 깨는 것이 코드 가독성을 더 높일 때가 있다. (기존 코드와의 일관성을 유지해야 할 때, 가이드를 따르면 오히려 난해해질 때 등)

### 1. Code Layout

#### 들여쓰기(Indentation)
- 공백(Space) 4칸 사용을 강력히 권장함.
- 탭(Tab)과 공백을 섞어 쓰지 마십시오. (파이썬 3에서는 혼용 금지)

```python
# Correct:

# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

#### 최대 줄 길이(Maximum Line Length)
- 모든 줄은 최대 79자 이하로 작성
- 주석이나 독스트링(Docstring)은 72자 이하로 제한
- 긴 줄을 나눌 때는 백슬래시(`\`)보다 괄호(`(), {}, []`)를 사용하는 암시적 줄 바꿈을 권장함
    ```python
    my_list = [
        1, 2, 3,
        4, 5, 6,
        ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
        )
    ```

#### 이항 연산자 전/후 줄 바꿈?(Should a Line Break Before or After a Binary Operator?)

**이항 연산자 전에 줄 바꿈!** (Knuth의 스타일)

```python
# Wrong:
# operators sit far away from their operands
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

```python
# Correct:
# easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

#### 빈 줄(Blank Lines)
- 최상위(Top-level) 함수와 클래스 정의 사이는 2줄을 띕니다.
- 클래스 내부의 메서드 정의 사이는 1줄을 띕니다.
- 함수 내부에서 논리적인 단락을 구분할 때 1줄을 띌 수 있습니다.

#### 소스 파일 인코딩(Source File Encoding)
- 기본적으로 항상 **UTF-8을 사용합니다.**

#### Imports
- 기본적으로 별도의 줄에 작성합니다.

```python
# Correct:
import os
import sys
```
```python
# Wrong:
import sys, os
```
```python
# 단, from 문법은 허용
from subprocess import Popen, PIPE
```
- 임포트는 항상 파일의 맨 위(모듈 독스트링 다음, 전역 변수/상수 이전)에 위치합니다.
- 임포트 순서 (각 그룹 사이는 빈 줄 하나로 구분):
    1. 표준 라이브러리 (Standard library)
    2. 관련된 서드파티 (Third-party) 라이브러리
    3. 로컬 애플리케이션 또는 라이브러리 특정 임포트
- 와일드카드 임포트(`from <module> import *`)는 네임스페이스를 오염시키므로 피해야 한다.

#### 모듈 레벨 Dunder Name
- 모듈 레벨 던더의 대표적인 예:
    - `__all__`: `from 모듈 import *`를 했을 때 공개할 함수/변수 목록을 지정
    - `__version__`: 해당 모듈/패키지의 버전 정보
    - `__author__`: 작성자 정보
- 핵심 규칙: 코드 작성 순서
    - 파이썬 모듈 맨 윗 부분을 작성할 때 반드시 지켜야 하는 코드의 순서를 정해둔 것
    1. 모듈 독스트링(Docstring): 모듈에 대한 설명(`"""..."""`)
    2. `from __future__` 임포트: 파이썬 문법상 다른 모든 코드보다 무조건 먼저 와야 함
    3. 모듈 레벨 던더 변수: `__all__`, `__version__`, `__author__` 등
    4. 일반 `import` 문: `import os`, `import sys` 등

```python
# 1. 가장 먼저 모듈 독스트링이 옵니다.
"""This is the example module.

This module does stuff.
"""

# 2. 파이썬 문법 제약상 docstring 바로 뒤에는 `__future__` 임포트가 와야 합니다.
from __future__ import barry_as_FLUFL

# 3. 그 바로 다음에 모듈 메타데이터(던더 변수들)를 정의합니다.
__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

# 4. 던더 변수 정의가 끝난 후 비로소 일반 라이브러리들을 import 합니다.
import os
import sys
```

### 2. 공백 사용 (Whitespace in Expressions and Statements)

#### 불필요한 공백 피하기
- 괄호 바로 안쪽: `spam(ham[1], {eggs: 2})` (O) / `spam( ham[ 1 ], { eggs: 2 } )` (X)
- 쉼표, 콜론, 세미콜론 바로 앞: `if x == 4: print(x, y)` (O) / `if x == 4 : print(x , y)` (X)
- 슬라이스 콜론: 양쪽의 공백 수가 같아야 함 (`ham[1:9]`, `ham[lower:upper]`, 'ham[lower + offset : upper + offset]`)
- 함수 호출 괄호 바로 앞: `spam(1)` (O) \ `spam (1)` (X)

#### 연산자 주변
- 대입(`=`), 증감(`+=`), 비교(`==`, `<`, `>` 등), 논리(`and`, `or`) 연산자 앞뒤에는 항상 1개의 공백을 둡니다.
- 키워드 인자나 기본 매개변수의 `=` 주위에는 공백을 넣지 않습니다.

```python
# Correct:
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```
```python
# Wrong:
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```
```python
# Correct:
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```
```python
# Wrong:
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

- 하지만, 타입 힌트가 있는(annotated) 함수 매개변수의 경우 `:` 때문에 가독성이 떨어질 수 있으므로 기본값과 결합될 때는 `=` 주위에 공백을 둡니다.
```python
# Correct:
def munge(sep: AnyStr = None): ...
def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
# Wrong:
def munge(input: AnyStr=None): ...
def munge(input: AnyStr, limit = 1000): ...
```

#### 기타

- 한 줄에 여러 문장을 작성한 코드는 일반적으로 지양합니다.
> Compound statements (multiple statements on the same line) are generally discouraged.

Rather not:
```python
# Wrong:
if foo == 'blah': do_blah_thing()
for x in lst: total += x
while t < 10: t = delay()
```
Definitely not:
```python
# Wrong:
if foo == 'blah': do_blah_thing()
else: do_non_blah_thing()

try: something()
finally: cleanup()

do_one(); do_two(); do_three(long, argument,
                             list, like, this)

if foo == 'blah': one(); two(); three()
```

### 3. 주석 (Comments)
- 기본 원칙: 코드와 모순되는 주석은 없느니만 못하다. 코드가 바뀌면 주석도 반드시 업데이트해야 한다.
- 블록 주석: 코드와 동일한 들여쓰기 수준을 유지하며, 각 줄은 `#`로 시작한다.
- 인라인 주석: 코드와 같은 줄에 작성하는 주석은 남용하지 말고, 코드와 최소 2칸 이상의 공백을 둔 뒤 `#`을 작성한다.
- 독스트링(Docstring - PEP 257)
    - 모든 공개(public) 모듈, 함수, 클래스, 메서드에는 독스트링을 작성해야 한다.
    - 여러 줄로 작성할 때는 닫는 따옴표(`"""`)를 별도의 줄에 작성한다.

### 4. 명명 규칙(Naming Convention)

|대상|스타일|예시|
|-|-|-|
|패키지/모듈|짧은 소문자 (모듈에 한해 밑줄 허용)|`my_module.py`, `sys`|
|클래스|카멜 케이스 (CapWords / PascalCase)|`MyClass`, `HTTPResponse`|
|예외(Exceptions)|클래스와 동일하나 끝에 `Error` 접미사|`CustomValueError`|
|함수/메서드|스네이크 케이스 (소문자 + 밑줄)|`my_function()`, `calculate_sum()`|
|변수|스네이크 케이스 (소문자 + 밑줄)|`user_name`, `total_count`|
|상수(Constants)|모든 글자 대문자 + 밑줄|`MAX_OVERFLOW`, `TOTAL`|

- 특수 밑줄 규칙:
    - `_single_leading_underscore`: 내부적으로만 사용됨을 암시 (`from module import *` 시 제외됨)
    - `single_trailing_underscore`: 파이썬 예약어와의 충돌을 피할 때 사용 (예: `class_`).
    - `__double_leading_underscore`: 클래스 속성의 이름 맹글링(Naming Mangling)을 유도할 때(상속 시 충돌 방지용)
    - `__magic__`: 특수 메서드나 속성 (예: `__init__`, `__str__`). 임의의 이런 형식의 이름을 새로 짓지 말 것.

### 5. 프로그래밍 권장 사항 (Programming Recommendations)
- `None`을 비교할 때는 항상 `is`나 `is not`을 사용합니다. (`==` 사용 금지)
    ```python
    if x is not None: # 권장
    ```
- `not ... is` 보다는 `is not` 연산자를 사용합니다.
    ```python
    if x is not None: # 권장
    if not x is None: # 비권장
    ```
- 불리언 값의 참/거짓을 비교할 때 `== True` 나 `== False`를 사용하지 않습니다.
    ```python
    if greeting: # 권장
    if greeting == True: # 비권장
    ```
- 빈 시퀀스(문자열, 리스트, 튜플)의 참/거짓을 검사할 때 길이를 재지 않습니다.
    ```python
    if not seq: # 빈 리스트일 때 True
    if len(seq): # 비권장
    ```
- 예외(Exception) 처리 시 단순히 `except:`만 쓰지 말고 구체적인 에러 타입을 명시합니다. (`except Exception:` 또는 bare `except:`는 시스템 종료 시그널까지 잡아버려 디버깅을 어렵게 만듭니다.)

### 요약 및 실무 팁

모든 규칙을 외울 필요는 없습니다. 최근에는 다음과 같은 **Linter/Formatter 도구** 를 사용하여 PEP 8 준수를 자동화합니다.

- Flake8 / Ruff: PEP 8 규칙 위반 사항을 검사(Linting)해 주는 도구
- Black / autopep8: 코드를 PEP 8 스타일에 맞게 자동으로 포맷팅해 주는 도구