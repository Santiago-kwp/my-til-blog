# 2장. 코틀린 기초

## 2.1 기본 요소: 함수와 변수

```kotlin
fun main(args: Array<String>) {
    println("Hello, world!")
}
```

- 파라미터 이름 뒤에 그 파라미터의 타입을 쓴다. 변수를 선언할 때도 마찬가지 방식으로 타입을 지정한다.
- 함수를 최상위 수준에 정의할 수 있다. (자바와 달리) 꼭 클래스 안에 함수를 넣어야 할 필요가 없다.

```kotlin
fun max(a: Int, b: Int) : Int {
    return if (a > b) a else b
}
```

- kotlin의 `if`는 문장이 아니고 결과를 만드는 식(expression)이다.

### 문(statement)와 식(expression)의 구분

> 코틀린에서 if는 식이지 문이 아니다. 식은 값을 만들어 내며 다른 식의 하위 요소로 계산에 참여할 수 있는 반면 문은 자신을 둘러싸고 있는 가장 안쪽 블록의 최상위 요소로 존재하며 아무런 값을 만들어내지 않는다는 차이가 있다. 자바에서 모든 제어 구조가 문인 반면 코틀린에서는 루프를 제외한 대부분의 제어 구조가 식이다.
> 반면 대입문은 자바에서는 식이었으나 코틀린에서는 문이 됐다. 그로 인해 자바와 달리 대입식과 비교식을 잘못 바꿔 써서 버그가 생기는 경우가 없다.

### 식이 본문인 함수

```kotlin
fun max(a: Int, b: Int) : Int = if (a>b) a else b

fun max(a: Int, b: Int) = if (a>b) a else b
```

> 본문이 중괄호로 둘러싸인 함수를 블록이 본문인 함수라 부르고, 등호와 식으로 이뤄진 함수를 식이 본문인 함수라고 부른다.

- 인텔리J 아이디어는 이 두 방식의 함수를 서로 변환하는 메뉴가 있다. 각각은 Convert to expression body 와 Convert to block body이다.

- 코틀린은 정적 타입 지정 언어이므로 컴파일 시점에 모든 식의 타입을 지정해야 한다. 실제로 모든 변수나 모든 식에는 타입이 있으며, 모든 함수는 반환 타입이 정해져야 한다. 하지만 식이 본문인 함수의 경우 굳이 사용자가 반환 타입을 적지 않아도 컴파일러가 함수 본문 식을 분석해서 식의 결과 타입을 함수 반환 타입으로 정해준다. 이렇게 컴파일러가 타입을 분석해 프로그래머 대신 프로그램 구성 요소의 타입을 정해주는 기능을 **타입 추론(type inference)**이라고 부른다.

### 변경 가능한 변수와 변경 불가능한 변수

- val : 변경 불가능한(immutable) 참조를 저장하는 변수다. val로 선언된 변수는 일단 초기화하고 나면 재대입이 불가능하다. 자바로 말하자면 final 변수에 해당한다.
- var : 변경 가능한(mutable) 참조다. 이런 변수의 값은 바뀔 수 있다. 자바의 일반 변수에 해당한다.
- 기본적으로는 모든 변수를 val 키워드를 사용해 불변 변수로 선언하고, 나중에 꼭 필요할 때에만 var로 변경하라.
- val 참조 자체는 불변일지라도 그 참조가 가리키는 객체의 내부 값은 변경될 수 있다는 사실을 기억하라.

```kotlin
val languages = arrayListOf("Java")
languages.add("Kotlin")
```

- var 키워드를 사용하면 변수의 값은 변경할 수 있지만, 변수의 타입은 고정돼 바뀌지 않는다. 예를 들어 다음 코드는 컴파일할 수 없다.

```kotlin
var answer = 42
answer = "no answer"
```

- 컴파일러는 변수 선언 시점의 초기화 식으로부터 변수의 타입을 추론하며, 변수 선언 이후 변수 재대입이 이뤄질 때는 이미 추론한 변수의 타입을 염두에 두고 대입문의 타입을 검사한다.

### 문자열 템플릿

```kotlin
fun main(args: Array<String>) {
    val name = if (args.size > 0) args[0] else "Kotlin"
    println("Hello, $name!")
}
```

