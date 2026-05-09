# 10장. 객체와 클래스

## 10.2 간단한 객체

### 10.2.4 초기화

> 객체를 생성할 때 속성을 할당하려면 객체 초기화 메서드 **init**()를 사용한다.

```python
class Cat:
	def __init__(self, name):
		self.name = name

furball = Cat('Grumpy')
print('Our latest addition: ', furball.name)_
>>> Our latest addition: Grumpy
```

> 모든 클래스 정의에서 **init**() 메서드를 가질 필요가 었다. **init**() 메서드는 같은 클래스에서 생성된 다른 객체를 구분하기 위해 필요한 다른 뭔가를 수행한다. **init**() 메서드는 다른 언어에서 부르는 '생성자' 개념이 아니다. **init**() 메서드 호출 전에 이미 객체를 만들었기 때문이다. **init**() 메서드를 초기화 메서드라고 생각하자!

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

- `self.name = name`을 자식 클래스에 직접 쓰는 순간, 당신은 "부모 클래스가 하는 일을 내가 똑같이 수행하겠다"라고 선언한 것입니다.
- 만약 나중에 `Person` 클래스에서 이름 처리 방식을 바꾼다면, `Person`을 상속받은 모든 클래스(`EmailPerson`, `Student`, `Employee` 등)를 일일이 찾아가서 수정해야 합니다.
- `super()`를 사용하면 **"이름 초기화는 부모(Person)의 책임이니 부모에게 맡긴다"**라는 명확한 역할 분담이 이루어집니다.

#### 3. 상속의 의미 (계층 구조)

상속은 단순히 기능을 물려받는 것이 아니라 **"자식은 부모의 일종(is-a)이다"**라는 관계를 정의하는 것입니다.

- `EmailPerson`은 `Person`의 일종입니다.
- 따라서 `EmailPerson` 객체를 만들 때는 "당연히 `Person` 객체를 만드는 과정이 먼저 선행되어야 한다"는 논리가 성립합니다.
- `super().__init__`은 "먼저 부모 객체로서 완벽하게 초기화된 후, 나의 고유한 기능(`email`)을 추가하겠다"는 논리적 순서를 보장합니다.

### 10.3.5 다중 상속

> 파이썬의 상속은 메서드 해석 순서(method resolution order, MRO)에 달려 있다. 각 파이썬 클래스에는 특수 메서드 mro()가 있다. 이 메서드는 해당 클래스 객체에 대한 메서드 또는 속성을 찾는 데 필요한 클래스의 리스트를 반환한다. **mro**라는 유사한 속성은 해당 클래스의 튜플이다. 위 경우 먼저 선언된 부모 클래스를 상속받는다.

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

### 10.3.6 믹스인

> 클래스 정의에 부모 클래스를 추가하여 상속받을 수 있다. 그러나 이를 헬퍼의 목적으로만 사용할 수 있다. 즉, 다른 상위 클래스와 메서드를 공유하지 않으며 이전 절에서 언급한 메서드 해석 순서의 모호성을 피한다.

> 이러한 부모 클래스를 믹스인(mixin) 클래스라고도 한다. 로깅과 같은 '사이드' 작업에서 이를 사용할 수 있다. 다음 예제는 객체 속성을 출력하는 믹스인 클래스다.

```python
class PrettyMixin():
	def dump(self):
		import pprint
		pprint.pprint(vars(self))

class Thing(PrettyMixin):
	pass

t = Thing()
t.name = "Nyarlathotep"
t.feature = "ichor"
t.age = "eldritch"
t.dump()
>>> {'age':'eldritch', 'feature':'ichor', 'name':'Nyarlathotep'}

```

## 10.4 자신:self

> 파이썬에서(공백 사용 외에) 어떤 한 비판은 인스턴스 메서드(이전 예제에서 봤던 메서드의 종류)의 첫 번째 인수로 self를 포함해야 한다는 것이다. 파이썬은 적절한 객체의 속성과 메서드를 찾기 위해 self 인수를 사용한다. 다음 예제에서 객체의 메서드를 어떻게 호출하고, 파이썬에서 실제로 은밀하게 무엇을 처리하는지 살펴보자.

