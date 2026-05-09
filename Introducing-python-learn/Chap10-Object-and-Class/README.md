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

## 10.8 매직 메서드

> a = 3 + 8 과 같은 무언사를 입력했을 때, 값 3과 8이 정수 객체고 + 기호로 더하라는 것을 어떻게 알까? name = "Daffy" + " " + "Duck"를 입력하면 문자열을 연결한다는 것을 어떻게 알까? 또한 = 기호를 사용하여 어떻게 결과를 얻을까? 파이썬의 특수 메서드를 사용하여 이러한 연산자를 사용할 수 있다.

> 이 메서드의 이름은 두 언더바로 시작하고 끝난다. 왜 그럴까? 이 이름은 개발자가 이렇게 변수 이름을 짓지 않을 것이다. 위에서 이미 **init**() 메서드를 사용했다. 이 메서드는 클래스의 정의로부터 생성된 새로운 객체를 초기화하고, 어떤 인수를 전달받는다. 간단한 Word 클래스와 두 단어를 비교(대소문자 무시)하는 equals() 메서드가 있다고 가정한다.

```python
class Word():
	def __init__(self, text):
		self.text = text
	def equals(self, word2):
		return self.text.lower() == word2.text.lower()

first = Word('ha')
second = Word('HA')
third = Word('eh')

first.equals(second)
>>> True
first.equals(third)
>>> False
```

> equals() 메서드를 특수 이름의 **eq**() 메서드로 바꿔보자

```python
class Word():
	def __init__(self, text):
		self.text = text

	def __eq__(self, word2):
		return self.text.lower() == word2.text.lower()

first = Word('ha')
second = Word('HA')
third = Word('eh')

first == second
>>> True
first == third
>>> False
```

> `__eq__()`는 같은지 판별하는 파이썬의 특수 메서드 이름이다.

| 메서드                        | 설명          |
| ----------------------------- | ------------- |
| \_\_eq\_\_(self, other)       | self==other   |
| \_\_ne\_\_(self, other)       | self!=other   |
| \_\_lt\_\_(self, other)       | self<other    |
| \_\_gt\_\_(self, other)       | self>other    |
| \_\_le\_\_(self, other)       | self<=other   |
| \_\_ge\_\_(self, other)       | self>=other   |
| \_\_add\_\_(self, other)      | self+other    |
| \_\_sub\_\_(self, other)      | self-other    |
| \_\_mul\_\_(self, other)      | self\*other   |
| \_\_floordiv\_\_(self, other) | self//other   |
| \_\_truediv\_\_(self, other)  | self/other    |
| \_\_mod\_\_(self, other)      | self%other    |
| \_\_pow\_\_(self, other)      | self\*\*other |
| \_\_str\_\_(self)             | str(self)     |
| \_\_repr\_\_(self)            | repr(self)    |
| \_\_len\_\_(self)             | len(self)     |

## 10.9 애그리게이션과 컴포지션

> 자식 클래스가 부모 클래스처럼 행동하고 싶을 때, 상속은 좋은 기술이다(자식 is-a 부모). 개발자는 정교한 상속 계층 구조에 유혹될 수 있지만, 컴포지션(composition) 혹은 애그리게이션(aggregation; X has-a Y)의 사용이 더 적절한 경우가 있다. 오리는 조류이지만(오리 is-a 조류, 상속), 꼬리를 갖고 있다(오리 has-a 꼬리, 컴포지션). 꼬리는 오리에 속하지 않지만 오리의 일부이다. 다음 예제에서는 부리(bill)와 꼬리(tail) 객체를 만들어서 새로운 오리(duck) 객체에 부여해보자.

```python
class Bill():
	def __init__(self, description):
		self.description = description

class Tail():
	def __init__(self, length):
		self.length = length

class Duck():
	def __init__(self, bill, tail):
		self.bill = bill
		self.tail = tail
	def about(self):
		print('This duck has a', self.bill.description, 'bill and a', self.tail.length, 'tail')

a_tail = Tail('long')
a_bill = Bill('wide orange')
duck = Duck(a_bill, a_tail)
duck.about()
>>> This duck has a wide orange bill and a long tail

```

