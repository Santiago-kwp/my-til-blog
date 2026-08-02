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

확장 함수는 **"정적 타입(좌변의 타입)"** 만 보고 어떤 함수를 호출할지 컴파일 시점에 완전히 결정해 버립니다.

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

## 3.4 컬렉션 처리: 가변 길이 인자, 중위 함수 호출, 라이브러리 지원

> 이번 절은 컬렉션을 처리할 때 쓸 수 있는 코틀린 표준 라이브러리 함수 몇 가지를 보여준다. 그 과정에서 아래와 같은 코틀린 언어 특성을 설명한다.

- `vararg` 키워드를 사용하면 호출 시 인자 개수가 달라질 수 있는 함수를 정의할 수 있다.
- 중위(infix) 함수 호출 구문을 사용하면 인자가 하나뿐인 메소드를 간편하게 호출할 수 있다.
- 구조 분해 선언(destructing declaration)을 사용하면 복합적인 값을 분해해서 여러 변수에 나눠 담을 수 있다.

### 3.4.1 자바 컬렉션 API 확장

> 코틀린 컬렉션은 자바와 같은 클래스를 사용하지만 더 확장된 API를 제공한다고 했다. 그리고 리스트의 마지막 원소를 가져오는 예제와 숫자로 이뤄진 컬렉션의 최댓값을 찾는 예제를 살펴봤다.

```kotlin
val strings: List<String> = listOf("first","second","fourteenth")
strings.last()
// fourteenth
val numbers: Collection<Int> = setOf(1, 14, 2)
numbers.max()
// 14
```

> 이런 코드가 어떻게 작동할 수 있을지 궁금했을 것이다. 어떻게 자바 라이브러리 클래스의 인스턴스인 컬렉션에 대해 코틀린이 새로운 기능을 추가할 수 있을까? 답은 last 와 max 모두 확장 함수였던 것이다.

> `last` 함수는 앞 절에서 `String`에 대해 정의했던 `lastChar`보다 복잡하지 않다. `last`는 `List` 클래스의 확장 함수다. `max`의 경우에는 더 단순하게 정리한 선언을 살펴봤다.

```kotlin
fun <T> List<T>.last(): T { /* 마지막 원소를 반환함 */}
fun Collection<Int>.max(): Int { /* 컬렉션의 최댓값을 찾음 */ }
```

### 3.4.2 가변 인자 함수: 인자의 개수가 달라질 수 있는 함수 정의

> 리스트를 생성하는 함수를 호출할 때 원하는 만큼 많이 원소를 전달할 수 있다.

```kotlin
val list = listOf(2, 3,  5, 7 ,11)
```

라이브러리에서 이 함수의 정의를 보면 다음과 같다.

```kotlin
fun listOf<T>(vararg values: T): List<T> {...}
```

> 자바의 가변 길이 인자는 메소드를 호출할 때 원하는 개수만큼 값을 인자로 넘기면 자바 컴파일러가 배열에 그 값들을 넣어주는 기능이다. 코틀린의 가변 길이 인자도 자바와 비슷하다. 다만 문법이 조금 다르다. 타입 뒤에 `...` 을 붙이는 대신 코틀린에서는 파라미터 앞에 `vararg` 변경자를 붙인다.

> 이미 배열에 들어있는 원소를 가변 길이 인자로 넘길 때도 코틀린과 자바 구문이 다르다. 자바에서는 배열을 그냥 넘기면 되지만 코틀린에서는 배열을 명시적으로 풀어서 배열의 각 원소가 인자로 전달되게 해야 한다. 기술적으로는 **스프레드(spread) 연산자** 가 그런 작업을 해준다. 하지만 실제로는 전달하려는 배열 앞에 `*` 를 붙이기만 하면 된다.

```kotlin
fun main(args: Array<String>) {
    val list = listOf("args", *args)
    println(list)
}
```

> 이 예제는 스프레드 연산자를 통하면 배열에 들어있는 값과 다른 여러 값을 함께 써서 함수를 호출할 수 있음을 보여준다. 이런 기능은 자바에서는 사용할 수 없다.

---

> 참고 : **가변 인자 함수를 호출할 때 '개별 값'과 '배열'을 동시에 섞어서 전달하는 것이 자바에서는 불가능하다**는 뜻