- 위 예제는 문자열 템플릿(String template)이라는 기능을 보여준다. 이 코드는 name이라는 변수를 선언하고 그 다음 줄에 있는 문자열 리터럴 안에서 그 변수를 사용했다. 여러 스크립트 언어와 비슷하게 코틀린에서도 변수를 문자열 안에 사용할 수 있다. 문자열 리터럴의 필요한 곳에 변수를 넣되 변수 앞에 `$`를 추가해야 한다.
- 이 문자열 템플릿은 자바의 문자열 접합 연산("Hello, " + name + "!")과 동일한 기능을 하지만 좀 더 간결하며, 자바 문자열 접합 연산을 사용한 식과 마찬가지로 효율적이다.
- 물론 컴파일러는 각 식을 정적(static)으로 (컴파일 시점)에 검사하기 때문에 존재하지 않는 변수를 문자열 템플릿 안에서 사용하면 컴파일 오류가 발생한다.
- `$` 문자를 문자열에 넣고 싶으면 println("\$x")와 같이 \를 사용해 $를 이스케이프시켜야 한다.
- 문자열 템플릿 안에 사용할 수 있는 대상은 간단한 변수 이름만으로 한정되지 않는다. 복잡한 식도 중괄호({})로 둘러싸서 문자열 템플릿 안에 넣을 수 있다.

```kotlin
fun main(args: Array<String>) {
    if (args.size > 0) {
        println("Hello, ${args[0]}!")
    }
}
```

### 한글을 문자열 템플릿에서 사용할 경우 주의할 점

> 코틀린에서는 자바와 마찬가지로 한글(사실은 한글 뿐 아니라 '글자(letter)'로 분류할 수 있는 모든 유니코드 문자)을 식별자에 사용할 수 있으므로 변수 이름에 한글이 들어갈 수 있다. 그런 유니코드 변수 이름으로 인해 문자열 템플릿을 볼 때 오해가 생길 수 있다. 문자열 템플릿 안에 $로 변수를 지정할 때 변수명 바로 뒤에 한글을 붙여서 사용하면 코틀린 컴파일러는 영문자와 한글을 한꺼번에 식별자로 인식해서 unresolved reference 오류를 발생시킨다.

> 이 문제를 해결하는 방법은 '${name}님 반가워요!'처럼 변수 이름을 {}로 감싸는 것이다. 문자열 템플릿 안에서 변수 이름만 사용하는 경우라도 ${name}처럼 중괄호로 변수명을 감싸는 습관을 들이면 더 좋다. 필요할 때 정규식 등을 통해 검색하거나 일괄 변환할 때도 중괄호를 쓴 경우 처리가 더 쉽고, 코드를 사람이 읽을 때도 문자열 템플릿 안에서 변수가 쓰인 부분을 더 쉽게 식별할 수 있다.

- 중괄호로 둘러싼 식 안에서 큰 따옴표를 사용할 수도 있다. 심지어 중괄호로 둘러싼 식 안에서 문자열 템플릿을 사용해도 된다.
  - `${if (s.length>2) "too short" else "normal string ${s}"}`

```kotlin
fun main(args: Array<String>) {
    println("Hello, ${if (args.size > 0) args[0] else "someone"}!")
}
```

## 2.2 클래스와 프로퍼티

> 시작하기 위해 간단한 자바빈 클래스인 Person을 정의하자. Person에는 name이라는 프로퍼티만 들어있다.