> 애그리게이션은 관계를 표현하지만 조금 더 느슨하다. 한 객체는 다른 객체를 사용하지만, 둘 다 독립적으로 존재한다. 오리는 어느 한 호수에 있지만, 다른 호수에는 오리가 없다(호수는 오리의 일부가 아니다)

## 10.10 객체는 언제 사용할까?

> 클래스, 모듈의 사용 지침은 다음과 같다.

- 비슷한 행동(메서드)을 하지만 내부 상태(속성)가 다른 개별 인스턴스가 필요할 때, 객체는 매우 유용하다.
- 클래스는 상속을 지원하지만, 모듈은 상속을 지원하지 않는다.
- 어떤 한 가지 일만 수행한담녀 모듈이 가장 좋은 선택일 것이다. 프로그램에서는 파이썬 모듈이 참조된 횟수에 상관없이 단 하나의 복사본만 불러온다
- 여러 함수에 인수로 전달하는 여러 변수가 있다면, 클래스로 정의하는 것이 더 좋다. 예를 들어 화상 이미지를 나타내기 위해 size나 color를 딕셔너리의 키로 사용한다고 가정해보자. 프로그램에서는 각 이미지에 대한 딕셔너리를 생성하고, scale()과 transform() 같은 함수에 인수를 전달할 수 있다. 키와 함수를 추가하면 코드가 지저분해질 수도 있다. size와 color를 속성으로 하고 scale()과 transfor()을 메서드로 하는 이미지 클래스를 정의하는 것이 더 일관성이 있다. 색상 이미지에 대한 모든 데이터와 메서드를 한 곳에 정의할 수 있기 때문이다.
- 가장 간단한 문제 해결법을 사용한다. 딕셔너리, 리스트, 튜플은 모듈보다 더 작고 간단하며 빠르다. 그리고 일반적으로 모듈은 클래스보다 더 간단하다.

> **귀도의 조언**
> 자료구조를 과하게 엔지니어링하는 것을 피해야 한다. 객체보다 튜플이 더 낫다(네임드 튜플을 써보라). getter/setter 함수보다 간단한 field 가 더 낫다 ...(중략)... 내장된 데이터 타입은 우리 친구다. 숫자, 문자열, 튜플, 리스트, 셋, 딕셔너리를 사용하라. 또한 데크와 같은 컬렉션 라이브러리를 활용하라.

- 새로운 대안은 데이터 클래스다.

---

### 모듈 vs 클래스

#### 1. 목적의 차이

- **모듈(Module):** 그냥 **파일 하나**입니다. 함수나 변수들을 단순히 한 파일에 모아놓은 것입니다. "이 파일에 있는 기능들을 가져다 써라"는 수준의 **정적(Static)인 도구**입니다.
- **클래스(Class):** **'틀(Blueprint)'**입니다. 단순히 기능을 모아두는 게 아니라, **"상태(데이터)를 가진 개체(Object)를 얼마나 많이 만들 것인가?"**를 고민하는 도구입니다.

#### 2. 왜 모듈이 더 간단한가?

**① '상태(State)'를 관리할 필요가 없습니다.**

- **클래스**는 `self.radius = 10`처럼 객체마다 다른 데이터를 유지해야 합니다. 이를 위해 인스턴스화(`__init__`)하고, 메모리 관리하고, `self`를 통해 데이터에 접근하는 등 **상태 관리 로직**이 복잡합니다.
- **모듈**은 그냥 함수들의 집합입니다. 모듈 안에 `count = 0` 같은 변수를 하나 두면 프로그램 전체에서 딱 하나만 존재합니다. 복잡한 인스턴스 생성 과정이 필요 없습니다.

**② 복잡한 문법이 없습니다.**

- 클래스를 쓰려면 상속, 다형성, 캡슐화, `self`의 개념, 생성자, 소멸자 등을 이해해야 합니다.
- 모듈은 그냥 파일 하나를 만들고 `import` 하면 끝입니다. `self`를 붙일 필요도 없고, 상속을 고민할 필요도 없습니다.

**③ 코드의 복잡도(Overhead)**

- 클래스는 '객체'라는 실제 메모리 덩어리를 생성하고 관리하는 비용이 듭니다. 반면 모듈은 프로그램이 시작될 때 딱 한 번 메모리에 올라가면 끝입니다(싱글톤). 그래서 훨씬 가볍고 빠릅니다.

