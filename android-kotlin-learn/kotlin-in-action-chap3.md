# 3장. 함수 정의와 호출

## 3.1 코틀린에서 컬렉션 만들기

```kotlin
val set = hashSetOf(1, 7, 53)
val list = arrayListOf(1, 7, 53)
val map = hashMapOf(1 to "one", 7 to "seven", 53 to "fifty-three")

>>> println(set.javaClass)
class java.util.HashSet
>>> println(list.javaClass)
class java.util.ArrayList
>>> println(map.javaClass)
class java.util.HashMap

```

> 여기서 to 가 언어가 제공하는 특별한 키워드가 아니라 일반 함수라는 점에 유의하라.
> 코틀린은 자신만의 컬렉션 기능을 제공하지 않는다. 자바 개발자가 기존 자바 컬렉션을 활용할 수 있다는 뜻이다. 코틀린은 표준 자바 컬렉션을 활용하여 자바 코드와 상호작용을 쉽게 했다.

> 코틀린 컬렉션은 자바 컬렉션과 똑같은 클래스다. 하지만 코틀린에서는 자바보다 더 많은 기능을 쓸 수 있다. 예를 들어 리스트의 마지막 원소를 가져오거나 수로 이뤄진 컬렉션에서 최댓값을 찾을 수 있다.

```kotlin
val strings = listOf("first", "second", "fourteenth")
>>> println(strings.last())
fourteenth
val numbers = setOf(1, 14, 2)
>>> println(numbers.max())
14
```

## 3.2 함수를 호출하기 쉽게 만들기

> 자바 컬렉션에는 디폴트 toString 구현이 들어있다. 하지만 그 디폴트 toString의 출력 형식은 고정돼 있고 우리에게 필요한 형식이 아닐 수도 있다.

```kotlin
val list = listOf(1, 2, 3)
>>> println(list)
[1, 2, 3]

```

> 디폴트 구현과 달리 (1; 2; 3) 처럼 원소 사이를 세미콜론으로 구분하고 괄호로 리스트를 둘러싸고 싶다면 어떻게 해야 할까? 이를 위해서는 자바 프로젝트에 구아바(Guava)나 아파치 커먼즈(Apache Commons) 같은 서드파티 프로젝트를 추가하거나 직접 관련 로직을 구현해야 한다. 코틀린에는 이런 요구 사항을 처리할 수 있는 함수가 표준 라이브러리에 이미 들어있다.

- joinToString() 함수의 초기 구현

```kotlin
fun <T> joinToString(
    collection: Collection<T>,
    seperator: String,
    prefix: String,
    postfix: String
) : String {
    val result = StringBuilder(prefix)
    for ((index, element) in collection.withIndex()) {
        if (index > 0) result.append(separator)
        result.append(element)
    }
    result.append(postfix)
    return result.toString()
}
```

> 이 함수는 제네릭(generic)하다. 즉, 이 함수는 어떤 타입의 값을 원소로 하는 컬렉션이든 처리할 수 있다. 제네릭 함수의 문법은 자바와 비슷하다.

```kotlin
val list = listOf(1, 2, 3)
>>> println(joinToString(list, "; ", "(", ")"))
(1; 2; 3)

```

> 잘 작동하지만, 어떻게 하면 이 함수를 호출하는 문장을 덜 번잡하게 만들 수 있을까? 함수를 호출할 때마다 매번 네 인자를 모두 전달할 수는 없을까?

### 3.2.1 이름 붙인 인자

> `joinToString(collection, " ", " ", ".")` 이 코드에서 인자로 전달한 각 문자열이 어떤 역할을 하는지 구분할 수 있는가? 각 원소는 공백으로 구분될까, 마침표로 구분될까? 함수의 시그니처를 살펴보지 않고는 이런 질문에 답하기 어렵다. 물론 함수 시그니처를 외우거나, IDE가 함수 시그니처를 표시해서 도움을 줄 수는 있겠지만, 함수 호출 코드 자체는 여전히 모호하다.

> 이런 문제는 특히 불리언 플래그 값을 전달해야 하는 경우 흔히 발생한다. 이를 해결하기 위해 일부 자바 코딩 스타일에서는 불리언 대신 enum 타입을 사용하라고 권장한다.

```java
joinToString(collection, /* seperator */ " ", /* prefix */ " ", /* postfix */ ".");

```

```kotlin
joinToString(collection, seperator=" ", prefix = " ", postfix = ".")
```

### 3.2.2 디폴트 파라미터 값

> 자바에서는 일부 클래스에 오버로딩한 메소드가 너무 많아진다는 문제가 있다. 파라미터 이름과 타입이 계속 반복되며, 모든 오버로딩 함수에 대해 대부분의 설명을 반복해 달아야 할 것이다. 그리고 인자 중 일부가 생략된 오버로드 함수를 호출할 때 어떤 함수가 불릴지 모호한 경우가 생긴다.

> 코틀린에서는 함수 선언에서 파라미터의 디폴트 값을 지정할 수 있으므로 이런 오버로드 중 상당 수를 피할 수 있다. 디폴트 값을 사용해 joinToString 함수를 개선해보자.

