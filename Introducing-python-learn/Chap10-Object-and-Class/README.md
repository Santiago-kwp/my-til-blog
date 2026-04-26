# 10장. 객체와 클래스

## 10.2 간단한 객체

### 10.2.4 초기화
> 객체를 생성할 때 속성을 할당하려면 객체 초기화 메서드 __init__()를 사용한다.

```python
class Cat:
	def __init__(self, name):
		self.name = name

furball = Cat('Grumpy')
print('Our latest addition: ', furball.name)_
>>> Our latest addition: Grumpy
```

> 모든 클래스 정의에서 __init__() 메서드를 가질 필요가 었다. __init__() 메서드는 같은 클래스에서 생성된 다른 객체를 구분하기 위해 필요한 다른 뭔가를 수행한다. __init__() 메서드는 다른 언어에서 부르는 '생성자' 개념이 아니다. __init__() 메서드 호출 전에 이미 객체를 만들었기 때문이다. __init__() 메서드를 초기화 메서드라고 생각하자!

## 10.3 상속

### 10.3.1 부모 클래스 상속받기
> 필요한 것만 추가하거나 변경해서 새 클래스를 정의한다. 그리고 기존 클래스의 행동을 오버라이드(재정의)한다. 기존 클래스는 부모 클래스, 슈퍼 클래스, 베이스 클래스라고 부른다. 새 클래스는 자식 클래스, 서브 클래스, 파생된 클래스라고 부른다. 

```python
class Car():
	pass

class Yugo(Car):
	pass

issubclass(Yugo, Car)
>>> True
```

### 10.3.4 부모에게 도움받기: super()
> 자식 클래스에서 부모 클래스를 호출하고 싶다면 어떻게 해야 할까? super()메서드를 사용하면 된다. 

```python
class Person():
	def __init__(self, name):
		self.name = name

class EmailPerson(Person):
	def __init__(self, name, email):
		super().__init__(name)
		self.email = email

bob = EmailPerson('Bob Frapples', 'bob@frapples.com')

bob.name
>>> 'Bob Frapples'
bob.email
>>> 'bob@frapples.com'
```

> 왜 자식 클래스에서 다음과 같이 정의하지 않았을까?
```python
class EmailPerson(Person):
	def __init__(self, name, email):
		self.name = name
		self.email = email
```

> 다음과 같이 정의할 수 있지만, 이것은 상속의 이점을 활용할 수 없다. 위에서 super() 메서드를 사용하여 Person 클래스에서 일반 Person 객체와 같은 방식으로 동작하게 만들었다. super() 메서드에 대한 또 다른 이점이 있다. Person 클래스의 정의가 나중에 바뀌면 Person 클래스로부터 상속받은 EmailPerson 클래스의 속성과 메서드에 변경 사항이 반영된다. 

`super().__init__(name)`을 쓰는 이유를 요약하면 **"코드의 중복을 제거하고, 부모 클래스의 설계를 계승(유지)하기 위해서"** 입니다.

#### 1. 부모 클래스의 내부 로직이 복잡할 때 (핵심 이유)
부모 클래스(`Person`)의 `__init__` 메서드에 단순히 `self.name = name`만 있는 것이 아니라, **초기화 과정에서 수행해야 할 아주 복잡한 로직**이 있다고 가정해 봅시다.

```python
class Person:
    def __init__(self, name):
        # 이름 유효성 검사, DB 연결, 데이터 가공 등 복잡한 로직이 있다고 가정
        if not name:
            raise ValueError("이름은 필수입니다.")
        self.name = name.strip().capitalize()
        # ... 그 외 10줄의 추가 초기화 코드 ...

class EmailPerson(Person):
    def __init__(self, name, email):
        # 만약 직접 self.name = name을 한다면?
        # 위의 복잡한 로직들을 EmailPerson에서도 똑같이 다시 작성(복사/붙여넣기)해야 합니다.
        self.name = name 
        self.email = email
```

이렇게 되면 **`Person` 클래스의 초기화 정책이 바뀌었을 때 `EmailPerson` 클래스도 함께 수정해야 하는 '결합도' 문제**가 발생합니다. `super().__init__`을 사용하면 부모의 초기화 로직을 그대로 가져오므로, 부모 쪽만 수정하면 자식은 자동으로 업데이트됩니다.

#### 2. 유지보수와 DRY(Don't Repeat Yourself) 원칙
프로그래밍의 가장 중요한 원칙 중 하나는 **"똑같은 코드를 두 번 작성하지 말라(DRY)"**입니다.

*   `self.name = name`을 자식 클래스에 직접 쓰는 순간, 당신은 "부모 클래스가 하는 일을 내가 똑같이 수행하겠다"라고 선언한 것입니다. 
*   만약 나중에 `Person` 클래스에서 이름 처리 방식을 바꾼다면, `Person`을 상속받은 모든 클래스(`EmailPerson`, `Student`, `Employee` 등)를 일일이 찾아가서 수정해야 합니다. 
*   `super()`를 사용하면 **"이름 초기화는 부모(Person)의 책임이니 부모에게 맡긴다"**라는 명확한 역할 분담이 이루어집니다.

#### 3. 상속의 의미 (계층 구조)
상속은 단순히 기능을 물려받는 것이 아니라 **"자식은 부모의 일종(is-a)이다"**라는 관계를 정의하는 것입니다.

*   `EmailPerson`은 `Person`의 일종입니다. 
*   따라서 `EmailPerson` 객체를 만들 때는 "당연히 `Person` 객체를 만드는 과정이 먼저 선행되어야 한다"는 논리가 성립합니다.
*   `super().__init__`은 "먼저 부모 객체로서 완벽하게 초기화된 후, 나의 고유한 기능(`email`)을 추가하겠다"는 논리적 순서를 보장합니다. 

### 10.3.5 다중 상속

> 파이썬의 상속은 메서드 해석 순서(method resolution order, MRO)에 달려 있다. 각 파이썬 클래스에는 특수 메서드 mro()가 있다. 이 메서드는 해당 클래스 객체에 대한 메서드 또는 속성을 찾는 데 필요한 클래스의 리스트를 반환한다. __mro__라는 유사한 속성은 해당 클래스의 튜플이다. 위 경우 먼저 선언된 부모 클래스를 상속받는다.

```python
class Animal:
	def says(self):
		return 'I speak!'

class Horse(Animal):
	def says(self):
		return 'Neigh!'

class Donkey(Animal):
	def says(self):
		return 'Hee-haw!'

class Mule(Donkey, Horse):
	pass

class Hinny(Horse, Donkey):
	pass

mule = Mule()
hinny = Hinny()

mule.says()
>>> 'hee-haw!'
hinny.says()
>>> 'neigh'
```

> Mule 클래스에서 메서드나 속성을 찾을 때 순서는 다음과 같다.
1. 객체 자신(Mule 타입)
2. 객체의 클래스(Mule)
3. 클래스의 첫 번째 부모 클래스(Donkey)
4. 클래스의 두 번쨰 부모 클래스(Horse)
5. 부모의 부모 클래스(Animal)


