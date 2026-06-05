# Chapter 11 모듈과 패키지

## 11.1 모듈과 import 문

> 두 개 이상의 파일에서 파이썬 코드를 작성하고 사용한다. 모듈은 파이썬 코드 파일이다. 개발자는 특별한 작업 없이 코드를 모듈로 사용할 수 있다.
> import 문을 사용하여 다른 모듈의 코드를 참조한다. 이것은 임포트한 모듈의 코드와 변수를 프로그램에서 사용할 수 있게 만들어준다.

### 11.1.1 모듈 임포트하기

> import 문을 사용하여 간단하게 모듈을 임포트할 수 있다. 확장자 .py를 제외한 파이썬 파일의 이름을 입력한다.

예제 11-1. fast.py

```python
from random import choice

places = ["McDonalds", "KFC", "Burger King", "Taco Bell", "Wendys", "Arbys", "PizzaHut"]

def pick():
    """
    임의의 패스트푸드점을 반환한다.
    """
    return choice(places)
```

예제 11-2 lunch.py

```python
import fast

place = fast.pick()
print("Let's go to", place)
```

> 두 파일을 같은 디렉토리에 저장하고, 메인 프로그램의 lunch.py를 실행하면 메인 프로그램은 fast 모듈에 접근해서 fast() 함수를 실행한다. 이 함수는 문자열 리스트로부터 임의의 결과를 반환하고, 메인 프로그램에서 그 결과를 출력한다.
> 위 예제에서 import 문을 두 번 사용했다.

- 메인 프로그램 lunch.py에서 fast 모듈을 임포트했다.
- 모듈 fast.py의 pick() 함수에서 파이썬 표준 라이브러리인 random 모듈의 choice 함수를 임포트했다.

또한 메인 프로그램과 모듈에서 두 가지 방식으로 임포트했다.

- 첫 번째 경우, fast 모듈 전체를 임포트했지만 pick() 앞에 `fast.`를 붙였다. import 문 이후, fast.py에 있는 모든 객체는 이름 앞에 fast.를 붙여 메인 프로그램에서 사용할 수 있다. 모듈 이름으로 내용을 한정하고 정리함으로써 다른 모듈 간의 불필요한 이름 충돌을 피해야 한다. pick() 함수가 다른 모듈에 있을 수 있지만, 시룻로 다른 모듈의 함수를 호출하지 않았다.
- 두 번째 경우, fast.py의 from random import choice에서 `choice()` 함수를 바로 가져왔다.

예제 11-3. fast2.py

```python
places = ["McDonalds", "KFC", "Burger King", "Taco Bell", "Wendys", "Arbys", "PizzaHut"]

def pick():
    """
    임의의 패스트푸드점을 반환한다.
    """
    import random
    return random.choice(places)
```

### 11.1.2 다른 이름으로 모듈 임포트하기

> alias 사용해 가져오기

```python
import fast as f
place = f.pick()
print("Let's go to", place)
```

### 11.1.3 필요한 모듈만 임포트하기

> 모듈 전체나 필요한 부분만 임포트할 수 있다. 예제 11-1 에서 random 모듈의 choice() 함수만 임포트했다.
> 모듈에서 alias를 사용한 것처럼 모듈의 각 항목에 별명을 사용할 수 있다.
> 이전 패스트푸드의 예제에서 fast 모듈에서 pick() 함수를 원래 이름으로 임포트한다.

```python
from fast import pick
place = pick()
print("Let's go to ", place)

from fast import pick as who_cares
place = who_cares()
print("Let's go to ", place)

```

## 11.2 패키지

> 파이썬 애플리케이션을 좀 더 확장하기 위해 모듈을 패키지라는 파일과 모듈 계층 구조에 구성할 수 있다. 패키지는 .py 파일을 포함한 하위 디렉토리다. 또한 디렉터리 안에 디렉터리를 여러 깊이로 사용할 수 있다.

> 현재 디렉터리에 questions.py라는 새로운 메인 프로그램을 작성한다. choice라는 하위 디렉토리를 만들고 fast.py와 advice.py라는 두 모듈을 작성한다. 각 모듈에는 문자열을 반환하는 함수가 있다.

예제 11-7 questions.py

```python
from choice import fast, advice

print("Let's go to", fast.pick())
print("Should. we take out?", advice.give())

```

> 파이썬은 현재 디렉터리에서 choice라는 디렉토리를 찾는다. 그리고 그 안에 fast.py와 advice.py 파일을 찾는다.

### 11.2.1 모듈 탐색 경로

> 이전 절의 예제에서 현재 디렉토리와 하위 디렉터리를 선택하여 해당 모듈에 접근했다. 다른 위치에서도 접근하여 제어할 수 있다.

> 이전에는 표준 라이브러리의 random 모듈에서 choice() 함수를 임포트했다. 이 모듈은 현재 디렉터리에 없기 때문에 다른 위치에서 찾아야 한다.