- 디폴트 파라미터 값을 사용해 joinToString() 정의하기

```kotlin
fun <T> joinToString(
    collection: Collection<T>,
    seperator: String = ", ",
    prefix: String = "",
    postfix: String = ""
): String

>>> joinToString(list, ", ", "", "")
1, 2, 3
>>> joinToString(list)
1, 2, 3
>>> joinToString(list, "; ")
1; 2; 3

>>> joinToString(list, postfix =";", prefix="# ")
# 1, 2, 3;
```

**디폴트 값과 자바**

> 자바에는 디폴트 파라미터 값이라는 개념이 없어서 코틀린 함수를 자바에서 호출하는 경우에는 그 코틀린 함수가 디폴트 파라미터 값을 제공하더라도 모든 인자를 명시해야 한다. 자바에서 코틀린 함수를 호출해야 한다면 자바 쪽에서 좀 더 편하게 코틀린 함수를 호출하고 싶을 것이다. 그럴 때 `@JvmOverloads` 애노테이션을 함수에 추가할 수 있다. `@JvmOverloads` 를 함수에 추가하면 코틀린 컴파일러가 자동으로 맨 마지막 파라미터로부터 파라미터를 하나씩 생략한 오버로딩한 자바 메소드를 추가해준다.
> 예를 들어 `joinToString`에 `@JvmOverloads`를 붙이면 다음과 같은 오버로딩한 함수가 만들어진다.

```java
String joinToString(Collection<T> collection, String seperator, String prefix, String postfix);

String joinToString(Collection<T> collection, String seperator, String prefix)

String joinToString(Collection<T> collection, String seperator);

String joinToString(Collection<T> collection);
```

### 3.2.3 정적인 유틸리티 클래스 없애기: 최상위 함수와 프로퍼티

> 자바를 아는 사람은 객체지향 언어인 자바에서는 모든 코드를 클래스의 메소드로 작성해야 한다는 사실을 알고 있다. 보통 그런 구조는 잘 작동한다. 하지만 실전에서는 어느 한 클래스에 포함시키기 어려운 코드가 많이 생긴다. 일부 연산에는 비슷하게 중요한 역할을 하는 클래스가 둘 이상 있을 수도 있다. 중요한 객체는 하나뿐이지만 그 연산을 객체의 인스턴스 API에 추가해서 API를 너무 크게 만들고 싶지는 않은 경우도 있다.
> 그 결과 다양한 정적 메소드를 모아두는 역할만 담당하며, 특별한 상태나 인스턴스 메소드는 없는 클래스가 생겨난다. JDK의 `Collections` 클래스가 전형적인 예다.

> 코틀린에서는 이런 무의미한 클래스가 필요 없다. 대신 함수를 직접 소스 파일의 최상위 수준, 모든 다른 클래스의 밖에 위치시키면 된다. 그런 함수들은 여전히 그 파일의 맨 앞에 정의된 패키지의 멤버 함수이므로 다른 패키지에서 그 함수를 사용하고 싶을 때는 그 함수가 정의된 패키지를 임포트해야만 한다. 하지만 임포트 시 유틸리티 클래스 이름이 추가로 들어갈 필요는 없다.

> joinToString 함수를 strings 패키지에 직접 넣어 보자.

- `joinToString()` 함수를 최상위 함수로 선언하기

```kotlin
package strings

fun joinToString(...): String {...}
```

> 이 함수가 어떻게 실행될 수 있는 걸까? JVM이 클래스 안에 들어있는 코드만을 실행할 수 있기 때문에 컴파일러는 이 파일을 컴파일할 때 **새로운 클래스를 정의** 해준다. 코틀린만 사용하는 경우에는 그냥 그런 클래스가 생긴다는 사실만 기억하면 된다. 하지만 이 함수를 자바 등의 다른 JVM 언어에서 호출하고 싶다면 코드가 어떻게 컴파일되는지 알아야 `joinToString`과 같은 최상위 함수를 사용할 수 있다. 어떻게 코틀린이 `join.kt`를 컴파일하는지 보여주기 위해 `join.kt`를 컴파일한 결과와 같은 클래스를 자바 코드로 써보면 다음과 같다.

```java
package strings;

public class JoinKt {
    public static String joinToString(...) {...}
}
```

> 코틀린 컴파일러가 생성하는 클래스의 이름은 최상위 함수가 들어있던 코틀린 소스 파일의 이름과 대응한다. 코틀린 파일의 모든 최상위 함수는 이 클래스의 정적인 메소드가 된다. 따라서 자바에서 `joinToString`을 호출하기는 쉽다.

```java
import strings.JoinKt;
...
JoinKt.joinToString(list, ", ", "", "");
```

- 최상위 프로퍼티
  > 어떤 데이터를 클래스 밖에 위치시켜야 하는 경우는 흔하지 않지만, 그래도 가끔 유용할 때가 있다. 예를 들어 어떤 연산을 수행한 횟수를 저장하는 `var` 프로퍼티를 만들 수 있다.