```java
public class Person{
    private final String name;
    public Person(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

자바-코틀린 변환기는 자바 코드를 같은 일을 하는 코틀린 코드로 자동으로 변환해준다. 변환기를 써서 방금 본 Person 클래스를 코틀린으로 변환해보자.

```kotlin
class Person(val name: String)
```

- 이런 유형의 클래스(코드가 없이 데이터만 저장하는 클래스)를 값 객체(value object)라 부르며, 다양한 언어가 값 객체를 간결하게 기술할 수 있는 구문을 제공한다.
- 자바를 코틀린으로 변환한 결과, public 가시성 변경자(visibility modifier)가 사라졌음을 확인하라. 코틀린의 기본 가시성은 public이므로 이런 경우 변경자를 생략해도 된다.

### 2.2.1 프로퍼티

> 클래스라는 개념의 목적은 데이터를 캡슐화(encapsulate)하고 캡슐화한 데이터를 다루는 코드를 한 주체 아래 가두는 것이다. 자바에서는 데이터를 필드(field)에 저장하며, 멤버 필드의 가시성은 보통 비공개(private)다. 클래스는 자신을 사용하는 클라이언트가 그 데이터에 접근하는 통로로 쓸 수 있는 접근자 메소드(accessor method)를 제공한다. 보통은 필드를 읽기 위한 게터를 제공하고 필드를 변경하게 허용해야 할 경우 세터를 추가 제공할 수 있다. 세터는 자신이 받은 값을 검증하거나 필드 변경을 다른 곳에 통지하는 등의 로직을 더 가질 수 있다.

> 자바에서는 필드와 접근자를 한데 묶어 프로퍼티라고 부르며, 프로퍼티라는 개념을 활용하는 프레임워크가 많다. 코틀린은 프로퍼티를 언어 기본 기능으로 제공하며, 코틀린 프로퍼티는 자바의 필드와 접근자 메소드를 완전히 대신한다. 클래스에서 프로퍼티를 선언할 때는 앞에서 살펴본 변수를 선언하는 방법과 마찬가지로 val이나 var를 사용한다. val로 선언한 프로퍼티는 읽기 전용이며, var로 선언한 프로퍼티는 변경 가능하다.

```kotlin
class Person(
    val name: String, // 읽기 전용 프로퍼티로, 코틀린은 (비공개) 필드와 필드를 읽는 단순한 (공개) 게터를 만들어낸다.
    var isMarried: Boolean
)
// var isMarried -> 쓸 수 있는 프로퍼티로, 코틀린은 (비공개) 필드, (공개) 게터, (공개) 세터를 만들어낸다.
```

- 자바와 코틀린에서 정의한 Person 클래스 중 어느 쪽을 사용해도 이 코드를 바꿀 필요가 없다는 사실을 기억하라. 코틀린의 name 프로퍼티를 자바 쪽에서는 getName이라는 이름으로 불 수 있다. 게터와 세터의 이름을 정하는 규칙에는 예외가 있다. 이름이 is로 시작하는 프로퍼티의 게터에는 get이 붙지 않고 원래 이름을 그대로 사용하며, 세터에는 is를 set으로 바꾼 이름을 사용한다. 따라서 자바에서 isMarried 프로퍼티의 게터를 호출하려면 `isMarried()`를 사용해야 한다.

자바에서 Person 클래스를 사용하는 방법

```java
>>> Person person = new Person("Bob", true);
>>> System.out.println(person.getName());
Bob
>>> System.out.printlng(person.isMarried());
true
```

코틀린에서 Person 클래스 사용하기

```kotlin
>>> val person = Person("Bob", true)
>>> println(person.name)
Bob
>>> println(person.isMarried)
true
```

- 게터를 호출하는 대신 프로퍼티를 직접 사용했음에 유의하라. 로직은 동일하지만 코드는 더 간결해졌다. 변경 가능한 프로퍼티의 세터도 마찬가지 방식으로 동작한다. 자바에서는 `person.setMarried(false)`로 어떤 사람이 이혼했다는 사실을 기록하지만, 코틀린에서는 `person.isMarried = false`로 쓴다.

### 2.2.2 커스텀 접근자

> 직사각형 클래스인 Rectangle을 정의하면서 자신이 정사각형인지 알려주는 기능을 만들어보자. 직사각형이 정사각형인지를 별도의 필드에 저장할 필요가 없다.
> 사각형의 너비와 높이가 같은지 검사하면 정사각형 여부를 그때그때 알 수 있다.

```kotlin
class Rectangle(val height: Int, val width: Int) {
    val isSquare: Boolean
        get() { // 프로퍼티 게터 선언
            return height == width
        }
}
```

- isSquare 프로퍼티에는 자체 값을 저장하는 필드가 필요 없다. 이 프로퍼티에는 자체 구현을 제공하는 게터만 존재한다. 클라이언트가 프로퍼티에 접근할 때마다 게터가 프로퍼티 값을 매번 다시 계산한다.
  `println(rectangle.isSquare)`

### 2.2.3 코틀린 소스코드 구조: 디렉터리와 패키지

> 자바의 경우 모든 클래스를 패키지 단위로 관리한다. 코틀린에도 자바와 비슷한 개념의 패키지가 있다. 모든 코틀린 파일의 맨 앞에 package 문을 넣을 수 있다. 그러면 그 파일 안에 있는 모든 선언(클래스, 함수, 프로퍼티 등)이 해당 패키지에 들어간다. 같은 패키지에 속해 있다면 다른 파일에서 정의한 선언일지라도 직접 사용할 수 있다. 반면 다른 패키지에 정의한 선언을 사용하려면 임포트를 통해 선언을 불러와야 한다. 자바와 마찬가지로 임포트문은 파일의 맨 앞에 와야 하며 import 키워드를 사용한다.

- 클래스와 함수 선언을 패키지에 넣기

```kotlin
package geometry.shapes // 패키지 선언
import java.util.Random

class Rectangle(val height: Int, val width: Int) {
    val isSquare: Boolean
        get() = height == width
}

fun createRandomRectangle(): Rectangle {
    val random = Random()
    return Rectangle(random.nextInt(), random.nextInt())
}