```python
a_car = Car()
a_car.exclaim()
>>> I'm a Car!

```

> 파이썬이 은밀하게 처리하는 일은 다음과 같다.

- a_car 객체의 Car 클래스를 찾는다.
- a_car 객체를 Car 클래스 exclaim() 메서드의 self 매개변수에 전달한다.

> 단지 재미로, 다음과 같은 방법으로 메서드를 실행할 수 있다. 이것은 일반 car.exclaim() 구문과 똑같이 동작한다.

```python
Car.exclaim(a_car)
>>> I'm a Car!

```

## 10.5 속성 접근

### 10.5.2 Getter/Setter 메서드

> 파이썬에는 private 속성이 없지만 조금의 프라이버시를 얻기 위해서 애매한 속성 이름을 가진 Getter/Setter 메서드를 작성할 수 있다(가장 좋은 해결책은 다음 절에서 살펴볼 프로퍼티를 사용하는 것이다)

> 다음 예제에서는 hidden_name이라는 속성으로 Duck 클래스를 정의한다. 이 속성을 외부에서 직접 접근하지 못하도록 getter(get_name())과 setter(set_name()) 메서드를 정의한다. 각 메서드가 언제 호출되는지 알아보기 위해 print() 함수를 추가한다.

```python
class Duck():
	def __init__(self, input_name):
		self.hidden_name = input_name
	def get_name(self):
		print('inside the getter')
		return self.hidden_name
	def set_name(self, input_name):
		print('inside the setter')
		self.hidden_name = input_name

don = Duck('Donald')
don.get_name()
>>> inside the getter 'Donald'
don.set_name('Donna')
>>> inside the setter
don.get_name()
>>> inside the getter 'Donna'
```

### 10.5.3 속성 접근을 위한 프로퍼티

> 속성 프라이버시를 위한 파이써닉한 방법은 프로퍼티(property)를 사용하는 것이다.

#### 프로퍼티(property)란?

파이썬에서 **프로퍼티**는 "메서드처럼 동작하지만, 속성처럼 보이는" 특별한 기능이에요.  
즉, `obj.name`처럼 속성에 접근하는 문법을 쓰면서도, 사실은 내부적으로 **getter/setter 메서드**가 실행되도록 만드는 거죠.

---

#### 왜 필요한가?

- 그냥 속성을 직접 쓰면(`obj.hidden_name`) 내부 구현이 드러나 버려요.
- getter/setter 메서드를 쓰면(`obj.get_name()`, `obj.set_name()`) 코드가 장황해져요.
- 프로퍼티를 쓰면 **속성처럼 깔끔하게 보이면서도, 내부적으로는 메서드가 실행**돼서 안전하게 값을 관리할 수 있어요.

> 두 방법으로 프로퍼티를 사용할 수 있다. 첫 번째 방법으로 먼저 name = property(get_name, set_name) 구문을 클래스 정의 마지막 줄에 추가한다.

```python
class Duck():
	def __init(self, input_name):
		self.hidden_name = input_name
	def get_name(self):
		print('inside the getter')
		return self.hidden_name
	def set_name(self, input_name):
		print('inside the setter')
		self.hidden_name = input_name
	name = property(get_name, set_name)

name = property(get_name, set_name)
```

→ 이제 `don.name`을 쓰면 `get_name()`이 실행되고,  
 `don.name = "새 이름"`을 쓰면 `set_name()`이 실행돼요.

> Getter/Setter 메서드는 여전히 동작한다.
> 그러나 이제 속성 이름을 사용하여 hidden_name 속성을 가져오거나 설정할 수 있다.

```python
don = Duck('Donald')
don.name
>>> inside the getter 'Donald'
don.name = 'Donna'
>>> inside the setter
don.name
>>> inside the getter 'Donna'
```

> 두 번째 방법은 데커레이터를 추가하고, 두 메서드 이름(get_name, set_name)을 name으로 변경한다.

- getter 메서드 앞에 @property 데커레이터를 쓴다
- setter 메서드 앞에 @name.setter 데커레이터를 쓴다