```kotlin
var opCount = 0

fun performOperation() {
    opCount++
}

fun reportOperationCount() {
    println("Operation performed $opCount times")
}
```

> 이런 프로퍼티의 값은 정적 필드에 저장된다. 최상위 프로퍼티를 활용해 코드에 상수를 추가할 수 있다.

`val UNIX_LINE_SEPERATOR = "\n"`

> 기본적으로 최상위 프로퍼티도 다른 모든 프로퍼티처럼 접근자 메소드를 통해 자바 코드에 노출된다(`val`의 경우 **게터**, `var`의 경우 **게터와 세터** 가 생긴다). 겉으론 상수처럼 보이는데 실제로는 게터를 사용해야 한다면 자연스럽지 못하다. 더 자연스럽게 사용하려면 이 상수를 `public static final` 필드로 컴파일해야 한다. `const` 변경자를 추가하면 프로퍼티를 `public static final` 필드로 컴파일하게 만들 수 있다.

`const val UNIX_LINE_SEPERATOR = "\n"`

`public static final String UNIX_LINE_SEPERATOR = "\n";` 자바 코드와 동등한 바이트코드를 만들어낸다.

---

3.2.3 절의 핵심은 **"자바처럼 불필요하게 껍데기뿐인 클래스를 만들지 않고도, 편리하게 유틸리티 함수와 상수를 정의하고 사용할 수 있다"**는 점이다.

---

### 1. 자바에서의 문제점 (배경)

자바는 모든 코드가 반드시 클래스 안에 존재해야 하는 객체지향 언어입니다.
하지만 개발을 하다 보면 특정 객체(인스턴스)의 데이터와 상관없이, 독립적으로 동작하는 편리한 함수(유틸리티 함수)가 필요할 때가 많습니다. 예를 들면 다음과 같은 작업들입니다.

- 두 숫자를 비교해 큰 수를 반환하는 작업
- 리스트의 요소들을 예쁘게 묶어서 하나의 문자열로 만드는 작업 (`joinToString`)

자바에서는 이를 해결하기 위해 어쩔 수 없이 실질적인 데이터는 없고 `static` 메소드만 모아둔 '껍데기 클래스'를 만들어야 했습니다. 대표적인 예가 자바의 `java.util.Collections`나 `java.lang.Math` 클래스입니다.

```java
// 자바에서는 클래스라는 껍데기가 강제됩니다.
public class StringUtils {
    public static String joinToString(...) { ... }
}
```

---

### 2. 코틀린의 해결책: 최상위 함수 (Top-level Function)

코틀린에서는 이러한 무의미한 클래스 선언을 생략할 수 있습니다. 클래스 밖, 즉 **파일의 가장 첫 머리(최상위 수준)**에 함수를 바로 작성할 수 있도록 허용하기 때문입니다.

`join.kt` 라는 파일이 있다면, 아래처럼 클래스 없이 함수만 적어두면 됩니다.

```kotlin
// join.kt 파일 내용
package strings

// 클래스 선언 없이 바로 함수를 정의합니다.
fun joinToString(...): String { ... }
```

이렇게 하면 호출할 때도 `StringUtils.joinToString(...)` 처럼 클래스 이름을 앞에 붙일 필요 없이, 그냥 `joinToString(...)`으로 바로 사용할 수 있어 코드가 한결 간결해집니다.

---

### 3. 내부적인 동작 원리 (JVM과의 호환성)

코틀린은 자바 가상 머신(JVM) 위에서 동작합니다. 하지만 JVM은 여전히 클래스 안에 있는 코드만 실행할 수 있습니다.

따라서 코틀린 컴파일러는 뒤에서 알아서 자바가 이해할 수 있는 형태로 코드를 변환(컴파일)해 줍니다.

- 코틀린 파일 이름이 `join.kt` 라면, 컴파일러는 자바의 `JoinKt`라는 클래스를 자동으로 만들어 냅니다.
- 그리고 우리가 만든 최상위 함수를 그 클래스 안의 `static` 메소드로 변환합니다.

이 덕분에 자바 코드에서도 코틀린의 최상위 함수를 가져다 쓸 수 있습니다. 자바에서는 아래와 같이 자동 생성된 클래스 이름을 거쳐 호출하게 됩니다.

```java
// 자바에서 코틀린의 최상위 함수를 호출하는 모습
import strings.JoinKt;

JoinKt.joinToString(...);
```

---

### 4. 최상위 프로퍼티와 `const` 변환

함수와 마찬가지로, 클래스 밖에 변수나 상수(프로퍼티)를 둘 수도 있습니다. 이를 **최상위 프로퍼티**라고 합니다.

```kotlin
var opCount = 0 // 최상위 프로퍼티 (변수)
val UNIX_LINE_SEPARATOR = "\n" // 최상위 프로퍼티 (읽기 전용)
```

이 프로퍼티들도 자바와 호환될 때는 내부적으로 자바의 `static` 필드로 변환됩니다.
하지만 코틀린의 일반적인 프로퍼티는 게터(getter)와 세터(setter)라는 메소드를 통해 값에 접근하는 것이 기본 규칙입니다. 즉, 자바에서 `UNIX_LINE_SEPARATOR`를 쓰려고 하면 내부적으로는 메소드를 호출하게 되어 직관적이지 않을 수 있습니다.