#### 1. 자바에서의 제한 사항

자바에서도 가변 인자(Varargs)를 지원하지만, 다음과 같은 제약이 있습니다.

```java
// 가변 인자를 받는 자바 메서드
public static void printColors(String... colors) {
    for (String color : colors) {
        System.out.println(color);
    }
}
```

이 메서드를 호출할 때 자바에서는 아래 두 가지 방식 중 하나만 선택해야 합니다.

1. **개별 값들을 나열하여 전달하기**
   ```java
   printColors("Red", "Green", "Blue"); // 가능
   ```
2. **배열 하나만 전달하기**
   ```java
   String[] moreColors = {"Green", "Blue"};
   printColors(moreColors); // 가능
   ```

하지만 **개별 값과 배열을 섞어서 전달하는 것은 불가능**합니다. 즉, 아래와 같은 코드는 자바에서 컴파일 에러가 발생합니다.

```java
String[] moreColors = {"Green", "Blue"};

// 에러 발생: 개별 값("Red")과 배열(moreColors)을 동시에 인자로 넘길 수 없습니다.
printColors("Red", moreColors);
```

자바에서 위와 같이 구현하려면 새로운 배열을 생성하여 "Red"와 `moreColors`의 원소들을 합친 뒤, 그 합쳐진 배열을 전달해야 하는 번거로움이 있습니다.

---

#### 2. 코틀린에서의 해결 (스프레드 연산자)

코틀린은 **스프레드 연산자(`*`)** 를 제공하여 이 문제를 해결합니다. 배열 앞에 `*`를 붙이면 배열의 요소를 각각 낱개로 포장을 풀어서(spread) 전달해 줍니다.

질문하신 예제 코드를 다시 보겠습니다.

```kotlin
fun main(args: Array<String>) {
    // "args"라는 개별 문자열과 *args(배열의 내용물들을 풀어헤친 것)를 동시에 전달합니다.
    val list = listOf("args", *args)
    println(list)
}
```

예를 들어 프로그램 실행 시 인자(`args`)로 `"one"`, `"two"`라는 배열이 들어왔다고 가정해 보겠습니다.

- `*args`는 배열 내부의 값들을 풀어서 `"one"`, `"two"`로 만들어 줍니다.
- 결과적으로 `listOf("args", "one", "two")`를 호출하는 것과 같아집니다.

이처럼 **"이미 존재하는 배열의 원소들과 다른 개별 값들을 조합하여 가변 인자 함수에 한 번에 전달하는 기능"** 은 자바에 존재하지 않으며, 코틀린에서는 스프레드 연산자를 통해 지원합니다.

---

### 3.4.3 값의 쌍 다루기: 중위 호출과 구조 분해 선언

> 맵을 만들려면 `mapOf` 함수를 사용한다.

`val map = mapOf(1 to "One", 7 to "Seven", 53 to "fifty-three")`

> 여기서 `to` 라는 단어는 코틀린 키워드가 아니다. 이 코드는 **중위 호출(infix call)** 이라는 특별한 방식으로 `to`라는 일반 메소드를 호출한 것이다.

> 중위 호출 시에는 수신 객체와 유일한 메소드 인자 사이에 메소드 이름을 넣는다(이때 객체, 메소드 이름, 유일한 인자 사이에는 공백이 들어가야 한다). 다음 두 호출은 동일하다.

```kotlin
1.to("one") // "to" 메소드를 일반적인 방식으로 호출함
1 to "one" // "to" 메소드를 중위 호출 방식으로 호출함
```

> 인자가 하나뿐인 일반 메소드나 인자가 하나뿐인 확장 함수에 중위 호출을 사용할 수 있다. 함수(메소드)를 중위 호출에 사용하게 허용하고 싶으면 `infix` 변경자를 함수(메소드) 선언 앞에 추가해야 한다. 다음은 `to` 함수의 정의를 간략하게 줄인 코드다.

```kotlin
infix fun Any.to(other: Any) = Pair(this, other)
```

> 이 `to` 함수는 `Pair` 의 인스턴스를 반환한다. `Pair` 는 코틀린 표준 라이브러리 클래스로, 그 이름대로 두 원소로 이뤄진 순서쌍을 표현한다. 실제로 `to`는 제네릭 함수지만 여기서는 설명을 위해 그런 세부 사항을 생략했다.