```python
class Duck():
	def __init__(self, input_name):
		self.hidden_name = input_name
	@property
	def name(self):
		print('inside the getter')
		return self.hidden_name
	@name.setter
	def name(self, input_name):
		print('inside the setter')
		hidden_name = input_name

```

> 속성처럼 name에 접근할 수 있다.

```python
fowl = Duck('Howard')
fowl.name
>>> inside the getter 'Howard'
fowl.name = 'Donald'
>>> inside the setter
fowl.name
>>> inside the getter 'Donald'


```

### 10.5.4 계산된 값의 프로퍼티

> 이전 예제에서는 객체에 저장된 속성(hidden_name)을 참조하기 위해 name 프로퍼티를 사용했다.

> 프로퍼티는 계산된 값(computed value)을 참조할 수도 있다. radius 속성과 계산된 diameter 프로퍼티를 가진 Circle 클래스를 정의해보자.

```python
class Circle():
	def __init__(self, radius):
		self.radius = radius

	@property
	def diameter(self):
		return 2 * self.radius

```

> radius 속성의 초기값 5와 Circle 객체를 만든다.

```python
a = Circle(5)
a.radius
>>> 5

```

> radius와 같은 속성을 계산된 diameter 프로퍼티로 참조할 수 있다.

```python
a.diameter
>>> 10

```

> radius 속성은 언제든지 바꿀 수 있다. 그리고 diameter 프로퍼티는 현재 radius 값으로부터 계산된다.

```python
a.radius = 7
a.diameter
>>> 14

```

> 속성에 대한 setter 프로퍼티를 명시하지 않는다면 외부로부터 이 속성을 설정할 수 없다. 이것은 읽기전용(read-only) 속성이다.

```python
a.diameter = 20
>>> Traceback (most recent call last):
	File "<stdin>", line 1, in <module>
	AttributeError: can't set attribute

```

> 속성을 직접 접근하는 것보다 프로퍼티로 접근하면 여러 이점이 있다. 속성의 정의를 바꾼다면 모든 호출자를 수정할 필요 없이 클래스 정의에 있는 코드만 수정하면 된다.

---

#### 1. "계산된 값"이라는 말의 의미

보통 객체의 속성(Attribute)은 `self.radius = 5`처럼 어딘가에 값이 **저장**되어 있습니다.
하지만 `diameter`는 어떨까요? `self.diameter`라는 변수를 따로 메모리에 저장해두지 않아도, `radius` 값만 알면 언제든 계산해낼 수 있죠?

이렇게 **"실제 저장된 값은 아니지만, 저장된 다른 데이터를 조합해서 즉석에서 계산해내는 값"**을 **계산된 값(Computed Value)**이라고 부릅니다.

#### 2. 왜 일반 메서드(`def`) 대신 `@property`를 쓰나요?

#### ① 사용자의 입장에서 일관성 유지 (가장 큰 이유)

만약 `diameter`를 일반 메서드로 만들면, 사용자는 이를 호출할 때 `a.diameter()`라고 괄호를 붙여야 합니다.

- **변수일 때:** `a.radius` (속성 접근)
- **메서드일 때:** `a.diameter()` (함수 실행)

사용자는 이 속성이 '실제로 저장된 값'인지 '계산해서 나오는 값'인지 일일이 구분하기 귀찮습니다. **`@property`를 쓰면 속성처럼 `a.diameter`라고만 써도 내부에서 알아서 계산 함수가 실행**됩니다. 사용자는 그게 메서드인지 변수인지 신경 쓸 필요가 없죠.

#### ② 읽기 전용(Read-only) 제어

일반 메서드로 만들면 `a.diameter = 20`이라고 써도 파이썬은 에러를 내지 않습니다. 그냥 `diameter`라는 이름의 새로운 변수를 객체에 생성해버리죠.
하지만 `@property`를 사용하면, **setter를 따로 정의하지 않는 한 외부에서 값을 변경하려 할 때 파이썬이 즉시 `AttributeError`를 띄워 차단**해줍니다. "이 값은 외부에서 함부로 바꿀 수 없는 계산된 값이야!"라고 명시적으로 선언하는 효과가 있습니다.