이를 해결하고 자바의 진짜 상수(`public static final`)처럼 컴파일되도록 만들고 싶을 때 사용하는 키워드가 바로 `const`입니다.

```kotlin
// const를 붙이면 컴파일 시점에 상수로 처리되어 성능과 직관성이 좋아집니다.
const val UNIX_LINE_SEPARATOR = "\n"
```

이 코드는 자바의 아래 코드와 완전히 동일하게 컴파일됩니다.

```java
public static final String UNIX_LINE_SEPARATOR = "\n";
```

---

### 요약하자면

- **기존 자바**: 유틸리티 함수 하나를 만들려고 해도 의미 없는 클래스 껍데기를 선언해야 했습니다.
- **코틀린**: 파일에 직접 함수(`최상위 함수`)와 상수(`const val`)를 적으면 되므로 구조가 한결 단순해집니다.
- **동작**: 코틀린 컴파일러가 파일 이름을 따서 자바 클래스(예: `파일이름Kt`)를 자동으로 만들어 주므로, 자바와의 호환성도 유지됩니다.

## 3.3 메소드를 다른 클래스에 추가: 확장 함수와 확장 프로퍼티

> 기존 코드와 코틀린 코드를 자연스럽게 통합하는 것은 코틀린의 핵심 목표 중 하나다. 완전히 코틀린으로만 이뤄진 프로젝트조차도 JDK나 안드로이드 프레임워크 또는 다른 서드파티 프레임워크 등의 자바 라이브러리를 기반으로 만들어진다. 또 코틀린을 기존 자바 프로젝트에 통합하는 경우에는 코틀린으로 직접 변환할 수 없거나 미처 변환하지 않은 기존 자바 코드를 처리할 수 있어야 한다. 이런 기존 자바 API를 재작성하지 않고도 코틀린이 제공하는 여러 편리한 기능을 사용할 수 있다면 정말 좋은 일이 아닐까? 바로 확장 함수(extension function)가 그런 역할을 해줄 수 있다.

> 개념적으로 확장 함수는 단순하다. 확장 함수는 어떤 클래스의 멤버 메소드인 것처럼 호출할 수 있지만 그 클래스의 밖에 선언된 함수다. 확장 함수를 보여주기 위해 어떤 문자열의 마지막 문자를 돌려주는 메소드를 추가해보자.

```kotlin
package strings

fun String.lastChar() : Char = this.get(this.length - 1)

```

> 확장 함수를 만들려면 추가하려는 함수 이름 앞에 그 함수가 확장할 클래스의 이름을 덧붙이기만 하면 된다. 클래스 이름을 수신 객체 타입(receiver type)이라 부르며, 확장 함수가 호출되는 대상이 되는 값(객체)을 수신 객체(receiver object)라고 부른다.

- 수신 객체 타입은 확장이 정의될 클래스의 타입이며, 수신 객체는 그 클래스에 속한 인스턴스 객체다.
  `fun String.lastChar(): Char = this.get(this.length - 1)` - `String`: 수신 객체 타입 - `this` : 수신 객체

> 이 함수를 호출하는 구문은 다른 일반 클래스 멤버를 호출하는 구문과 똑같다.

```kotlin
>>> println("Kotlin".lastChar())
n
```

- 이 예제에서는 `String`이 수신 객체 타입이고, `"Kotlin"` 이 수신 객체다.

> 어떤 면에서 이는 String 클래스에 새로운 메소드를 추가하는 것과 같다. String 클래스가 여러분이 직접 작성한 코드가 아니고 심지어 String 클래스의 소스코드를 소유한 것도 아니지만, 여러분은 여전히 원하는 메소드를 String 클래스에 추가할 수 있다. 심지어 String이 자바나 코틀린 등의 언어 중 어떤 것으로 작성됐는가는 중요하지 않다. 예를 들어 그루비(Groovy)와 같은 다른 JVM 언어로 작성된 클래스도 확장할 수 있다. 자바 클래스로 컴파일한 클래스 파일이 있는 한 그 클래스에 원하는 대로 확장을 추가할 수 있다.