Pair의 내용으로 두 변수를 즉시 초기화할 수 있다.

`val (number, name) = 1 to "one"`

> 이런 기능을 구조 분해 선언(destructing declaration)이라고 부른다.

`Pair` 인스턴스 외 다른 객체에도 구조 분해를 적용할 수 있다. 예를 들어 `key`와 `value` 라는 두 변수를 맵의 원소를 사용해 초기화할 수 있다.
루프에서도 구조 분해 선언을 활용할 수 있다. `joinToString` 에서 본 `withIndex` 를 구조 분해 선언과 조합하면 컬렉션 원소의 인덱스와 값을 따로 변수에 담을 수 있다.

```kotlin
for ((index, element) in collection.withIndex()) {
    println("$index: $element")
}
```

> `to` 는 확장 함수다. `to`를 사용하면 타입과 관계없이 임의의 순서쌍을 만들 수 있다. 이는 `to`의 수신 객체가 제네릭하다는 뜻이다. `1 to "one", "one" to 1, list to list.size()` 등의 호출이 모두 잘 작동한다. `mapOf` 함수의 선언을 살펴보자.

`fun <K, V> mapOf(vararg values: Pair<K, V>): Map(K, V)`

listOf 와 마찬가지로 mapOf도 원하는 개수만큼 인자를 전달할 수 있다. 하지만 mapOf의 경우에는 각 인자가 키와 값으로 이뤄진 순서쌍이어야 한다.

## 3.5 문자열과 정규식 다루기

> 코틀린 문자열은 자바 문자열과 같다. 코틀린 코드가 만들어낸 문자열을 아무 자바 메소드에 넘겨도 되며, 자바 코드에서 받은 문자열을 아무 코틀린 표준 라이브러리 함수에 전달해도 전혀 문제없다. 특별한 변환도 필요 없고 자바 문자열을 감싸는 별도의 래퍼도 생기지 않는다.

> 코틀린은 다양한 확장 함수를 제공함으로써 표준 자바 문자열을 더 즐겁게 다루게 해준다. 또한 혼동이 야기될 수 있는 일부 메소드에 대해 더 명확한 코틀린 확장 함수를 제공함으로써 프로그래머의 실수를 줄여준다. 자바와 코틀린 API의 차이를 알아보기 위한 첫 번째 예제로 문자열을 구분 문자열에 따라 나누는 작업을 코틀린에서 어떻게 처리하는지 살펴보자.

### 3.5.1 문자열 나누기

> 자바 개발자라면 String의 split 메소드를 잘 알고 있을 것이다. 스택 오버플로우 질문 중에는 "자바 split 메소드로는 점(.)을 사용해 문자열을 분리할 수 없습니다."라는 질문이 있다. "12.345-6.A".split(".") 라는 호출의 결과가 [12, 345-6, A] 라고 생각하는 실수를 저지르는 개발자가 많다. 하지만 자바의 split 메소드는 빈 배열을 반환한다! split의 구분 문자열은 실제로는 정규식(regular expression)이기 때문이다. 따라서 마침표(.)는 모든 문자를 나타내는 정규식으로 해석된다.

> 코틀린에서는 자바의 split 대신에 여러 가지 다른 조합의 파라미터를 받는 split 확장 함수를 제공함으로써 혼동을 야기하는 메소드를 감춘다. 정규식을 파라미터로 받는 함수는 String이 아닌 Regex 타입의 값을 받는다. 따라서 코틀린에서는 split 함수에 전달하는 값의 타입에 따라 정규식이나 일반 텍스트 중 어느 것으로 문자열을 분리하는지 쉽게 알 수 있다.

다음 코드는 마침표나 대시(-)로 문자열을 분리하는 예를 보여준다.

```kotlin
println("12.345-6.A".split("\\.|-".toRegex())) // 정규식을 명시적으로 만든다.
// [12, 345, 6, A]
```

> 코틀린 정규식 문법은 자바와 똑같다. 여기 있는 패턴은 마침표나 대시와 매치된다(정규식 안에서 마침표가 와일드카드 문자가 아닌 문자 자체로 쓰이게 하기 위해 마침표를 이스케이프시켰다). 정규식을 처리하는 API는 표준 자바 라이브러리 API와 비슷하지만 좀 더 코틀린답게 변경됐다. 예를 들어 코틀린에서는 `toRegex` 확장 함수를 사용해 문자열을 정규식으로 변환할 수 있다.