#### ③ API 설계의 유연성 (추후 수정 용이)

처음에는 `self.radius = radius`로 직접 변수를 쓰다가, 나중에 코드가 복잡해져서 "반지름이 바뀔 때마다 로그를 찍어야지" 혹은 "계산 식을 바꿔야지"라고 생각할 때가 옵니다.

- **처음:** `self.radius` (변수)
- **나중에:** `self.radius`를 프로퍼티로 변경

이때 일반 메서드를 썼다면 외부 코드에서 `a.diameter()`라고 괄호를 붙여서 호출하던 곳을 전부 `a.diameter`로 고쳐야 합니다. 하지만 처음부터 `@property`로 설계해두었다면, **내부 구현만 바꾸고 밖에서 호출하는 방식(`a.diameter`)은 그대로 유지**할 수 있습니다. 유지보수 측면에서 엄청난 이점.

---

#### 요약하자면:

- **`def diameter(self): return 2 * self.radius`로 써도 작동은 합니다.** 다만, `a.diameter()`라고 괄호를 꼭 붙여야 합니다.
- **`@property`를 붙이면, 함수를 변수처럼 쓸 수 있습니다.**
  - 사용자에게는 "이것은 변수처럼 쓰면 돼"라는 약속을 하는 것이고,
  - 내부적으로는 "값이 바뀔 때나 호출될 때 제어 로직을 넣을 수 있는" 똑똑한 변수를 만드는 것입니다.

**결론:** 파이썬은 **"함수를 변수처럼 다루어 코드의 통일성과 캡슐화를 지키기 위해"** `@property`를 사용합니다. 단순히 값을 계산하는 것 이상의 '인터페이스 설계' 차원의 도구임.

### 10.5.5 프라이버시를 위한 네임 맹글링

> 이전 절의 Duck 클래스 예제에서 (완전하지 않지만) 숨겨진 hidden_name 속성을 호출했다. 파이썬은 클래스 정의 외부에서 볼 수 없도록 하는 속성에 대한 네이밍 컨벤션(naming convention)이 있다. 속성 이름 앞에 두 언더바(**)를 붙이면 된다.
> 다음과 같이 hidden_name을 **name으로 바꿔보자.

```python
class Duck():
	def __init__(self, input_name):
		self.__name = input_name
	@property
	def name(self):
		print('inside the getter')
		return self.__name
	@name.setter
	def name(self, input_name):
		print('inside the setter')
		self.__name = input_name

```

> \_\_name 속성에 바로 접근할 수 없다.

```python
fowl.__name
>>> AttributeError: 'Duck' object has no attribute '__name'
```

> 이 네이밍 컨벤션은 속성을 private로 만들지 않지만, 파이썬은 이 속성이 우연히 외부 코드에서 발견할 수 없도록 이름을 맹글링(mangling)했다. 사실 다음과 같이 접근할 수 있다.

```python
fowl._Duck__name
>>> 'Donald'
```

## 10.6 메서드 타입

> 어떤 메서드는 클래스의 일부이고, 어떤 메서드는 해당 클래스에서 작성된 객체의 일부이다. 어떤 메서드는 두 사항에 어느 것도 해당하지 않는다.

- 메서드 앞에 데커레이터가 없다면 이것은 인스턴스 메서드다. 첫 번째 인수는 객체 자신을 참조하는 `self`다.
- 메서드 앞에 `@classmethod` 데커레이터가 있다면 클래스 메서드다. 첫 번째 인수는 `cls`(또는 예약어인 class가 아닌 다른것)이다. 클래스 자체를 참조한다.
- 메서드 앞에 `@staticmethod` 데커레이터가 있다면 정적 메서드다. 첫 번째 인수는 위와 같이 자신의 객체나 클래스가 아니다.

### 10.6.1 인스턴스 메서드

> 일반적인 클래스를 생성할 때의 메서드 타입이다. 인스턴스 메서드의 첫 번째 매개변수는 self이고, 파이썬은 이 메서드를 호출할 때 객체를 전달한다. 인스턴스 메서드는 지금까지 예제에서 본 메서드이다.

### 10.6.2 클래스 메서드