> 일반 메소드의 본문에서 `this`를 사용할 때와 마찬가지로 확장 함수 본문에도 `this`를 쓸 수 있다. 그리고 일반 메소드와 마찬가지로 확장 함수 본문에서도 `this를 생략할 수 있다.

```kotlin
package strings
fun String.lastChar(): Char = get(length -1) // 수신 객체 멤버에 this 없이 접근할 수 있다.
```

> 확장 함수 내부에서는 일반적인 인스턴스 메소드의 내부에서와 마찬가지로 수신 객체의 메소드나 프로퍼티를 바로 사용할 수 있다. 하지만 확장 함수가 캡슐화를 깨지는 않는다는 사실을 기억하라. 클래스 안에서 정의한 메소드와 달리 확장 함수 안에서는 클래스 내부에서만 사용할 수 있는 비공개 멤버나 보호된 멤버를 사용할 수 없다.

> 이제부터는 클래스의 멤버 메소드와 확장 함수를 모두 **메소드** 라고 부를 것이다. 예를 들어 "확장 함수 내부에서는 수신 객체의 모든 메소드를 호출할 수 있다"라고 말하면 확장 함수 내부에서 수신 객체의 멤버 메소드와 확장 함수를 모두 호출할 수 있다는 뜻이다. 호출하는 쪽에서는 확장 함수와 멤버 메소드를 구분할 수 없다. 그리고 호출하는 메소드가 확장 함수인지 멤버 메소드인지 여부가 중요한 경우도 거의 없다.

---

> 확장 함수와 확장 프로퍼티의 핵심은 **"기본 라이브러리나 외부 오픈소스 등 내가 직접 소스코드를 수정할 수 없는 기존 클래스에, 마치 원래 있던 멤버 메서드나 프로퍼티처럼 새로운 기능을 덧붙여서 사용하는 기술"**

### 1. 확장 함수/프로퍼티는 왜 만들었을까? (도입 배경)

자바(Java)를 비롯한 기존 객체지향 언어에서는 다른 사람이 만든 클래스에 새로운 메서드를 추가하고 싶을 때 보통 두 가지 방법을 썼습니다.

#### 기존 방법 1: 상속 (Inheritance)

- `String` 클래스를 상속받아 `MyString`을 만들고 거기에 메서드를 추가합니다.
- **문제점**: `String` 클래스처럼 `final`로 선언되어 상속이 불가능한 클래스들이 많고, 메서드 단 하나를 추가하기 위해 새로운 클래스를 만드는 것은 비효율적입니다.

#### 기존 방법 2: 유틸리티 클래스 (Utility Class)

- 자바에서 흔히 볼 수 있는 `StringUtils`, `Collections` 같은 정적(static) 클래스를 만들어 사용합니다.

```java
// 자바에서의 유틸리티 클래스 사용 예시
if (StringUtils.isEmpty(str)) { ... }
Collections.sort(list);
```

- **문제점**: 코드가 직관적이지 않습니다. `"hello".isEmpty()` 처럼 객체 뒤에 마침표(`.`)를 찍어 자동완성 기능을 제공받는 형태가 아니라, `StringUtils`라는 클래스 이름을 기억해 내고 인자로 문자열을 넘겨주어야 하므로 가독성이 떨어집니다.

#### 코틀린의 해결책: 확장 함수

코틀린은 기존 클래스의 소스코드를 직접 수정하지 않고도, 해당 클래스의 인스턴스 뒤에 마침표(`.`)를 찍어 바로 호출할 수 있는 **확장 함수**를 제공하여 위 문제들을 해결했습니다.

---

### 2. 어떻게 작동하는가? (내부 원리)

우리가 작성한 확장 함수는 실제로 기존 클래스의 바이트코드를 변형하거나 내부로 들어가는 것이 아닙니다.

코틀린 컴파일러는 내부적으로 이 확장 함수를 **정적(static) 메서드**로 변환합니다.

```kotlin
// 코틀린에서 정의한 확장 함수
fun String.lastChar(): Char = this.get(this.length - 1)
```

이 코드는 컴파일 시점에 자바의 다음과 같은 정적 메서드로 자동 변환됩니다.

```java
// 자바 코드로 역컴파일했을 때의 모습
public static final char lastChar(String receiver) {
    return receiver.charAt(receiver.length() - 1);
}
```

따라서 기존 클래스(수신 객체)의 내부 설계를 전혀 훼손하지 않기 때문에 **안전(캡슐화 유지)**하며, 단지 호출할 때만 원래 클래스의 멤버인 것처럼 쓸 수 있는 편리한 문법적 설탕(Syntactic Sugar)인 것입니다.

---

### 3. 구체적인 사용 예시

실무에서 자주 쓰이는 유용한 예시들을 살펴보겠습니다.

#### 예시 A: 확장 함수 (Extension Function)

문자열이 이메일 형식인지 검사하는 도구를 만들어 보겠습니다. `String` 클래스는 우리가 수정할 수 없지만, 확장 함수를 사용하면 매우 편리해집니다.

```kotlin
// 1. 확장 함수 정의
fun String.isEmail(): Boolean {
    val emailRegex = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}$".toRegex()
    return this.matches(emailRegex) // this는 호출하는 문자열 객체를 가리킴
}

// 2. 실제 사용
fun main() {
    val userEmail = "contact@example.com"

    // 원래 String 클래스에 있는 메서드처럼 자연스럽게 호출 가능
    if (userEmail.isEmail()) {
        println("유효한 이메일입니다.")
    }
}
```

#### 예시 B: 확장 프로퍼티 (Extension Property)

프로퍼티(필드 변수)도 확장할 수 있습니다. 단, 실제 클래스에 메모리 공간(필드)을 추가할 수는 없기 때문에, 값을 저장할 수는 없고 **커스텀 게터(Getter)를 통해서만 정의**할 수 있습니다.

리스트의 마지막 인덱스를 가져오는 프로퍼티를 확장해 보겠습니다.

```kotlin
// 1. 확장 프로퍼티 정의 (상태를 저장할 수 없으므로 get()이 필수적임)
val <T> List<T>.lastIndex: Int
    get() = this.size - 1