```

> 코틀린에서는 클래스 임포트와 함수 임포트에 차이가 없으며, 모든 선언을 import 키워드로 가져올 수 있다. 최상위 함수는 그 이름을 써서 임포트할 수 있다.

- 다른 패키지에 있는 함수 임포트하기

```kotlin
package geometry.example

import geometry.shapes.createRandomRectangle // 이름으로 함수 임포트하기

fun main(args: Array<String>) {
    println(createRandomRectangle().isSquare)
}
```

> 패키지 이름 뒤에 .\*를 추가하면 패키지 안의 모든 선언을 임포트할 수 있다. 이런 스타임포트를 사용하면 패키지 안에 있는 모든 클래스뿐 아니라 최상위에 정의된 함수나 프로퍼티까지 모두 불러온다는 점에 유의하라.

> 코틀린에서는 여러 클래스를 한 파일에 넣을 수 있고, 파일의 이름도 마음대로 정할 수 있다. 코틀린에서는 디스크상의 어느 디렉토리에 소스코드 파일을 위치시키든 관계없다. 따라서 원하는 대로 소스코드를 구성할 수 있다. 예를 들어 geometry.shapes라는 패키지가 있다면 그 패키지의 모든 내용을 shapes.kt라는 파일에 넣고, 하위 패키지에 해당하는 별도의 디렉터리를 만들지 않고 geometry라는 폴더 안에 shapes.kt를 넣어도 된다.

> 하지만 대부분의 경우 자바와 같이 패키지별로 디렉터리를 구성하는 편이 낫다. 특히 자바와 코틀린을 함께 사용하는 프로젝트에서는 자바의 방식을 따르는게 중요하다. 자바의 방식을 따르지 않으면 자바 클래스를 코틀린 클래스로 마이그레이션할 때 문제가 생길 수도 있다.

> 하지만 여러 클래스를 한 파일에 넣는 것을 주저해서는 안 된다. 특히 각 클래스를 정의하는 소스코드 크기가 아주 작은 경우 더욱 그렇다.(코틀린에서는 클래스 소스코드 크기가 작은 경우가 자주 있다).

## 2.3 선택 표현과 처리: enum과 when

> when은 자바의 switch를 대치하되 훨씬 더 강력하며, 자주 사용할 프로그래밍 요소라고 생각할 수 있다. when에 대해 설명하는 과정에서 코틀린에서 enum을 선언하는 방법과 스마트 캐스트(smart cast)에 대해서도 살펴본다.

### 2.3.1 enum 클래스 정의

간단한 enum 클래스 정의하기

```kotlin
enum class Color {
    RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET
}
```

> enum은 자바 선언보다 코틀린 선언에 더 많은 키워드를 써야 하는 흔치 않은 예다. 코틀린에서는 enum class를 사용하지만 자바에서는 enum을 사용한다. 코틀린에서 enum은 소프트 키워드(soft keyword)라 부르는 존재다. enum은 class 앞에 있을 때는 특별한 의미를 지니지만 다른 곳에서는 이름에 사용할 수 있다. 반면 class는 키워드다. 따라서 class라는 이름을 사용할 수 없으므로 클래스를 표현하는 변수 등을 정의할 때는 clazz나 aClass와 같은 이름을 사용해야 한다.

> 자바와 마찬가지로 enum은 단순히 값만 열거하는 존재가 아니다. enum 클래스 안에도 프로퍼티나 메소드를 정의할 수 있다. 다음은 프로퍼티와 메소드를 enum 안에 선언하는 방법을 보여준다.

프로퍼티와 메소드가 있는 enum 클래스 선언하기

```kotlin
enum class Color (
    val r: Int, val g: Int, val b: Int
) {
    // 각 상수를 생성할 때 그에 대한 프로퍼티 값을 지정한다.
    RED(255, 0, 0), ORANGE(255, 165, 0),
    YELLOW(255, 255, 0), GREEN(0, 255, 0), BLUE(0, 0, 255),
    INDIGO(75, 0, 130), VIOLET(238, 130, 238); // 여기 반드시 세미콜론을 사용해야 한다.

    fun rgb() = (r * 256 + g) * 265 + b // enum 클래스 안에서 메소드를 정의한다.
}