> 이런 간단한 경우에는 꼭 정규식을 쓸 필요가 없다. split 확장 함수를 오버로딩한 버전 중에는 구분 문자열을 하나 이상 인자로 받는 함수가 있다.

```kotlin
println("12.345-6.A".split(".","-")) // 여러 구분 문자열을 지정한다.
// [12, 345, 6, A]
```

이 경우 "12.345-6.A".split('.','-') 처럼 문자열 대신 문자를 인자로 넘겨도 마찬가지 결과를 볼 수 있다. 이렇게 여러 문자를 받을 수 있는 코틀린 확장 함수는 자바에 있는 단 하나의 문자만 받을 수 있는 메소드를 대신한다.

---

#### 2. 자바: 자바에서는 무조건 정규식으로만 넘겨야 하는가?

**네, 기본적으로 자바의 `String.split()` 메서드는 인자로 들어온 문자열을 무조건 정규식으로만 처리합니다.**

자바의 `split` 메서드 시그니처는 다음과 같습니다.

```java
public String[] split(String regex)  // 인자 이름 자체가 regex(정규식)입니다.
```

이로 인해 자바에서는 다음과 같은 제약과 특징이 생깁니다.

#### 자바에서의 한계와 특징:

1. **단순 문자로 자를 때도 정규식 예외 규칙을 생각해야 합니다.**
   - 자바에서 마침표로 문자열을 자르고 싶을 때 `split(".")`이라고 쓰면 아무 결과도 얻지 못합니다. 정규식에서 마침표(`.`)는 '모든 문자'를 뜻하기 때문입니다.
   - 따라서 자바에서는 반드시 정규식 탈출 문자(escape)를 붙여서 `split("\\.")`으로 작성해야 합니다.

2. **여러 구분자를 동시에 지정하려면 정규식 표현법을 써야만 합니다.**
   - 코틀린처럼 `split(".", "-")`과 같이 여러 일반 문자열을 나열하는 메서드가 자바에는 존재하지 않습니다.
   - 자바에서 마침표와 대시를 모두 기준으로 자르고 싶다면, 무조건 정규식의 OR(`|`) 연산자를 사용하여 `split("\\.|-")` 형태로 작성해야 합니다.

#### 요약하자면

- **코틀린**은 개발자가 실수하기 쉬운 점을 고려하여, **정규식용 `split`** 과 **일반 텍스트용 `split`** 을 메서드 오버로딩을 통해 분리해 놓았습니다.
- **자바**는 `String.split()` 메서드를 사용할 때 입력되는 인자값을 **무조건 정규식으로 해석**하므로, 특수문자(., ?, \*, + 등)로 문자열을 자를 때는 항상 정규식 문법에 맞추어 이스케이프 처리를 해주어야 합니다.

### 3.5.2 정규식과 3중 따옴표로 묶은 문자열

다른 예로 두 가지 다른 구현을 만들어보자. 첫 번째 구현은 String을 확장한 함수를 사용하고 두 번째 구현은 정규식을 사용한다. 우리가 할 일은 파일의 전체 경로명을 디렉터리, 파일 이름, 확장자로 구분하는 것이다. 코틀린 표준 라이브러리에는 어떤 문자열에서 구분 문자열이 맨 나중(또는 처음)에 나타난 곳 뒤(또는 앞)의 부분 문자열을 반환하는 함수가 있다. 이런 함수를 사용해 경로 파싱을 구현한 버전은 다음과 같다.

> "\*/Users/yole/kotlin-book/chapter.adoc"

리스트 3.9 String 확장 함수를 사용해 경로 파싱하기

```kotlin
fun parsePath(path: String) {
    val directory = path.substringBeforeLast("/")
    val fullname = path.substringAfterLast("/")
    val filename = fullName.substringBeforeLast(".")
    val extension = fullName.substringAfterLast(".")

    println("Dir: $directory, name: $fileName, ext: $extension")

}
// parsePath("/Users/yole/kotlin-book/chapter.adoc")

// Dir: /Users/yole/kotlin-book, name: chapter, ext: adoc

```