// 2. 실제 사용
fun main() {
    val list = listOf("A", "B", "C")

    // 프로퍼티처럼 값에 접근 가능
    println(list.lastIndex) // 출력: 2
}
```

---

### 4. 어떻게 적용하고 관리하는가?

내가 만든 확장 함수를 다른 파일이나 패키지에서 가져다 쓰려면, 일반적인 클래스나 함수처럼 **`import`**만 해주면 됩니다.

```kotlin
// 다른 패키지에 있는 확장 함수를 가져올 때
import com.example.utils.isEmail

fun process(input: String) {
    if (input.isEmail()) { ... }
}
```

이러한 특성 덕분에 패키지 내부에 필요한 유틸리티성 함수들을 정리해 두고, 필요한 곳에서만 임포트하여 코드의 흐름을 깨지 않고 매우 직관적으로 작성할 수 있습니다.

---

### 3.3.1 임포트와 확장 함수

> 확장 함수를 정의했다고 해도 자동으로 프로젝트 안의 모든 소스코드에서 그 함수를 사용할 수 있지는 않다. 확장 함수를 사용하기 위해서는 그 함수를 다른 클래스나 함수와 마찬가지로 임포트해야만 한다. 확장 함수를 정의하자마자 어디서든 그 함수를 쓸 수 있다면 한 클래스에 같은 이름의 확장 함수가 둘 이상 있어서 이름이 충돌하는 경우가 자주 생길 수 있다. 코틀린에서는 클래스를 임포트할 때와 동일한 구문을 사용해 개별 함수를 임포트할 수 있다.

```kotlin
import strings.lastChar

val c = "Kotlin".lastChar()

import strings.*

val c = "Kotlin".lastChar()

import strings.lastChar as last

val c = "Kotlin".last()
```

> 다른 여러 패키지에 이름이 같은 함수가 많은데 한 파일 안에서 그런 함수들을 함께 써야 하는 경우 이름을 바꿔서 임포트하면 편리하다. 일반적인 클래스나 함수라면 다른 방법도 있다. 해당 클래스나 함수를 부를 때 전체 이름(FQN, Fully Qualifyed Name)을 쓰면 된다. 하지만 확장 함수는 코틀린 문법상 반드시 짧은 이름을 써야 한다. 따라서 임포트 시 이름을 바꾸는 것이 확장 함수의 이름 충돌을 해결하는 유일한 방법이다.

### 3.3.2 자바에서 확장 함수 호출

> 내부적으로 확장 함수는 수신 객체를 첫 번째 인자로 받는 정적 메소드다. 그래서 확장 함수를 호출해도 다른 어댑터 객체나 실행 시점 부가 비용이 들지 않는다.

> 이런 설계로 인해 자바에서 확장 함수를 사용하기도 편하다. 단지 정적 메소드를 호출하면서 첫 번째 인자로 수신 객체를 넘기기만 하면 된다. 다른 최상위 함수와 마찬 가지로 확장 함수가 들어있는 자바 클래스 이름도 확장 함수가 들어있는 파일 이름에 따라 결정된다. 따라서 확장 함수를 `StringUtil.kt` 파일에 정의했다면 다음과 같이 호출할 수 있다.

```java
char c = StringUtilKt.lastChar("Java");
```

### 3.3.3 확장 함수로 유틸리티 함수 정의

> 이제 `joinToString` 함수의 최종 버전을 만들자. 이제 이 함수는 코틀린 라이브러리가 제공하는 함수와 거의 같아졌다.

- 3.4 `joinToString()`를 확장으로 정의하기

```kotlin
fun <T> Collection<T>.joinToString(
    seperator: String = ", ",
    prefix: String = "",
    postfix: String = ""
): String {
    val result = StringBuilder(prefix)

    for ((index, element) in this.withIdex())
        if (index > 0) result.append(seperator)
        result.append(element)


    result.append(postfix)
    return result.toString()
}

>>> val list = listOf(1, 2, 3)
>>> println(list.joinToString(seperator="; ",
...    prefix = "(", postfix = ")"))
(1; 2; 3)

```

> 원소로 이뤄진 컬렉션에 대한 확장을 만든다. 긜고 모든 인자에 대한 디폴트 값을 지정한다. 이제 `joinToString`을 마치 클래스의 멤버인 것처럼 호출할 수 있다.

```kotlin
>>> val list = arrayListOf(1, 2, 3)
>>> println(list.joinToString(" "))
1 2 3

```

> 확장 함수는 단지 정적 메소드 호출에 대한 문법적인 편의(syntatic sugar)일 뿐이다. 그래서 클래스가 아닌 더 구체적인 타입을 수신 객체 타입으로 지정할 수도 있다. 그래서 문자열의 컬렉션에 대해서만 호출할 수 있는 `join` 함수를 정의하고 싶다면 다음과 같이 하면 된다.

```kotlin
fun Collection<String>.join(
    seperator: String = ", ",
    prefix: String = "",
    postfix: String = ""
) = joinToString(seperator, prefix, postfix)