>>> println(Color.BLUE.rgb())
255
```

> enum에서도 일반적인 클래스와 마찬가지로 생성자와 프로퍼티를 선언한다. 각 enum 상수를 정의할 때는 그 상수에 해당하는 프로퍼티 값을 지정해야만 한다. 이 예제에서는 코틀린에서 유일하게 세미콜론(;)이 필수인 부분을 볼 수 있다. enum 클래스 안에 메소드를 정의하는 경우 반드시 enum 상수 목록과 메소드 정의 사이에 세미콜론을 넣어야 한다.

### 2.3.2 when으로 enum 클래스 다루기

> 무지개 색을 기억하기 위해 연상법을 적용한 문장을 외우는 아이를 본 적이 있을 것이다. 그런 문장의 예로는 'Richard Of York Grave Battle In Vain!'를 들 수 있다. 무지개의 각 색에 대해 그와 상응하는 연상 단어를 짝지어주는 함수가 필요하다고 상상해보자(그리고 그 연상 단어 정보를 enum 안에 저장하지는 않는다고 하자). 자바라면 switch 문으로 그런 함수를 작성할 수 있다. switch에 해당하는 코틀린 구성 요소는 when 이다.

> if 와 마찬가지로 when도 값을 만들어내는 식(expression)이다. 따라서 식이 본문인 함수에 when을 바로 사용할 수 있다.

when을 사용해 올바른 enum 값 찾기

```kotlin
fun getMnemonic(color:Color) =
    when (color) {
        Color.RED -> "Richard"
        Color.ORANGE -> "Of"
        Color.YELLOW -> "York"
        Color.GREEN -> "Grave"
        Color.BLUE -> "Battle"
        Color.INDIGO -> "In"
        Color.VIOLET -> "Vain"
    }

>>> println(getMnemonic(Color.BLUE))
Battle
```

> 자바와 달리 각 분기의 끝에 break를 넣지 않아도 된다. 성공적으로 매치되는 분기를 찾으면 switch는 그 분기를 실행한다. 한 분기 안에서 여러 값을 매치 패턴으로 사용할 수도 있다. 그럴 경우 값 사이를 콤마(,)로 분리한다.

```kotlin
fun getWarmth(color: Color) = when(color) {
    Color.RED, Color.ORANGE, Color.YELLOW -> "warm"
    Color.GREEN -> "neutral"
    Color.BLUE, Color.INDIGO, Color.VIOLET -> "cold"
}
>>> println(getWarmth(Color.ORANGE))
warm
```

enum 상수 값을 임포트해서 enum 클래스 수식자 없이 enum 사용하기

```kotlin
import ch02.colors.Color
import ch02.colors.Color.*

fun getWarmth(color:Color) = when(color) {
    RED, ORANGE, YELLOW -> "warm"
    GREEN -> "neutral"
    BLUE, INDIGO, VIOLET -> "cold"
}
```

### 2.3.3 when과 임의의 객체를 함께 사용

> 코틀린에서 when은 자바의 switch보다 훨씬 더 강력하다. 분기 조건에 상수(enum 상수나 숫자 리터럴)만을 사용할 수 있는 자바 switch와 달리 코틀린 when의 분기 조건은 임의의 객체를 허용한다. 두 색을 혼합했을 때 미리 정해진 팔레트에 들어있는 색이 될 수 있는지 알려주는 함수를 작성하자. 팔레트에 있는 색을 조합할 수 있는 방법이 많지 않기 때문에 모든 경우를 쉽게 열거할 수 있다.

- when의 분기 조건에 여러 다른 객체 사용하기

```kotlin
fun mix(c1: Color, c2:Color) =
    when (setOf(c1, c2)) {
        setOf(RED, YELLOW) -> ORANGE
        setOf(YELLOW, BLUE) -> GREEN
        setOf(BLUE, VIOLET) -> INDIGO
        else -> throw Exception("Dirty color")
    }

>>> println(mix(BLUE, YELLOW))
GREEN
```

> 코틀린 표준 라이브러리에는 인자로 전달받은 여러 객체를 그 객체들을 포함하는 집합인 Set 객체로 만드는 `setOf`라는 함수가 있다.

> when 식은 인자 값과 매치하는 조건 값을 찾을 때까지 각 분기를 검사한다. 여기서는 setOf(c1, c2)와 분기 조건에 있는 객체 사이를 매치할 때 동등성(equality)을 사용한다.

### 2.3.4 인자 없는 when 사용

> 위 예제는 사실 약간 비효율적이다. 이 함수는 호출될 때마다 함수 인자로 주어진 두 색이 when의 분기 조건에 있는 다른 두 색과 같은지 비교하기 위해 여러 Set 인스턴스를 생성한다. 보통은 이런 비효율성은 크게 문제가 되지 않는다. 하지만 이 함수가 아주 자주 호출된다면 불필요한 가비지 객체가 늘어나는 것을 방지하기 위해 함수를 고쳐 쓰는 편이 낫다. 인자가 없는 when 식을 사용하면 불필요한 객체 생성을 막을 수 있다. 코드는 약간 읽기 어려워지지만 성능을 더 향상시키기 위해 그 정도 비용을 감수해야 하는 경우도 자주 있다.

인자가 없는 when

```kotlin
fun mixOptimized(c1: Color, c2: Color) =
    when {
        (c1 == RED && c2 == YELLOW) ||
        (c1 == YELLOW && c2 == RED) -> ORANGE
        ...
        else -> throw Exception("Dirty color")
    }