> 코틀린에서는 정규식을 사용하지 않고도 문자열을 쉽게 파싱할 수 있다. 정규식은 강력하긴 하지만 나중에 알아보기 힘든 경우가 많다. 정규식을 표현할 때는 코틀린 라이브러리를 사용하면 더 편하다. 다음은 같은 작업을 정규식을 활용해 구현한 프로그램이다.

```kotlin
fun parsePath(path: String) {
    val regex = """(.+)/(.+)\.(.+)""".toRegex()
    val matchResult = regex.matchEntire(path)
    if (matchResult != null) {
        val (directory, filename, extension) = matchResult.destructed
        println("Dir: $directory, name: $filename, ext: $extension")
    }
}
```

> 이 예제에서는 3중 따옴표 문자열을 사용해 정규식을 썼다. 3중 따옴표 문자열에서는 역슬래시(\)를 포함한 어떤 문자도 이스케이프할 필요가 없다. 예를 들어 일반 문자열을 사용해 정규식을 작성하는 경우 마침표 기호를 이스케이프하려면 \\. 라고 써야 하지만, 3중 따옴표 문자열에서는 \. 라고 쓰면 된다. 이 예제에서 쓴 정규식은 슬래시와 마침표를 기준으로 경로를 세 그룹으로 분리한다. 패턴 .은 임의의 문자와 매치될 수 있다. 따라서 첫 번째 그룹인 (.+)는 마지막 슬래시까지 모든 문자와 매치된다. 이 부분 문자열에는 마지막 슬래시를 제외한 모든 슬래시도 들어간다. 비슷한 이유로 두 번째 그룹에도 마지막 마침표 전까지 모든 문자가 들어간다. 세 번째 그룹에는 나머지 모든 문자가 들어간다.

> 이제 예제의 parsePath 함수 구현을 설명한다. 우선 정규식을 만들고, 그 정규식을 인자로 받은 path에 매치시킨다. 매치에 성공하면(결과가 null이 아니면) 그룹별로 분해한 매치 결과를 의미하는 destructed 프로퍼티를 각 변수에 대입한다. 이때 사용한 구조 분해 선언은 Pair로 두 변수를 초기화할 때 썼던 구문과 같다.

### 3.5.3 여러 줄 3중 따옴표 문자열

> 3중 따옴표 문자열을 문자열 이스케이프를 피하기 위해서만 사용하지는 않는다. 3중 따옴표 문자열에는 줄 바꿈을 표현하는 아무 문자열이나 그대로 들어간다. 따라서 3중 따옴표를 쓰면 줄 바꿈이 들어있는 프로그램 텍스트를 쉽게 문자열로 만들 수 있다. 예제는 ASCII 아트를 하나 출력한다.

```kotlin
val kotlinLogo = """| //
                   .| //
                   .|/\\"""

// println(kotlinLogo.trimMargin("."))
| //
| //
|/\
```

> 여러 줄 문자열(여러 줄 문자열은 3중 따옴표 문자열이다)에는 들여쓰기나 줄 바꿈을 포함한 모든 문자가 들어간다. 여러 줄 문자열을 코드에서 더 보기 좋게 표현하고 싶다면 들여쓰기를 하되 들여쓰기의 끝부분을 특별한 문자열로 표시하고, `trimMargin`을 사용해 그 문자열과 그 직전의 공백을 제거한다. 이 예제에서는 마침표를 들여쓰기 구분 문자열로 사용했다.