---

#### 3. 쉬운 비유: 도서관 vs 공장

- **모듈은 '도서관' 같습니다.**
  - 도서관이라는 건물(모듈)에 가서 책(함수)을 꺼내 읽기만 하면 됩니다. 건물을 새로 짓거나(인스턴스 생성), 책을 복제할 필요가 없죠. **단순히 가져다 쓰면 끝입니다.**
- **클래스는 '공장' 같습니다.**
  - 공장(클래스) 설계도를 만들고, 거기서 제품(인스턴스)을 찍어내야 합니다. 어떤 제품은 빨간색이고, 어떤 제품은 파란색이어야 하죠(상태 관리). 공장을 운영하려면 설계도도 복잡하고, 제품 관리도 해야 하니 훨씬 **무겁고 어렵습니다.**

---

#### 4. 결론: "모듈이 더 간단하다"는 말의 의미

**"굳이 복잡하게 객체를 만들어서 상태를 관리할 필요가 없는 기능이라면, 괜히 클래스 만들지 말고 그냥 파일 하나(모듈)에 함수들 넣어서 써라"**라는 뜻입니다.

- 데이터가 계속 변하고, 그 데이터를 가진 객체가 여러 개 필요하다 → **클래스**
- 그냥 공용으로 쓸 함수 묶음이 필요하다 (예: 수학 계산, 로그 출력 등) → **모듈**

파이썬의 철학은 **"할 수 있는 가장 단순한 방법을 택하라"**입니다.
클래스라는 무거운 도구는 꼭 필요한 곳(객체 지향이 필요할 때)에만 쓰고, 그게 아니라면 모듈이나 내장 자료형(리스트, 딕셔너리 등)을 사용하는 게 훨씬 쉽고 빠르다는 뜻입니다.

## 10.11 네임드 튜플

> 네임드 튜플은 튜플의 서브 클래스다. 이름(.name)과 위치([offset])로 값에 접근할 수 있다.

> Duck 클래스를 네임드 튜플로, bill과 tail을 간단한 문자열 속성으로 변환한다. 그리고 두 인수를 취하는 namedtuple 함수를 호출한다.

- 이름
- 스페이스로 구분된 필드 이름 문자열

```python
from collection import namedtuple
Duck = namedtuple('Duck', 'bill tail')
duck = Duck('wide orange', 'long')
duck
>>>Duck(bill='wide orange', tail='long')
duck.bill
>>> 'wide orange'
duck.tail
>>> 'long'

parts = {'bill':'wide orange', 'tail':'long'}
duck2 = Duck(**parts)
duck2
>>> Duck(bill='wide orange', tail='long')

```

> `**parts` 는 키워드 인수다. parts 딕셔너리에서 키와 값을 추출하여 Duck()의 인수로 제공한다. 다음 예제와 효과가 같ㄴ다.

`duck2 = Duck(bill= 'wide orange', tail = 'long')`

> 네임드 튜플은 불변이다. 하지만 필드를 바꿔서 또 다른 네임드 튜플을 반환할 수 있다.

```python
duck3 = duck2._replace(tail='magnificent', bill='crushing')
duck3
>>> Duck(bill='crushing', tail='magnificent')
```

네임드 튜플의 특징을 정리하면 다음과 같다.

- 불변 객체처럼 행동한다.
- 객체보다 공간 효율성과 시간 효율성이 좋다.
- 딕셔너리 형식의 대괄호([]) 대신, 온점(.) 표기법으로 속성을 접근할 수 있다.
- 네임드 튜플을 딕셔너리의 키처럼 쓸 수 있다.

---

### 네임드 튜플 vs 클래스

네임드 튜플(Named Tuple)은 **"데이터만 담고 있으면 되는데, 굳이 클래스까지 만들어야 하나?"**라는 고민에 대한 파이썬의 해답입니다.

#### 1. 왜 클래스 대신 네임드 튜플을 쓸까요?

보통 `Duck` 같은 클래스를 만들 때, 우리는 이렇게 짭니다.

```python
class Duck:
    def __init__(self, bill, tail):
        self.bill = bill
        self.tail = tail

duck = Duck('wide orange', 'long')
```