>>> println(mix(BLUE, YELLOW))
GREEN
```

### 2.3.5 스마트 캐스트: 타입 검사와 타입 캐스트를 조합

> (1+2) + 4 와 같은 간단한 산술식을 계산하는 함수를 만들어보자. 함수가 받을 산술식에서는 오직 두 수를 더하는 연산만 가능하다.

> 우선 식을 인코딩하는 방법을 생각해야 한다. 식을 트리 구조로 저장하자. 노드는 합계(Sum)나 수(Num) 중 하나다. Num은 항상 말단 노드지만, Sum은 자식이 둘 있는 중간(non-terminal) 노드다. Sum 노드의 두 자식은 덧셈의 두 인자다.

식을 표현하는 클래스 계층

```kotlin
interface Expr
// value라는 프로퍼티만 존재하는 단순한 클래스로 Expr 인터페이스를 구현한다.
class Num(val value: Int) : Expr
// Expr 타입의 객체라면 어떤 것이나 Sum 연산의 인자가 될 수 있다.
class Sum(val left: Expr, val right: Expr) : Expr

>>> println(eval(Sum(Sum(Num(1), Num(2)), Num(4))))
7
```

> Expr 인터페이스에는 두 가지 구현 클래스가 존재하낟. 따라서 식을 평가하려면 두 가지 경우를 고려해야 한다.

- 어떤 식이 수라면 그 값을 반환한다.
- 어떤 식이 합계라면 좌항과 우항의 값을 계산한 다음에 그 두 값을 합한 값을 반환한다.

if 연쇄를 사용해 식을 계산하기

```kotlin
fun eval(e:Expr): Int {
    if (e is Num) {
        val n = e as Num // 여기서 Num으로 타입을 변환하는데, 이는 불필요한 중복이다
        return n.value
    }
    if (e is Sum) {
        return eval(e.right) + eval(e.left)
    }
    throw IllegalArgumentException("Unknown expression")
}
```

> 코틀린에서는 is를 사용해 변수 타입을 검사한다. is 검사는 자바의 instanceof와 비슷하다. 하지만 자바에서 어떤 변수의 타입을 instanceof로 확인한 다음에 그 타입에 속한 멤버에 접근하기 위해서는 명시적으로 변수 타입을 캐스팅해야 한다. 이런 멤버 접근을 여러 번 수행해야 한다면 변수에 따로 캐스팅한 결과를 저장한 후 사용해야 한다. 코틀린에서는 프로그래머 대신 컴파일러가 캐스팅을 해준다. 어떤 변수가 원하는 타입인지 일단 is로 검사하고 나면 굳이 변수를 원하는 타입으로 캐스팅하지 않아도 마치 처음부터 그 변수가 원하는 타입으로 선언된 것처럼 사용할 수 있다. 하지만 실제로는 컴파일러가 캐스팅을 수행해준다. 이를 스마트 캐스트라고 부른다.

> eval 함수에서 e의 타입이 Num인지 검사한 다음 부분에서 컴파일러는 e의 타입을 Num으로 해석한다. 그렇기 때문에 Num의 프로퍼티인 value를 명시적 캐스팅 없이 e.value로 사용할 수 있다. Sum의 프로퍼티인 right와 left도 마찬가지다. Sum 타입인지 검사한 다음부터는 e.right와 e.left를 사용할 수 있다.

```kotlin
if (e is Sum) {
    return eval(e.right) + eval(e.left)
}

```

> - 스마트 캐스트란? 컴파일러가 "아, 너 방금 is로 타입 검사했구나? 그럼 내가 알아서 진짜 그 타입으로 형변환(캐스팅)해 줄게!" 하고 도와주는 기능입니다.
> - 장점: 개발자가 귀찮게 as Num 같은 코드를 일일이 적지 않아도 되므로 코드가 훨씬 깨끗해지고 실수가 줄어듭니다.

### 2.3.6 리팩토링: if를 when으로 변경

값을 만들어내는 if 식

```kotlin
fun eval(e: Expr): Int =
    if (e is Num) {
        e.value
    } else if (e is Sum) {
        eval(e.right) + eval(e.left)
    } else {
        throw IllegalArgumentException("Unknown expression")
    }