> 여러 줄 문자열에는 줄 바꿈이 들어가지만 줄 바꿈은 `\n` 과 같은 특수 문자를 사용해 넣을 수는 없다. 반면에 `\` 문자열을 넣고 싶으면 이스케이프할 필요가 없다. 따라서 일반 문자열로 `"C:\\Users\\yole\\kotlin-book"`이라고 쓴 윈도우 파일 경로를 3중 따옴표 문자열로 쓰면 `"""C:\Users\yole\kotlin-book"""`이다.

> 3중 따옴표 문자열 안에 문자열 템플릿을 사용할 수도 있다. 그러나 3중 따옴표 문자열 안에서는 이스케이프를 할 수 없기 때문에 문자열 템플릿의 시작을 표현하는 `$`를 넣어야 한다면 `val price = """${'$'}99.9"""` 처럼 어쩔 수 없이 문자열 템플릿 안에 `'$'` 문자를 넣어야 한다.

> 프로그래밍 시 여러 줄 문자열이 요긴한 분야로 테스트를 꼽을 수 있다. 테스트에서는 여러 줄의 텍스트 출력을 만들어내는 연산을 실행하고
> 그 결과를 예상 결과와 비교해야 하는 경우가 자주 있다. 여러 줄 문자열은 테스트의 예상 출력을 작성할 때 가장 완벽한 해법이다. 복잡하게 이스케이프를 쓰거나 외부 파일에서 텍스트를 불러올 필요가 없다. 단지 3중 따옴표 사이에 HTML이나 텍스트를 넣으면 된다. 그리고 소스코드에서 더 보기 좋게 하려면 앞에서 본 `trimMargin` 확장 함수를 사용하면 된다.

## 3.6 코드 다듬기: 로컬 함수와 확장

> 많은 개발자들이 좋은 코드의 중요한 특징 중 하나가 중복이 없는 것이라 믿는다. 그래서 그 원칙에는 반복하지 말라(DRY, Don't Repeat Yourself)라는 이름도 붙어있다. 하지만 자바 코드를 작성할 때는 DRY 원칙을 피하기는 쉽지 않다. 많은 경우 메소드 추출(Extract Method) 리펙토링을 적용해서 긴 메소드를 부분부분 나눠서 각 부분을 재활용할 수 있다. 하지만 그렇게 코드를 리펙토링하면 클래스 안에 작은 메소드가 많아지고 각 메소드 사이의 관계를 파악하기 힘들어서 코드를 이해하기 더 어려워질 수도 있다. 리팩토링을 진행해서 추출한 메소드를 별도의 내부 클래스 안에 넣으면 코드를 깔끔하게 조직할 수는 있지만, 그에 따른 불필요한 준비 코드가 늘어난다.

> 코틀린에는 더 깔끔한 해법이 있다. 코틀린에서는 함수에서 추출한 함수를 원 함수 내부에 중첩시킬 수 있다. 그렇게 하면 문법적인 부가 비용을 들이지 않고도 깔끔하게 코드를 조직할 수 있다.
> 흔히 발생한느 코드 중복을 로컬 함수를 통해 어떻게 제거할 수 있는지 살펴보자.

> 다음 리스트에는 사용자를 데이터베이스에 저장하는 함수가 있다. 이때 데이터베이스에 사용자 객체를 저장하기 전에 각 필드를 검증해야 한다.

리스트 3.11 코드 중복을 보여주는 예제

```kotlin
class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {
    if (user.name.isEmpty()) {
        throw IllegalArgumentException(
            "Can't save user $(user.id): empty Name"
        )
    }

    if (user.address.isEmpty()) {
        throw IllegalArgumentException(
            "Can't save user $(user.id): empty Address"
        )
    }

    // user를 데이터베이스에 저장한다.
}

saveUser(User(1, "", ""))
// java.lang.IllegaArgumentException: Can't save user 1: empty Name
```

> 여기서는 코드 중복이 그리 많지 않다. 하지만 클래스가 사용자의 필드를 검증할 때 필요한 여러 경우를 하나씩 처리하는 메소드로 넘쳐나기를 바라지는 않을 것이다. 이런 경우 검증 코드를 로컬 함수로 분리하면 중복을 없애는 동시에 코드 구조를 깔끔하게 유지하 수 있다. 다음 리스트는 그런 변경이 어떻게 작용하는지 보여준다.

리스트 3.12 로컬 함수를 사용해 코드 중복 줄이기

```kotlin
class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {

    // 한 필드를 검증하는 로컬 함수를 정의한다.
    fun validate(user: User, value: String, fieldName : String) {
        if (value.isEmpty()) {
        throw IllegalArgumentException(
            "Can't save user ${user.id}: empty $fieldName"
        )
        }

    }
    // 로컬 함수를 호출해서 각 필드를 검증한다.
    validate(user, user.name, "Name")
    validate(user, user.address, "Address")