이 코드는 **"객체 지향적"**이지만, 사실 `__init__` 함수도 만들어야 하고, 나중에 객체가 많아지면 메모리도 꽤 차지합니다. 만약 이 클래스가 별도의 복잡한 메서드 없이 **"데이터만 저장하는 역할"**만 한다면, 클래스는 지나치게 무거운 도구입니다.

이때 **네임드 튜플**을 쓰면 한 줄로 끝납니다.

```python
from collections import namedtuple
Duck = namedtuple('Duck', 'bill tail')
duck = Duck('wide orange', 'long')
```

#### 2. 네임드 튜플 vs 클래스 (차이점)

| 특징        | 클래스 (Class)                     | 네임드 튜플 (Named Tuple)     |
| :---------- | :--------------------------------- | :---------------------------- |
| **코드 양** | 길다 (생성자 정의 등)              | 짧다 (한 줄 선언)             |
| **메모리**  | 무겁다 (객체마다 별도의 공간 점유) | 가볍다 (튜플 기반이라 효율적) |
| **가변성**  | 가변 (값 변경 가능)                | **불변 (값 변경 불가)**       |
| **용도**    | 복잡한 동작(메서드)이 있을 때      | **순수하게 데이터만 담을 때** |

#### 3. 왜 네임드 튜플을 쓰면 좋은가?

1.  **가독성:** 그냥 튜플(`('wide orange', 'long')`)을 쓰면 `a[0]`, `a[1]`로 접근해야 해서 무엇이 부리(`bill`)고 무엇이 꼬리(`tail`)인지 헷갈립니다. 네임드 튜플은 `duck.bill`처럼 이름으로 접근하니 훨씬 명확합니다.
2.  **효율성:** 클래스 객체는 파이썬이 관리하는 여러 정보(`__dict__` 등)를 내부에 저장하느라 메모리를 많이 먹습니다. 네임드 튜플은 이름 그대로 '튜플'이라서 메모리를 훨씬 적게 씁니다.
3.  **불변성(Immutability):** 데이터가 중간에 바뀌면 안 되는 설정값이나, API에서 받아온 데이터 같은 경우 네임드 튜플을 쓰면 실수로 값을 수정하는 버그를 방지할 수 있습니다.

---

#### 4. "불변"인데 왜 수정이 되나요? (`_replace`)

네임드 튜플은 "불변(Immutable)"이라서 `duck.bill = 'small'`처럼 직접 수정은 불가능합니다. 그런데 데이터 수정이 필요할 때가 있죠? 그래서 파이썬은 **기존 데이터를 복사해서 새로운 값을 반영한 새 튜플을 만들어주는** `_replace`라는 편의 기능을 제공합니다.

```python
duck3 = duck2._replace(tail='magnificent')
```

이것은 `duck2`를 바꾼 게 아니라, `duck2`를 기반으로 'tail'만 바뀐 새로운 튜플 `duck3`를 만든 것입니다.

#### 요약하자면:

- **언제 클래스를 쓰나요?** 내부에서 복잡한 계산을 수행하거나, 값을 수시로 바꿔야 할 때.
- **언제 네임드 튜플을 쓰나요?** **데이터를 담아서 전달하는 용도가 주 목적일 때.** (예: 데이터베이스에서 가져온 한 줄의 정보, 설정값 묶음, API 통신으로 받은 결과값 등)

"클래스를 쓸까?" 고민될 때, **"내부에 메서드가 없고 그냥 데이터만 담는 거라면?" -> "네임드 튜플이 답이다!"** 라고 생각하시면 아주 좋습니다. 이것이 바로 파이썬식 '데이터 구조 관리'입니다.

### 네임드 튜플 인자

`namedtuple` 함수를 호출할 때 사용하는 두 가지 주요 인자는 다음과 같습니다.

#### 1. 첫 번째 인자: 클래스 이름

- **역할:** 새로 만들어질 튜플의 **자료형 이름(클래스 이름)**입니다.
- **특징:** 파이썬 코드에서 출력할 때 이 이름이 그대로 표시됩니다.
- 예: `Duck = namedtuple('Duck', ...)`이라고 하면, 객체를 만들었을 때 `Duck(...)`이라는 이름으로 나타납니다.