> 대조적으로 클래스 메서드는 클래스 전체에 영향을 미친다. 클래스에 대한 어떤 변화는 모든 객체에 영향을 미친다. 클래스 정의에서 함수에 `@classmethod` 데커레이터가 있다면 이것은 클래스 메서드다. 또한 이 메서드의 첫 번째 매개변수는 클래스 자신이다. 파이썬에서는 보통 이 클래스의 매개변수를 cls로 쓴다. class는 예약어라서 사용할 수 없다. A 클래스에서 객체 인스턴스가 몇 개 만들어졌는지 알아보는 클래스 메서드를 정의해보자.

```python
class A():
	count = 0
	def __init__(self):
		A.count += 1
	def exlaim(self):
		print("I'm an A!")
	@classmethod
	def kids(cls):
		print("A has", cls.count, "little objects.")

easy_a = A()
breezy_a = A()
wheezy_a = A()
A.kids()
>>> A has 3 little objects.
easy_a.kids()
>>> A has 3 little objects.
```

### 10.6.3 정적 메서드

> 정적 메서드(static method)는 클래스나 객체에 영향을 미치지 못한다. 이 메서드는 단지 편의를 위해 존재한다. 정적 메서드는 @staticmethod 데커레이터가 있고, 첫 번째 매개변수로 self나 cls가 없다.

```python
class CoyoteWeapon():
	@staticmethod
	def commercial():
		print('This CoyoteWeapon has been brought to you by Acme')

CoyoteWeapon.commercial()
>>> This CoyoteWeapon has been brought to you by Acme'
```

> 이 메서드를 접근하기 위해 CoyoteWeapon 클래스에서 객체를 생성할 필요가 없다. 매우 클래시(class-y)하다.

---

### 클래스 메서드 vs 정적 메서드

둘 다 **"객체(인스턴스)를 생성하지 않고 호출할 수 있다"**는 공통점이 있습니다. 하지만 그 **'의도'**와 **'클래스 내부 정보에 접근할 수 있는지'**라는 측면에서 결정적인 차이가 있습니다.

왜 굳이 둘을 나누어 놓았는지 핵심 위주로 설명해 드릴게요.

---

#### 1. 차이점의 핵심: "클래스를 아느냐, 모르느냐"

- **클래스 메서드 (`@classmethod`):**
  - **클래스 정보를 알고 싶을 때 씁니다.**
  - `cls`라는 매개변수를 통해 클래스 자신(`A`)에 접근합니다. 즉, 클래스 변수를 읽거나 수정할 수 있습니다.
- **정적 메서드 (`@staticmethod`):**
  - **클래스와 아무 관련이 없습니다.**
  - 함수 내부에서 클래스나 인스턴스의 상태를 전혀 건드리지 않습니다. 그냥 "이 클래스라는 이름의 폴더 안에 넣어두면 관리하기 편하겠다" 싶은, 이름만 빌려온 함수입니다.

---

#### 2. 왜 정적 메서드를 따로 만들었을까? (쓸모)

정적 메서드는 **"클래스 안에 있지만, 클래스의 정보를 전혀 쓰지 않는 함수"**입니다. 굳이 클래스 안에 왜 넣을까요? **'연관성'** 때문입니다.

예를 들어, `CoyoteWeapon` 클래스와 관련된 유틸리티 함수(무기 설명 문구 출력 등)를 짠다고 해봅시다.

- 만약 클래스 밖의 일반 함수(`def commercial(): ...`)로 만들면, 이 함수가 `CoyoteWeapon`과 관련된 것인지 다른 클래스와 관련된 것인지 외부에서 알기 어렵습니다.
- 하지만 클래스 내부에 `@staticmethod`로 두면, **"이 함수는 `CoyoteWeapon`과 관련된 도구(Utility)구나"**라는 것을 개발자가 즉시 이해할 수 있게 됩니다. (관련된 기능을 한 곳에 모아두는 '이름공간' 역할)

---

#### 3. 클래스 메서드의 특별한 쓸모: "팩토리 메서드"

클래스 메서드는 객체를 생성하지 않고도 호출할 수 있다는 점을 이용해 **'팩토리 메서드(Factory Method)'**라는 아주 중요한 용도로 자주 쓰입니다.