    // user를 데이터베이스에 저장한다.
}
```

> 이제 검증 로직 중복은 사라졌고, 필요하면 `User`의 다른 필드에 대한 검증도 쉽게 추가할 수 있다. 하지만 `User` 객체를 로컬 함수 하나하나 전달해야 한다는 점은 아쉽다. 다행이지만 사실은 전혀 그럴 필요가 없다. 로컬 함수는 자신이 속한 바깥 함수의 모든 파라미터와 변수를 사용할 수 있다. 이런 성질을 이용해 불필요한 `User` 파라미터를 없애보자.

리스트 3.13 로컬 함수에서 바깥 함수의 파라미터 접근하기

```kotlin

class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {
    // 이제 saveUser 함수의 user 파라미터를 중복 사용하지 않는다.
    fun validate(value: String, fieldName: String) {
        if (value.isEmpty()) {
            // 바깥 함수의 파라미터에 직접 접근할 수 있다.
            throw IllegalArgumentException(
                "Can't save user ${user.id}: " + "empty $fieldName"
            )
        }
    }

    validate(user.name, "Name")
    validate(user.address, "Address")

    // user를 데이터베이스에 저장한다.
}


```

이 예제를 더 개선하고 싶다면 검증 로직을 `User` 클래스를 확장한 함수로 만들 수도 있다.

리스트 3.14 검증 로직을 확장 함수로 추출하기

```kotlin

class User(val id: Int, val name: String, val address: String)

fun User.validateBeforeSave() {
    fun validate(value:String, fieldName: String) {
        if (value.isEmpty()) {
            throw IllegalArgumentException(
                "Can't save user $id: empty $fieldName"
            )
        }
    }

    validate(name, "Name")
    validate(address, "Address")
}

fun saveUser(user: User) {
    user.validateBeforeSave() // 확장함수를 호출한다.
    // user를 데이터베이스에 저장한다.
}
```

> 코드를 확장 함수로 뽑아내는 기법은 놀랄만큼 유용하다. `User`는 라이브러리에 있는 클래스가 아니라 여러분 자신의 코드 기반에 있는 클래스지만, 이 경우 검증 로직은 `User`를 사용하는 다른 곳에는 쓰이지 않는 기능이기 때문에 User에 포함시키고 싶지는 않다. `User`를 간결하게 유지하면 생각해야 할 내용이 줄어들어서 더 쉽게 코드를 파악할 수 있다. 반면 한 객체만을 다루면서 객체의 비공개 데이터를 다룰 필요는 없는 함수는 리스트 3.14처럼 확장 함수로 만들면 객체.멤버처럼 수신 객체를 지정핟지 않고도 공개된 멤버 프로퍼티나 메소드에 접근할 수 있다.

> 확장 함수를 로컬 함수로 정의할 수도 있다. 즉 `User.validateBeforeSave`를 `saveUser` 내부에 로컬 함수로 넣을 수 있다. 하지만 중첩된 함수의 깊이가 깊어지면 코드를 읽기가 상당히 어려워진다. 따라서 일반적으로는 한 단계만 함수를 중첩시키라고 권장한다.

---

#### 1. "User는 내 코드지만, User 클래스 안에 검증 로직을 넣고 싶지 않다"는 의미

보통 "내가 직접 만든 클래스(`User`)니까, 검증 메서드도 클래스 내부에 정의하면 되는 것 아닌가?"라고 생각할 수 있습니다. 하지만 소프트웨어 설계 관점에서는 다음과 같은 이유로 분리하는 것이 좋습니다.

- **클래스의 단순성 유지:** `User` 클래스는 사용자의 이름, 주소 등 '데이터'만 담는 가벼운 역할(DTO 등)만 하는 것이 좋습니다.
- **관심사의 분리:** 이 검증 로직(`validateBeforeSave`)은 오직 **"데이터베이스에 저장하기 직전"** 에만 필요한 특수한 기능입니다. 만약 화면에 단순히 사용자 정보를 보여주기만 하는 다른 코드 영역에서는 이 검증 로직이 전혀 필요 없습니다.
- **결론:** 클래스 내부를 복잡하게 만들지 않고, 저장 기능이 필요한 곳 근처에서만 쓸 수 있도록 **확장 함수(Extension Function)** 로 따로 빼서 정의하는 것이 깔끔하다는 뜻입니다.

---

### 2. "확장 함수를 로컬 함수로 정의한다"는 것의 실제 코드 모습

책의 설명 중 *"User.validateBeforeSave를 saveUser 내부에 로컬 함수로 넣을 수 있다"*를 코드로 표현하면 다음과 같습니다.

```kotlin
// 함수 안에 함수(로컬 함수)가 있고, 그 안에 또 함수가 중첩된 구조
fun saveUser(user: User) {

    // 1단계 중첩: saveUser 내부에 정의된 로컬 확장 함수
    fun User.validateBeforeSave() {

        // 2단계 중첩: validateBeforeSave 내부에 정의된 로컬 함수
        fun validate(value: String, fieldName: String) {
            if (value.isEmpty()) {
                throw IllegalArgumentException("Can't save user $id: empty $fieldName")
            }
        }

        validate(name, "Name")
        validate(address, "Address")
    }

    // 호출
    user.validateBeforeSave()
    // user를 데이터베이스에 저장하는 로직...
}
```

위 코드처럼 함수(`saveUser`) 안에 또 함수(`User.validateBeforeSave`)가 있고, 그 안에 또 함수(`validate`)가 들어가는 구조를 만들 수 있습니다. 코틀린 문법상으로는 이것이 가능합니다.

---

### 3. "중첩 깊이가 깊어지면 어렵다. 한 단계만 중첩하라"는 권장의 의미

위의 중첩된 코드를 보면 들여쓰기(Indentation)가 깊어지고, 어디서부터 어디까지가 어떤 함수의 범위인지 한눈에 파악하기 어렵습니다.

따라서 책의 저자는 **"이런 식으로 2단계, 3단계씩 안으로 꼬리를 물고 들어가는 중첩은 피하라"** 고 권장하는 것입니다.

가장 좋은 대안은 본문의 **[리스트 3.14]** 처럼 작성하는 것입니다.

```kotlin
// [올바른 예: 딱 1단계만 중첩함]

