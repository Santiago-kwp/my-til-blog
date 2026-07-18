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

> 이 함수가 어떻게 실행될 수 있는 걸까? JVM이 클래스 안에 들어있는 코드만을 실행할 수 있기 때문에 컴파일러는 이 파일을 컴파일할 때 새로운 클래스를 정의해준다. 코틀린만 사용하는 경우에는 그냥 그런 클래스가 생긴다는 사실만 기억하면 된다. 하지만 이 함수를 자바 등의 다른 JVM 언어에서 호출하고 싶다면 코드가 어떻게 컴파일되는지 알아야 joinToString과 같은 최상위 함수를 사용할 수 있다. 어떻게 코틀린이 join.kt를 컴파일하는지 보여주기 위해 join.kt를 컴파일한 결과와 같은 클래스를 자바 코드로 써보면 다음과 같다.

```java
package strings;

public class JoinKt {
    public static String joinToString(...) {...}
}
```

> 코틀린 컴파일러가 생성하는 클래스의 이름은 최상위 함수가 들어있던 코틀린 소스 파일의 이름과 대응한다. 코틀린 파일의 모든 최상위 함수는 이 클래스의 정적인 메소드가 된다. 따라서 자바에서 joinToString을 호출하기는 쉽다.

```java
import strings.JoinKt;
...
JoinKt.joinToString(list, ", ", "", "");
```

- 최상위 프로퍼티
  > 어떤 데이터를 클래스 밖에 위치시켜야 하는 경우는 흔하지 않지만, 그래도 가끔 유용할 때가 있다. 예를 들어 어떤 연산을 수행한 횟수를 저장하는 var 프로퍼티를 만들 수 있다.

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

> 기본적으로 최상위 프로퍼티도 다른 모든 프로퍼티처럼 접근자 메소드를 통해 자바 코드에 노출된다(val의 경우 게터, var의 경우 게터와 세터가 생긴다). 겉으론 상수처럼 보이는데 실제로는 게터를 사용해야 한다면 자연스럽지 못하다. 더 자연스럽게 사용하려면 이 상수를 `public static final` 필드로 컴파일해야 한다. `const` 변경자를 추가하면 프로퍼티를 `public static final` 필드로 컴파일하게 만들 수 있다.

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

> 이 함수를 호출하는 구문은 다른 일반 클래스 멤버를 호출하는 구문과 똑같다.

`>>> println("Kotlin".lastChar())``
`n`