예를 들어, "이름"만 알면 객체를 만들어주는 기능을 클래스 안에 넣고 싶다면 어떻게 할까요?

```python
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def margherita(cls):
        # 마르게리타 피자는 항상 이 재료를 쓴다고 가정할 때
        return cls(['mozzarella', 'tomatoes'])

# 객체를 만들지 않은 상태에서 마르게리타 피자 객체를 생성!
my_pizza = Pizza.margherita()
```

여기서 `margherita` 메서드는 클래스 메서드여야만 합니다. 왜냐하면 **`cls`를 통해 현재 클래스(`Pizza`)가 무엇인지 알고 있어야 그 클래스의 객체를 생성(`cls(...)`)할 수 있기 때문**입니다. 정적 메서드로는 `cls`를 받을 수 없으니 이런 기능을 구현할 수 없습니다.

---

#### 요약하자면

| 구분           | 클래스 메서드 (`@classmethod`)  | 정적 메서드 (`@staticmethod`)           |
| :------------- | :------------------------------ | :-------------------------------------- |
| **핵심 목적**  | 클래스 변수 사용, 팩토리 메서드 | 관련 로직을 클래스 안에 묶어두는 편의성 |
| **`cls` 인자** | 있음 (클래스 접근 가능)         | 없음 (클래스 접근 불가)                 |
| **연관성**     | 클래스와 긴밀함                 | 클래스와 관련 없음 (그냥 함수임)        |

**정리하자면:**

- 클래스의 상태(변수 등)를 써야 한다면 **`@classmethod`**
- 클래스나 객체의 상태를 쓸 필요는 없지만, 논리적으로 이 클래스와 한 몸처럼 묶여있어야 한다면 **`@staticmethod`**를 사용합니다.

파이썬이 이 둘을 나눈 이유는, **"함수가 클래스의 정보를 필요로 하는가?"**에 대해 명확하게 의도를 밝히고(가독성), 그에 맞는 적절한 기능을 제공하기 위함입니다.

## 10.7 덕 타이핑

> 파이썬은 다형성(polymorphism)을 느슨(loose)하게 구현했다. 이것은 클래스에 상관없이 같은 동작을 다른 객체에 적용할 수 있다는 것을 의미한다.

> 세 Quote 클래스에서 같은 `__init__()` 이니셜라이저를 사용해보자. 클래스에 다음 두 메서드를 추가한다.

- who() 메서드는 저장된 person 문자열의 값을 반환한다.
- says() 메서드는 특정 구두점과 함께 저장된 words 문자열을 반환한다.

```python
class Quote():
	def __init__(self, person, words):
		self.person = person
		self.words = words
	def who(self):
		return self.person
	def says(self):
		return self.words + '.'

class QuestionQuote(Quote):
	def says(self):
		return self.words + '?'

class ExclaimQuote(Quote):
	def says(self):
		return self.words + '!'

```

> QuestionQuote와 ExclaimQuote 클래스에서 초기화 함수를 쓰지 않았다. 그러므로 부모의 **init**() 메서드를 오버라이드하지 않는다. 파이썬은 자동으로 부모 클래스 Quote의 **init**() 메서드를 호출해서 인스턴스 변수 person과 words를 저장한다. 그러므로 자식 클래스 QuestionQuote와 ExclaimQuote에서 생성된 객체의 self.words에 접근할 수 있다.

```python
hunter = Quote('Elmer Fudd', "I'm hunting wabbits")
print(hunter.who(), 'says: ', hunter.says())
>>> Elmer Fudd says: I'm hunting wabbits.

hunted1 = QuestionQuote('Bugs Bunny', "What's up, doc")
print(hunted1.who(), 'says:', hunted1.says())
>>> Bugs Bunny says: What's up, doc?

...
```

> 세 개의 서로 다른 says() 메서드는 세 클래스에 대해 서로 다른 동작을 제공한다. 이것은 객체 지향 언어에서 전통적인 다형성의 특징이다. 더 나아가 파이썬은 who()와 says() 메서드를 갖고 있는 모든 객체에서 이 메서드를 실행할 수 있게 해준다.