#### 2. 두 번째 인자: 속성(필드) 이름들

- **역할:** 튜플 안에 들어갈 각 데이터의 **이름표**를 정의합니다.
- **구분 방식:** 질문하신 대로 **공백(스페이스)**으로 구분합니다.
  - 예: `'bill tail'` (공백으로 구분된 문자열)
- **대안:** 공백으로 구분하는 문자열 대신 **리스트**를 전달해도 똑같이 작동합니다.
  - 예: `['bill', 'tail']`

---

#### 예시 비교

둘 다 결과는 똑같습니다.

**방법 A: 공백으로 구분된 문자열 사용 (가장 흔한 방식)**

```python
from collections import namedtuple
Point = namedtuple('Point', 'x y z')
p = Point(1, 2, 3)
# 출력: Point(x=1, y=2, z=3)
```

**방법 B: 리스트 사용**

```python
Point = namedtuple('Point', ['x', 'y', 'z'])
p = Point(1, 2, 3)
# 출력: Point(x=1, y=2, z=3)
```

#### 왜 이렇게 하나요?

파이썬은 개발자가 타이핑을 적게 하면서도 읽기 편하게 만들려고 노력합니다.

- `'x y z'`라고 쓰면 `['x', 'y', 'z']`라고 일일이 따옴표와 콤마를 찍는 것보다 훨씬 타이핑이 빠르고 깔끔해 보이기 때문입니다.

**주의할 점:**

- 속성 이름은 파이썬의 **변수 이름 규칙**을 따라야 합니다. (숫자로 시작하면 안 되고, 공백이나 특수문자가 포함되면 안 됩니다.)
- 이름들 사이에는 반드시 **공백**을 한 칸 이상 두어야 합니다. (`'bill tail'`은 되지만 `'bill,tail'` 처럼 콤마를 쓰면 오류가 나거나 의도치 않은 이름이 될 수 있습니다.)

## 10.12 데이터 클래스

> 많은 개발자는 행동(메서드)이 아니라 주로 데이터(속성)를 저장하기 위해 객체 생성하는 것을 선호한다. 이전 절에서 이를 대체할 수 있는 네임드 튜플을 살펴봤다. 파이썬 3.7부터는 데이터 클래스를 지원한다.

> name 속성을 가진 보통 객체는 다음과 같다.

```python
class TeenyClass():
	def __init__(self, name):
		self.name = name

teeny = TeenyClass('itsy')
teeny.name
>>> 'itsy'
```

> 데이터 클래스를 사용하여 같은 작업을 한다면 조금 다르게 보인다.

```python
from dataclass import dataclass
@dataclass
class TeenyDataClass:
	name: str

teeny = TeenyDataClass('bitsy')
teeny.name
>>> 'bitsy'
```

> @dataclass 데커레이트 외에 name: type(이름: 타입), 예를 들면 color:str 또는 color: str = "red" 와 같은 형식의 변수 어노테이션을 사용하여 클래스 속성을 정의한다. 타입은 str 또는 int와 같은 내장 클래스뿐만 아니라 사용자가 생성한 클래스를 포함한 모든 파이썬 객체 타입일 수 있다.

> 데이터 클래스 객체를 생성할 때, 클래스에 지정된 순서대로 인수를 제공하거나 이름이 지정된 인수를 임의의 순서로 제공한다.

```python
from dataclasses import dataclass
@dataclass
class AnimalClass:
	name: str
	habitat: str
	teeth: int = 0

snowman = AnimalClass('yeti', 'Himalays', 46)
duck = AnimalClass(habitat='lake', name='duck')

snowman
>>> AnimalClass(name='yeti', habitat='Himalayas', teeth=46)
duck
>>> AnimalClass(name='duck', habitat='lake', teeth=0)
```

> AnimalClass 클래스에서 teeth 속성의 기본 값을 정의해서 객체를 생성할 때 teeth 속성을 제공하지 않아도 된다.

### 클래스 vs 네임드 튜플 vs 데이터 클래스

클래스, 네임드 튜플, 데이터 클래스 세 가지가 비슷해 보여서 혼란스러울 수 있습니다. 사실 이들은 **"데이터를 담는 주머니"**라는 공통점이 있지만, **"어느 정도의 자유도와 기능을 원하는가"**에 따라 명확하게 구분됩니다.