>>> println(eval(Sum(Num(1), Num(2))))
3
```

> if의 분기에 식이 하나밖에 없다면 중괄호를 생략해도 된다. if 분기에 블록을 사용하는 경우 그 블록의 마지막 식이 그 분기의 결과 값이다.

if 중첩 대신 when 사용하기

```kotlin
fun eval(e:Expr): Int =
    when(e) {
        is Num -> e.value
        is Sum -> eval(e.right) + eval(e.left)
        else -> throw IllegalArgumentException("Unknown expression")
    }
```

## 2.4 대상을 이터레이션: while과 for 루프

### 2.4.1 while 루프

> 코틀린에는 while과 do-while 루프가 있다. 두 루프의 문법은 자바와 다르지 않다.

### 2.4.2 수에 대한 이터레이션: 범위와 수열

> 코틀린에는 자바의 for 루프(어떤 변수를 초기화하고 그 변수를 루프를 한 번 실행할 때마다 갱신하고 루프 조건이 거짓이 될 때 반복을 마치는 형태의 루프)에 해당하는 요소가 없다. 이런 루프의 가장 흔한 용례인 초깃값, 증가 값, 최종 값을 사용한 루프를 대신하기 위해 코틀린에서는 범위range를 사용한다.

> 범위는 기본적으로 두 값으로 이뤄진 구간이다. 보통은 그 두 값은 정수 등의 숫자 타입의 값이며, `..` 연산자로 시작 값과 끝 값을 연결해서 범위를 만든다.
> `val oneToTen = 1..10`

> 코틀린의 범위는 폐구간(닫힌 구간)또는 양끝을 포함하는 구간이다. 이는 두 번째 값이 항상 범위에 포함된다는 뜻이다.

> 정수 범위로 수행할 수 있는 가장 단순한 작업은 범위에 속한 모든 값에 대한 이터레이션이다. 이런 식으로 어떤 범위에 속한 값을 일정한 순서로 이터레이션하는 경우를 수열(progression)이라고 부른다.

- when을 사용해 피즈버즈 게임 구현하기

```kotlin
fun fizzBuzz(i: Int) = when {
    i % 15 == 0 -> "FizzBuzz"
    i % 3 == 0 -> "Fizz"
    i % 5 == 0 -> "Buzz"
    else -> "$i"
}
>>> for (i in 1..100) {
    ...print(fizzBuzz(i))
}
1 2 Fizz 4 Buzz Fizz 7 ...

for (i in 100 downTo 1 step 2) {
    print(fizzBuzz(i))
}
Buzz 98 Fizz 94 92 FizzBuzz 88 ...
```

> 끝 값을 포함하지 않는 반만 닫힌 범위(half-closed range)에 대해 이터레이션하면 편할 때가 자주 있다. 그런 범위를 만들고 싶다면 until 함수를 사용하라. 예를 들어 `for (x in 0 until size)`라는 루프는 `for (x in 0..size-1)`과 같지만 좀 더 명확하게 개념을 표혆나다.

### 2.4.3 맵에 대한 이터레이션

- 맵을 초기화하고 이터레이션하기

```kotlin
val binaryReps = TreeMap<Char, String>() // 키에 대해 정렬하기 위해 TreeMap을 사용한다.

for (c in 'A'..'F') {
    val binary = Integer.toBinaryString(c.toInt())
    binaryReps[c] = binary
}

for ((letter, binary) in binaryReps) {
    println("${letter} = ${binary}")
}
```

> get과 put을 사용하는 대신 map[key]나 map[key] = value를 사용해 값을 가져오고 설정할 수 있다.
> `binaryReps[c] = binary`라는 코드는 `binaryReps.put(c, binary)`라는 자바 코드와 같다.

#### 2.4.4 in으로 컬렉션이나 범위의 원소 검사

```kotlin
fun isLetter(c: Char) = c in 'a'..'z' || c in 'A'..'Z'
fun isNotDigit(c: Char) = c !in '0'..'9'
>>> println(isLetter('q'))
true
>>> println(isNotDigit('x'))
true
```

> 범위는 문자에만 국한되지 않는다. 비교가 가능한 클래스라면(java.lang.Comparable 인터페이스를 구현한 클래스라면) 그 클래스의 인스턴스 객체를 사용해 범위를 만들 수 있다. Comparable을 사용하는 범위의 경우 그 범위 내의 모든 객체를 항상 이터레이션하지는 못한다. 예를 들어 'Java'와 'Kotlin' 사이의 모든 문자열을 이터레이션할 수 있을까? 그럴 수 없다. 하지만 in 연산자를 사용하면 값이 범위 안에 속하는지 항상 결정할 수 있다.

```kotlin
>>> println("Kotlin" in "Java".."Scala")
true
```

> String에 있는 Comparable 구현이 두 문자열을 알파벳 순서로 비교하기 때문에 여기있는 in 검사에서도 문자열을 알파벳 순서로 비교한다.

## 2.5 코틀린의 예외 처리

### 2.5.1 try, catch, finally

> 자바와 마찬가지로 예외를 처리하려면 try와 catch, finally 절을 함께 사용한다. 파일에서 각 줄을 읽어 수로 변환하되 그 줄이 올바른 수 형태가 아니면 null을 반환하는 다음 예제에서 그 세 가지 요소를 볼 수 있다.

- 자바와 마찬가지로 try 사용하기

```kotlin
fun readNumber(reader: BufferedReader): Int? {
    try {
        val line = reader.readLine()
        return Integer.parseInt(line)
    }
    catch (e: NumberFormatException) {
        return null
    }
    finally {
        reader.close()
    }
}