>>> println(listOf("one", "two", "eight").join(" "))
one two eight
```

> 이 함수를 객체의 리스트에 대해 호출할 수는 없다.
> `listOf(1, 2, 8).join()`
> `Error: Type mismatch: inferred type is List<Int> but Collection<String> was expected`

> 확장 함수가 정적 메소드와 같은 특징을 가지므로, 확장 함수를 하위 클래스에서 오버라이드할 수는 없다.

### 3.3.4 확장 함수는 오버라이드할 수 없다.

> View와 그 하위 클래스인 Button이 있는데 Button이 상위 클래스의 click 함수를 오버라이드하는 경우를 생각해보자.

3.5 멤버 함수 오버라이드 하기

```kotlin
open class View {
    open fun click() = println("View clicked")
}

class Button: View() {
    override fun click() = println("Button clicked")
}
```

> Button이 View의 하위 타입이기 때문에 View 타입 변수를 선언해도 Button 타입 변수를 그 변수에 대입할 수 있다. View 타입 변수에 대해 click과 같은 일반 메소드를 호출했는데, click을 Button 클래스가 오버라이드했다면 실제로는 Button이 오버라이드한 click이 호출된다.

- 실행 시점에 객체 타입에 따라 동적으로 호출될 대상 메소드를 결정하는 방식을 동적 디스패치(dynamic dispatch)라고 한다. 반면 컴파일 시점에 알려진 변수 타입에 따라 정해진 메소드를 호출하는 방식은 정적 디스패치라고 부른다. 참고로 프로그래밍 언어 용어에서 '정적'이라는 말은 컴파일 시점을 의미하고 '동적'이라는 말은 실행 시점을 의미한다.

```kotlin
>>> val view: View = Button()
>>> view.click()
Button clicked
```

> 하지만 확장 함수는 클래스의 일부가 아니다. 확장 함수는 클래스 밖에 선언된다. 이름과 파라미터가 완전히 같은 확장 함수를 기반 클래스와 하위 클래스에 대해 정의해도 실제로는 확장 함수를 호출할 때 수신 객체로 지정한 변수의 정적 타입에 의해 어떤 확장 함수가 호출될지 결정되지, 그 변수에 저장된 객체의 동적인 타입에 의해 확장 함수가 결정되지 않는다.

- 확장 함수는 오버라이드 될 수 없다.

```kotlin
fun View.showOff() = println("I'm a view!")
fun Button.showOff() = println("I'm a button!")

>>> val view: View = Button()
>>> view.showOff()
I'm a view!
```

> view가 가리키는 객체의 실제 타입이 `Button`이지만, 이 경우 view의 타입이 View이기 때문에 무조건 View의 확장 함수가 호출된다.

> 확장 함수를 첫 번째 인자가 수신 객체인 정적 자바 메소드로 컴파일한다는 사실을 기억한다면 이런 동작을 쉽게 이해할 수 있다. 자바도 호출할 정적 함수를 같은 방식으로 정적으로 결정한다.

```java
>>> View view = new Button();
>>> ExtensionsKt.showOff(view);
I'm a view!
```

> 위 예제와 같이 확장 함수를 오버라이드할 수는 없다. 코틀린은 호출될 확장 함수를 정적으로 결정하기 때문이다.

- 어떤 클래스를 확장한 함수와 그 클래스의 멤버 함수의 이름과 시그니처가 같다면 확장 함수가 아니라 멤버 함수가 호출된다(멤버 함수의 우선순위가 더 높다). 클래스의 API를 변경할 경우 항상 이를 염두에 둬야 한다. 여러분이 코드 소유권을 가진 클래스에 대한 확장 함수를 정의해서 사용하는 외부 클라이언트 프로젝트가 있다고 하자. 그 확장 함수와 이름과 시그니처가 같은 멤버 함수를 여러분의 클래스 내부에 추가하면 클라이언트 프로젝트를 재컴파일한 순간부터 그 클라이언트는 확장 함수가 아닌 새로 추가된 멤버 함수를 사용하게 된다.

---

#### 1. 용어의 정확한 개념

- **정적 타입 (Static Type, 컴파일 시점 타입)**
  - 변수를 선언할 때 **코드에 명시한 타입**입니다.
  - 컴파일러는 오직 이 타입만 보고 "이 변수로 어떤 메서드를 호출할 수 있는지"를 판단합니다.
- **동적 타입 (Dynamic Type, 실행 시점/실제 타입)**
  - 애플리케이션이 실행될 때, **힙(Heap) 메모리에 실제로 생성되어 변수가 가리키고 있는 객체의 타입**입니다.

---

#### 2. 세 가지 시나리오로 보는 정적/동적 타입

`View`가 상위 클래스이고 `Button`이 하위 클래스일 때, 코드를 어떻게 작성하느냐에 따라 정적 타입은 달라집니다.

#### 경우 A: 상위 클래스 타입 변수에 하위 객체를 담는 경우 (다형성)

질문하신 책의 예제와 같은 경우입니다.

```kotlin
val view: View = Button()
```

- **정적 타입**: `View` (코드 왼쪽에 `View`라고 선언했으므로 컴파일러는 얘를 `View`로만 봅니다.)
- **동적 타입**: `Button` (실제 메모리에 만들어진 녀석은 `Button`입니다.)
- _이 경우에만 상위 클래스(`View`)가 정적 타입이 됩니다._

#### 경우 B: 하위 클래스 타입 변수에 하위 객체를 담는 경우

일반적으로 가장 많이 작성하는 형태입니다.

```kotlin
val button: Button = Button()
```

- **정적 타입**: `Button` (코드 왼쪽에 `Button`이라고 적었습니다.)
- **동적 타입**: `Button` (실제 객체도 `Button`입니다.)
- _이 경우 정적 타입은 상위 클래스가 아니라 하위 클래스(`Button`)가 됩니다._

#### 경우 C: 타입 추론을 사용하는 경우

타입을 명시하지 않고 컴파일러에게 추론을 맡기는 경우입니다.

```kotlin
val view = Button() // 컴파일러가 좌변의 타입을 Button으로 추론함
```

- **정적 타입**: `Button`
- **동적 타입**: `Button`

---

#### 3. 이것이 확장 함수와 무슨 상관인가요?

확장 함수는 **"정적 타입(좌변의 타입)"**만 보고 어떤 함수를 호출할지 컴파일 시점에 완전히 결정해 버립니다.

다시 책의 예시를 보면:

```kotlin
fun View.showOff() = println("I'm a view!")     // (1)번 함수
fun Button.showOff() = println("I'm a button!") // (2)번 함수