// 1. 확장 함수는 바깥(파일 수준)에 둡니다.
fun User.validateBeforeSave() {
    // 1단계 중첩: 확장 함수 내부에 검증 로직을 로컬 함수로 정의
    fun validate(value: String, fieldName: String) {
        if (value.isEmpty()) {
            throw IllegalArgumentException("Can't save user $id: empty $fieldName")
        }
    }

    validate(name, "Name")
    validate(address, "Address")
}

// 2. 저장 함수 역시 바깥에 둡니다.
fun saveUser(user: User) {
    user.validateBeforeSave() // 필요할 때 호출만 함 (중첩 없음)
    // 저장 로직...
}
```

이렇게 작성하면:

- `User` 클래스는 여전히 깨끗하게 유지됩니다.
- `validateBeforeSave` 내부에는 `validate`라는 로컬 함수 딱 하나만 중첩되어 있으므로(중첩 깊이 1단계) 코드를 읽기가 아주 쉽습니다.
- `saveUser` 함수 역시 중첩 없이 깔끔하게 유지됩니다.

## 3.7 요약

- 코틀린은 자체 컬렉션 코드를 정의하지 않지만 자바 클래스를 확장해서 더 풍부한 API를 제공한다.
- 함수 파라미터의 디폴트 값을 정의하면 오버로딩한 함수를 정의할 필요성이 줄어든다. 이름붙인 인자를 사용하면 함수의 인자가 많을 때 함수 호출의 가독성을 더 향상시킬 수 있다.
- 코틀린 파일에서 클래스 멤버가 아닌 최상위 함수와 프로퍼티를 직접 선언할 수 있다. 이를 활용하면 코드 구조를 더 유연하게 만들 수 있다.
- 확장 함수와 프로퍼티를 사용하면 외부 라이브러리에 정의된 클래스를 포함해 모든 클래스의 API를 그 클래스의 소스코드를 바꿀 필요 없이 확장할 수 있다. 확장 함수를 사용해도 실행 시점에 부가 비용이 들지 않는다.
- 중위 호출을 통해 인자가 하나 밖에 없는 메소드나 확장 함수를 더 깔끔한 구문으로 호출할 수 있다.
- 코틀린은 정규식과 일반 문자열을 처리할 때 유용한 다양한 문자열 처리 함수를 제공한다.
- 자바 문자열로 표현하려면 수많은 이스케이프가 필요한 문자열의 경우 3중 따옴표 문자열을 사용하면 더 깔끔하게 표현할 수 있다.
- 로컬 함수를 써서 코드를 더 깔끔하게 유지하면서 중복을 제거할 수 있다.