> 파이썬 인터프리터가 보는(임포트하는) 모든 위치를 보려면 표준 sys 모듈을 임포트해서 path 리스트를 살펴본다. 이것은 파이썬이 임포트할 모듈을 찾기 위해 탐색하는 디렉터리 이름 및 ZIP 아카이브 파일의 리스트다.

```python
import sys
for place in sys.path:
    print(place)

```

> 파이썬은 임포트할 파일을 현재 디렉터리에서 먼저 찾는다. 즉, import fast는 fast.py를 찾는다. 이것은 파이썬의 일반적인 설정이다. 또한 sources라는 하위 디렉터리를 만들어 파이썬 파일을 넣을 때 import sources를 사용하거나 from sources import fast를 사용하여 임포트 한다.

> 중복된 이름의 모듈이 있다면 첫 번째로 검색된 모듈을 사용한다. 즉, 우리가 random이라는 모듈을 정의하고, 이 모듈이 표준 라이브러리를 찾기 전의 검색 경로에 있다면 표준 라이브러리의 random 모듈에 접근할 수 없다.

> 코드 내에서 탐색 경로를 수정할 수 있다. 파이썬이 다른 것보다 먼저 /my/modules 디렉터리에서 탐색하길 원한다고 가정하면 다음과 같이 코드를 추가한다.

```python
import sys
sys.path.insert(0, "/my/modules")
```

### 11.2.2 상대/절대 경로 임포트

> 파이썬은 절대 또는 상대 경로 임포트를 지원한다. 지금까지 본 예제는 절대 경로 임포트다. import rougarou를 입력하면, 탐색 경로의 각 디렉터리에 대해 파이썬은 rougarou.py인 파일 이름(모듈) 또는 rougarou인 디렉터리 이름(패키지)을 찾는다.

- rougarou.py 파일이 메인 프로그램을 실행한 파일과 같은 디렉터리에 있는 경우, `from . import rougarou`를 사용하여 상대 경로 임포트를 할 수 있다.
- 상위 디렉토리에 있는 경우, `from .. import rougarou`를 사용한다.
- 상위 디렉터리의 creatures라는 디렉터리에 있는 경우, `from ..creatures import rogarou`를 사용한다.

### 11.2.3 네임스페이스 패키지

> 파이썬 모듈을 다음과 같이 패키징할 수 있다는 것을 배웠다.

- 단일 모듈(.py 파일)
- 패키지(모듈 및 다른 패키지를 포함하는 디렉터리)

> 네임스페이스 패키지가 있는 디렉터리에서 패키지를 분할할 수 도 있다. critters 패키지가 있다고 가정한다. 시간이 지나면서 패키지가 커질 수 있으므로 위치별로 세분화하려고 한다. 한 가지 옵션은 critters 아래에 하위 패키지를 추가하고 기존 .py 모듈 파일을 그 아래로 모두 이동한다. 그러나 이것은 이 모듈을 임포트한 다른 모듈에서 문제가 발생한다. 그대신 다음을 수행한다.

- critters 상위에 새 위치 디렉터리를 만든다.
- 새 상위 디렉터리 아래에 다른 종류의 생물 디렉터리를 만든다.
- 기존 모듈을 해당 디렉터리로 이동한다.

```
critters
ㄴ rougarou.py
ㄴ wendigo.py
```

이 모듈의 일반적인 import 문은 다음과 같다.
`from critters import wendigo, rougarou``

이제 미국의 남과 북 위치를 추가했을 때의 파일과 디렉터리의 내용은 다음과 같다.

```
north
ㄴcritters
  ㄴwendigo.py
south
ㄴcritters
  ㄴrougarou.py
```

north 와 south가 모두 모듈 탐색 경로에 있다면, 단일 디렉터리 패키지를 공동으로 사용하는 것처럼 모듈을 가져올 수 있다.
`from critters import wendigo, rougarou`

### 11.2.4 모듈 vs 객체

> 언제 코드를 모듈로 사용해야 하는가? 아니면 객체로 사용해야 하는가?
> 모듈과 객체는 여러 면에서 비슷하게 보인다. stuff라는 내부 데이터 값이 있는 thing이라는 객체 또는 모듈을 사용하면 thing.stuff로 값에 접근할 수 있다.

> 모듈이나 클래스를 만들 때 stuff가 정의되었거나 나중에 할당될 수 있다. 객체는 프로퍼티나 던더(\_\_) 이름을 사용하여 데이터 속성에 대한 접근을 숨기거나 제어할 수 있다.

```python
import math
math.pi
>>> 3.14159...
math.pi = 3.0
math.pi
>>> 3.0
```

> 위 코드는 좋은 코드는 아니지만, 파이썬 math 모듈에 영향을 미치지 않았다. 호출 프로그램에서 가져온 math 모듈 코드의 사본에 대해서만 pi 값을 변경했으며, 위 코드 수행이 완료되면 이 값은 사라진다.