val view: View = Button() // 정적 타입: View, 동적 타입: Button
view.showOff()
```

1.  컴파일러는 `view.showOff()` 코드를 분석합니다.
2.  이때 컴파일러는 실제 메모리에 뭐가 들어있는지(동적 타입이 `Button`인지)는 관심이 없고, 오직 코드에 적힌 **정적 타입(`View`)**만 봅니다.
3.  따라서 `View` 타입에 정의된 **(1)번 함수**를 호출하도록 컴파일된 바이트코드를 고정해 버립니다.
4.  실행 시점에도 이미 결정된 (1)번 함수만 실행되므로 "I'm a view!"가 출력됩니다.

#### 요약

- **변수를 선언할 때 지정한 타입**이 정적 타입이 됩니다.
- 다만 개발자가 유연한 설계를 위해 일부러 변수 타입을 상위 클래스로 선언(`val view: View = Button()`)했을 때만, 상위 클래스가 정적 타입이 됩니다.
- 확장 함수는 오직 이 **좌변에 선언된 정적 타입**을 기준으로 실행할 대상을 결정하기 때문에 오버라이딩이 불가능합니다.

### 3.3.5 확장 프로퍼티

> 확장 프로퍼티를 사용하면 기존 클래스 객체에 대한 프로퍼티 형식의 구문으로 사용할 수 있는 API를 추가할 수 있다. 프로퍼티라는 이름으로 불리기는 하지만 상태를 저장할 적절한 방법이 없기 때문에(기존 클래스 인스턴스 객체에 필드를 추가할 방법은 없다) 실제로 확장 프로퍼티는 아무 상태도 가질 수 없다. 하지만 프로퍼티 문법으로 더 짧게 코드를 작성할 수 있어서 편한 경우가 있다.
> 앞 절에서 `lastChar`라는 함수를 정의했다. 이제 그 함수를 프로퍼티로 바꾸자.

- 3.7 확장 프로퍼티 선언하기

```kotlin
val String.lastChar: Char
    get() = get(length-1)

```

> 확장 함수의 경우와 마찬가지로 확장 프로퍼티도 일반적인 프로퍼티와 같은데, 단지 수신 객체 클래스가 추가됐을 뿐이다. 뒷받침하는 필드가 없어서 기본 게터 구현을 제공할 수 없으므로 최소한 게터는 꼭 정의해야 한다. 마찬가지로 초기화 코드에서 계산한 값을 담을 장소가 전혀 없으므로 초기화 코드도 쓸 수 없다.

> `StringBuilder`에 같은 프로퍼티를 정의한다면 `StringBuilder` 의 맨 마지막 문자는 변경 가능하므로 프로퍼티를 `var`로 만들 수 있다.

- 3.8 변경 가능한 확장 프로퍼티 선언하기

```kotlin
var StringBuilder.lastChar: Char
    get() = get(length-1)
    set(value: Char) {
        this.setCharAt(length - 1, value)
    }

```

> 확장 프로퍼티를 사용하는 방법은 멤버 프로퍼티를 사용하는 방법과 같다.

```kotlin
>>> println("Kotlin".lastChar)
n
>>> val sb = StringBuilder("Kotlin?")
sb.lastChar = '!'

>>> println(sb)
>>> Kotlin!
```