>>> val reader = BufferedReader(StringReader("239"))
>>> println(readNumber(reader))
239
```

> 자바 코드와 가장 큰 차이는 throws 절이 코드에 없다는 점이다. 자바에서는 함수를 작성할 때 함수 선언 뒤에 throws IOException을 붙여야 한다. 이유는 IOException이 체크 예외(checked exception)이기 때문이다. 자바에서는 체크 예외를 명시적으로 처리해야 한다. 어떤 함수가 던질 가능성이 있는 예외나 그 함수가 호출한 다른 함수에서 발생할 수 있는 예외를 모두 catch로 처리해야 하며, 처리하지 않는 예외는 throws 절에 명시해야 한다.

### 2.5.2 try를 식으로 사용

```kotlin
fun readNumber(reader: BufferedReader) {
    val number = try {
        Integer.parseInt(reader.readLine()) // 이 식의 값이 try 식의 값이 된다.
    } catch (e: NumberFormatException) {
        return
    }
    println(number)
}
>>> val reader = BufferedReader(StringReader("not a number"))
>>> readNumber(reader)
// 아무것도 출력되지 않음
```

> 코틀린의 try 키워드는 if나 when과 마찬가지로 식이다. 따라서 try의 값을 변수에 대입할 수 있다. if와 달리 try의 본문을 반드시 중괄호 {}로 둘러싸야 한다. 다른 문장과 마찬가지로 try의 본문도 내부에 여러 문장이 있으면 마지막 식의 값이 전체 결과 값이다.

> 역시 catch 블록도 그 안의 마지막 식이 블록 전체의 값이 된다.

```kotlin
fun readNumber(reader: BufferedReader) {
    val number = try {
        Integer.parseInt(reader.readLine()) // 이 식의 값이 try 식의 값이 된다.
    } catch (e: NumberFormatException) {
        null
    }
    println(number)
}
>>> val reader = BufferedReader(StringReader("not a number"))
>>> readNumber(reader)
null // 예외가 발생했으므로 함수가 "null"을 출력한다.

```

## 2.6 요약

- 함수를 정의할 때 fun 키워드를 사용한다. val과 var는 각각 읽기 전용 변수와 변경 가능한 변수를 선언할 때 쓰인다.
- 문자열 템플릿을 사용하면 문자열을 연결하지 않아도 되므로 코드가 간결해진다.
- 코틀린에서는 값 객체 클래스를 아주 간결하게 표현할 수 있다.
- 다른 언어에도 있는 if는 코틀린에서는 식이며, 값을 만들어낸다.
- 코틀린 when은 자바의 switch와 비슷하지만 더 강력하다.
- 어떤 변수의 타입을 검사하고 나면 굳이 그 변수를 캐스팅하지 않아도 검사한 타입의 변수처럼 사용할 수 있다. 그런 경우 컴파일러가 스마트 캐스트를 활용해 자동으로 타입을 바꿔준다.
- for, while, do-while 루프는 자바가 제공하는 같은 키워드의 기능과 비슷하다. 하지만 코틀린의 for는 자바의 for보다 더 편리하다. 특히 맵을 이터레이션하거나 이터레이션하면서 컬렉션의 원소와 인덱스를 함께 사용해야 하는 경우 코틀린의 for가 더 편리하다.
- 1..5와 같은 식은 범위를 만들어낸다. 범위와 수열은 코틀린에서 같은 문법을 사용하며, for 루프에 대해 같은 추상화를 제공한다. 어떤 값이 범위 안에 들어있거나 들어있지 않은지 검사하기 위해서 in이나 !in을 사용한다.
- 코틀린 예외 처리는 자바와 비슷하다. 담나 코틀린에서는 함수가 던질 수 있는 예외를 선언하지 않아도 된다.