```python
class BabblingBrook():
	def who(self):
		return 'Brook'
	def says(self):
		return 'Babble'

brook = BabblingBrook()

def who_says(obj):
	print(obj.who(), 'says:', obj.says())

who_says(hunter)
>>> Elmer Fudd says: I'm hunting wabbits.

who_says(hunted1)
>>> Bugs Bunny says: What's up, doc?
who_says(brook)
>>> Brook says Babble
```

> brook 객체는 다른 객체와 전혀 관계없다. 예전부터 이러한 행위를 duck typing이라고 불렀다.

> "만약 어떤 새가 오리처럼 걷고, 오리처럼 꽥꽥거린다면, 그 새는 오리다."

즉, **"그 객체가 어떤 클래스(타입)인지는 중요하지 않다. 필요한 메서드(기능)만 가지고 있다면, 내가 원하는 대로 작동할 수 있으니 오리로 취급하겠다"** 는 뜻입니다.

---

#### 전통적인 다형성 vs 덕 타이핑

- **전통적인 언어(Java, C++ 등):** 다형성을 쓰려면 반드시 **상속(Inheritance)**이나 **인터페이스(Interface)**가 필요합니다.
  - "이 객체는 `Animal`을 상속받았으니 `speak()` 메서드가 있을 거야"라고 컴파일러가 엄격하게 검사하죠.
- **파이썬(덕 타이핑):** **"상속? 인터페이스? 그런 건 몰라도 돼! 그냥 `who()`랑 `says()`만 가지고 있으면 돼!"**라고 봅니다.
  - 위 예시의 `BabblingBrook` 객체는 `Quote`와 혈연관계(상속)가 전혀 없지만, `who()`와 `says()`라는 이름의 메서드를 가지고 있기 때문에 `who_says()` 함수 입장에선 **완벽한 'Quote' 객체처럼 동작**하는 것입니다.

#### 왜 이렇게 하나요? (장점)

1.  **결합도의 제거:** 클래스 간의 관계를 억지로 묶어둘 필요가 없습니다. 부모 클래스를 미리 설계해둘 필요도 없죠. 그냥 나중에 나타난 새로운 클래스라도 필요한 메서드만 맞추면 바로 기존 시스템에 끼워 넣을 수 있습니다.
2.  **유연성(유지보수):** 기존 코드를 수정하지 않고도 새로운 기능을 확장하기가 매우 쉽습니다.
3.  **코드의 간결함:** 상속 구조를 복잡하게 고민하지 않아도 됩니다. "필요한 기능만 있으면 된다"는 아주 실용적인 사고방식입니다.

#### 주의할 점 (단점)

이 방식은 아주 강력하지만, **"타입 검사"를 컴파일 타임에 하지 않기 때문에 생기는 위험**도 있습니다.

예를 들어 `who_says(obj)` 함수를 만들었는데, 어떤 사람이 `who()` 메서드는 있지만 `says()` 메서드가 없는 객체를 던졌다고 해봅시다. 그러면 프로그램이 실행되는 도중에(Runtime) "AttributeError: 'XXX' object has no attribute 'says'"라며 **프로그램이 터지게 됩니다.**

#### 요약하자면:

- **덕 타이핑의 개념:** 객체의 **'형태(Type)'**보다 **'행동(Method)'**을 우선시하는 방식입니다.
- **다형성과의 관계:** 다형성을 실현하는 파이썬만의 아주 자유로운 방식입니다. 상속 관계가 아니더라도 같은 이름을 가진 메서드만 있으면 같은 동작을 수행하게 하는 것이죠.
- **왜 덕 타이핑인가:** "오리처럼 행동하면 오리다"라는 말처럼, 객체의 정체성(클래스)을 묻지 않고, 기대하는 행동(메서드)을 할 수 있는지만 보기 때문입니다.

파이썬 개발자들은 이 철학을 좋아합니다. **"복잡한 상속 트리 만들지 말고, 그냥 필요한 메서드만 제대로 만들어놔! 그럼 내가 알아서 쓸게!"**라는 실용적인 태도인 셈이죠.