결정 장애를 없애드리기 위해 상황별로 정리해 드릴게요.

---

#### 1. 한눈에 보는 비교표

| 구분          | 클래스 (일반)         | 데이터 클래스 (@dataclass)  | 네임드 튜플 (namedtuple)    |
| :------------ | :-------------------- | :-------------------------- | :-------------------------- |
| **핵심 용도** | 복잡한 로직/상태 관리 | 데이터 관리 + 약간의 로직   | 순수 데이터 보관 (불변)     |
| **코드 양**   | 많음 (init 정의 필수) | 적음 (데코레이터 자동 생성) | 매우 적음 (한 줄 선언)      |
| **값 변경**   | 가능                  | 가능                        | **불가능 (불변)**           |
| **기능**      | 자유로움 (뭐든 가능)  | 편의 메서드 자동 생성       | 메모리 효율 최고, 튜플 호환 |

---

#### 2. 상황별 추천 가이드

##### ① 일반 클래스: "복잡한 행동이 필요할 때"

- **언제?** 단순히 데이터를 담는 수준을 넘어, 복잡한 로직을 수행하거나, 인스턴스마다 내부 상태를 정교하게 관리해야 할 때.
- 예: 게임의 '캐릭터' 클래스 (상태값도 있지만, 공격/이동/레벨업 등 메서드가 많음)

##### ② 데이터 클래스 (@dataclass): "데이터 중심이지만 유연함이 필요할 때" (가장 추천!)

- **언제?** **대부분의 상황.** 파이썬 3.7 이후 가장 권장되는 방식입니다. 데이터를 담는 것이 주 목적이지만, 필요하다면 메서드를 추가해서 로직을 넣을 수도 있고, 값을 중간에 수정할 수도 있습니다.
- **장점:** `__init__`, `__repr__`(출력 기능) 등을 파이썬이 알아서 만들어줍니다. '기본값' 지정도 매우 쉽습니다.
- 예: 웹 서비스의 '사용자 정보', '상품 정보' 등 (데이터가 중심이고, 가끔 '할인 가격 계산' 같은 간단한 메서드를 추가하고 싶을 때)

##### ③ 네임드 튜플: "메모리가 중요하거나 데이터가 변하면 안 될 때"

- **언제?**
  1.  **메모리 효율:** 수백만 개의 객체를 만들어야 해서 최대한 가벼워야 할 때.
  2.  **데이터 무결성:** "이 데이터는 절대 바뀌면 안 돼!"라는 보장이 필요할 때(Immutable).
  3.  **튜플 호환:** 기존에 튜플을 반환하던 함수를 수정할 때 유용합니다. (기존 함수가 튜플을 반환하고 있다면, 네임드 튜플로 바꾸기만 해도 코드를 안 깨뜨리고 이름으로 접근할 수 있게 됩니다.)
- 예: 데이터베이스에서 가져온 한 줄의 결과값, 함수의 반환값 묶음.

---

#### 3. 실무적인 선택 전략 (의사결정 트리)

1.  **값이 바뀌면 안 되나?**
    - **Yes:** **네임드 튜플** 선택.
    - **No:** 다음 단계로.

2.  **메서드(동작)가 많이 필요한가?**
    - **Yes:** **일반 클래스** 선택.
    - **No:** 다음 단계로.

3.  **그럼 데이터 클래스(@dataclass)를 선택하세요.**
    - 대부분의 경우 `@dataclass`가 가장 생산성이 좋습니다.
    - "나는 클래스를 만들기 귀찮지만, 값이 수정 가능해야 하고, 추후에 메서드를 붙일 수도 있을 것 같다"면 고민할 것 없이 **데이터 클래스**입니다.

#### 요약하자면:

- **일반 클래스**는 "공장(기능 중심)"
- **데이터 클래스**는 "편리한 데이터 보관함(데이터 중심)"
- **네임드 튜플**은 "가벼운 데이터 포장지(불변/효율 중심)"

라고 생각하시면 됩니다. **요즘 파이썬 트렌드는 가급적 `@dataclass`를 적극적으로 활용해서 `__init__`을 수동으로 작성하는 노가다를 줄이는 것입니다.**
