# Activity, Fragment and Parcelize

## Activity 와 Fragment

> **Activity(액티비티)** 와 **Fragment(프래그먼트)** 는 안드로이드 앱의 **'화면(UI)'을 구성하는 핵심 단위**

---

### 1. Activity (액티비티) = 웹의 **"하나의 독립적인 페이지 (Page)"**

액티비티는 사용자가 보는 **스마트폰의 화면 1개**를 의미함.

- **웹 개발 비유:** `index.html`이나 `detail.jsp` 같은 하나의 완성된 웹 페이지, 혹은 특정 URL(ex: `/home`)을 담당하는 **Controller + View**라고 생각할 수 있음.
- **특징:**
  - 앱을 켜면 가장 먼저 나타나는 메인 화면도 하나의 '액티비티'임.
  - 로그인 화면(Login Activity)에서 로그인을 누르면, 메인 화면(Main Activity)으로 넘어감. (웹에서 화면 전환/Redirect가 일어나는 것과 같음)

### 2. Fragment (프래그먼트) = 웹의 **"부분 화면 (Component / Partial View)"**

프래그먼트는 액티비티(전체 화면) 안에서 **일부분을 차지하는 조각 화면**임. 혼자서는 존재할 수 없고, 반드시 액티비티 위에 얹혀서 동작해야 한다.

- **웹 개발 비유:**
  - React나 Vue의 **컴포넌트(Component)**
  - JSP의 `<jsp:include>`, Thymeleaf의 `fragment`
  - 웹 페이지 안의 특정 영역(사이드바, 탭 메뉴 콘텐츠 등)
- **특징:**
  - 하나의 액티비티(화면) 안에 여러 개의 프래그먼트를 넣을 수 있음.
  - 하단 탭 바(Bottom Navigation)를 눌러 화면 내용이 바뀔 때, 보통 전체 액티비티가 바뀌는 게 아니라 **액티비티 안의 프래그먼트만 교체**되는 방식을 쓴다. (웹의 SPA/Ajax와 비슷한 느낌)

---

### 💡 왜 직렬화가 필요한가?

웹 개발에서 화면 A에서 화면 B로 데이터를 넘길 때,
단순한 문자열(String)이나 숫자(int)는 URL 파라미터(`?id=123`)로 넘길 수 있지만, **복잡한 Java 객체(예: `User`, `Order`)를 URL에 그대로 담아서 다른 페이지로 넘길 수 없음.** 보통은 객체를 JSON으로 변환(직렬화)해서 통신하거나, DB/세션에 저장해두고 ID만 넘김.

안드로이드도 마찬가지임.

- 안드로이드에서는 화면(Activity A)에서 다음 화면(Activity B)으로 넘어갈 때, 안드로이드 운영체제(OS)가 이 전환을 중간에서 처리해 준다.
- 이때 데이터를 전달하려면 **`Intent(인텐트)`**라는 택배 상자 같은 것을 이용한다.
- 그런데 웹에서 URL에 Java 메모리 주소값을 넘길 수 없듯, 안드로이드 OS도 메모리에 띄워진 **객체 그 자체(메모리 참조값)를 다른 화면으로 바로 휙 던져줄 수 없음.** (화면마다 독립적인 생명주기를 가지며, OS를 거쳐 통신하기 때문에)

**그래서 나오는 결론:**

> "객체(User, Board 등)를 통째로 다음 화면(Activity/Fragment)으로 넘기고 싶으면, 그 객체를 납작하게 압축해서 택배 상자(Intent)에 넣을 수 있는 형태인 **직렬화(Serialization)** 를 해야 함."

- **Serializable:** 자바에서 쓰는 `java.io.Serializable` 인터페이스. 하지만 리플렉션을 사용해서 안드로이드에서는 성능이 다소 느립니다.
- **Parcelable:** 안드로이드 전용으로 만들어진 **초고속 직렬화 인터페이스**. 안드로이드 개발에서는 객체를 넘길 때 보통 이 방식을 표준으로 사용함.

**요약하자면:**
"화면A(Activity)에서 화면B(Activity)로 내가 만든 `Member` 객체를 넘겨주고 싶은데, 객체를 넘기려면 `Member` 클래스에 `Parcelable` 인터페이스를 구현해서 직렬화 가능하게 만들어줘야 한다"

## Parcelize

### Parcelize 없이 데이터 전달하기 예시

```kotlin
data class Member(
  val id: String,
  val password: String
)

// 현재 액티비티에서 PostActivity로 데이터를 넘긴다고 가정
val member = Member(id="lohan", password="nahol123")

val intent = Intent(this, PostActivity::class.java).apply {
  putExtra("member_id", member.id)
  putExtra("member_password", member.password)
}
startActivity(intent)

// PostActivity에서 데이터 받기
override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  setContentView(R.layout.activity_post)

  val memberId = intent.getStringExtra("member_id")
  val memberPassword = intent.getStringExtra("member_password")

  // 받은 데이터 사용
  if (memberId != null && memberPassword != null) {
    val member = Member(id = memberId, password = memberPassword)
    // member 객체 사용
  }
}
```

> 만약 여러 개의 데이터를 전달하고 받아야하는 상황이면

1. 데이터 클래스에 필드가 추가될 때마다 `putExtra` 및 `getExtra` 코드를 추가해야 한다. 이렇게 되면 **필드가 많아질수록 코드가 복잡해지고 관리가 어려워짐.** 특히, 앱이 성장하고 유지보수가 길어질수록 수정할 부분이 많아질 수 있음
2. 객체를 Parcelable로 처리하면 User 객체를 그대로 전달하고 사용할 수 있지만, 필드별로 분해해 넘기는 경우 객체의 캡슐화 원칙이 깨질 수 있음. 필드별로 넘기면 해당 객체를 재구성하는 코드가 분산되어 나타남. 객체를 넘기는 의도를 분명히 하고 구조적으로 유지하기 어려워 코드가 중복되고 목적이 분산되어 보이기 쉬움.

### Parcelable

> build.gradle에 `kotlin-parcelize` 플러그인을 추가함

```gradle
plugins {
  id 'kotlin-parcelize'
}
```

```kotlin
import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Member(
  val id: String,
  val password: String
) : Parcelable

// 현재 액티비티에서 PostActivity로 데이터를 넘긴다고 가정
val member = Member(id = "lohan123", password = "nahol123")

val intent = Intent(this, PostActivity::class.java).apply {
  putExtra("member_data", member)
}
startActivity(intent)

// PostActivity에서 데이터 받기
override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  setContentView(R.layout.activity_post)

  val member = intent.getParcelableExtra<Member>("member_data")

  // 받은 member 객체 사용
  member?.let {
    // 예: it.id, it.password 사용
  }
}
```

## 기타 문법

### data class란?

> kotlin의 `data class`는 **데이터를 담기 위한 목적의 클래스(DTO, VO)** 를 만들 때 사용하는 코틀린의 특별한 문법

> 자바에서 DTO 클래스를 만들 때 필드를 선언하고 나면 `getter, setter, toString(), equals(), hashCode()`를 다 만들어야 하지만 보통 Lombok 라이브러리를 써서 @Data나 @Getter, @Setter 어노테이션을 붙임.

> 코틀린의 data class는 롬복의 @Data를 언어 자체에서 지원하는 기능

다음 코드가 코틀린의 `data class Member(val id: String, val password: String)`을 자바로 풀어쓴 코드

```java
@Data
public class Member {
  private final String id;
  private final String password;
}
```

- 일반 `class`와 달리 `data class`라는 키워드를 붙이면, 컴파일러가 알아서 `toString()`, `equals()`, `hashCode()`, `copy()` 같은 메서드를 모두 자동으로 만들어 줌.

### `PostActivity::class.java`에서 `::`의 의미

> 자바의 `PostActivity.class`와 완전히 똑같은 역할을 함.

> 안드로이드에서 화면을 이동할 때 사용하는 `Intent`는 안드로이드 SDK에 포함된 자바(Java) 클래스임. 그래서 Intent에게 "다음 띄울 화면이 어떤 클래스야?"라고 알려줄 때 자바의 Class 객체를 넘겨줘야 함.

- 자바 코드였다면: `new Intent(this, PostActivity.class);`
- 코틀린에서는: 코틀린은 자바와 클래스를 참조하는 방식이 다름. 코틀린에서 클래스 참조를 가져올 때 **`::`(더블 콜론)** 을 사용함.
  - `PostActivity::class` : 코틀린의 클래스 객체(`KClass` 타입)를 가져옵니다.
  - `.java` : 그 코틀린 클래스 객체를 자바의 클래스 객체(`java.lang.Class` 타입)로 변환해줌

### `.apply {...}`는?

> 코틀린의 스코프 함수(Scope Function) 중 하나. 자바로 치면 객체를 생성하고 변수명을 반복해서 쓰는 수고를 덜어주는 문법임.

[자바 코드]
자바에서는 Intent 객체를 만들고 데이터를 넣을 때 이렇게 `intent.`을 계속 반복해야 함.

```java
Intent intent = new Intent(this, PostActivity.class);
intent.putExtra("member_id", member.getId());
intent.putExtra("member_password", member.getPassword());
startActivity(intent);
```

[Kotlin 코드 - apply 사용]
코틀린에서는 `.apply{}` 블록 안에서는 `intent.`을 생략하고 바로 메서드(`putExtra`)를 부를 수 있음

```kotlin
val intent = Intent(this, PostActivity::class.java).apply {
  // 이 중괄호 안에서는 내가 곧 intent다 (this == intent)
  putExtra("member_id", member.id)
  putExtra("member_password", member.password)
}
startActivity(intent)
```

### 내장(Built-in) 함수

1. `startActivity(intent)`
   이 함수는 안드로이드의 `Activity` 클래스에 이미 정의되어 있는 기본 함수임.

- 역할: "안드로이드 OS야, 내가 만든 이 Intent(택배 상자/요청서)를 보고 다음 화면(Activity)을 띄워줘!"라고 명령하는 함수
- 웹 개발 비유:
  - Servlet의 `response.sendRedirect("/post.do");
  - Spring Controller에서 `return "redirect:/post";` 하거나 특정 뷰를 호출하는 것과 똑같은 역할을 함.

2. `putExtra("key", value)`
   이 함수는 데이터를 담아 나르는 `Intent` 클래스에 정의되어 있는 함수

- 역할: 다음 화면으로 넘길 데이터를 **Key-Value 형태로 저장**함. (내부적으로 Map처럼 동작함)
- 특징: 오버로딩(Overloading)이 엄청나게 많이 되어 있어서, String, int, boolean을 물론이고 직렬화된 객체(Parcelable, Serializable)까지 다 넣을 수 있음
- 웹 개발 비유:
  - Servlet의 `request.setAttribute("key", value);
  - Spring의 model.addAttribute("key", value);
  - 또는 GET 방식의 URL 파라미터 `?key=value`를 세팅하는 것과 같음

3. `getStringExtra()`, `getParcelableExtra()`
   이 함수들도 `Intent` 클래스에 정의되어 있는 함수. 다음 화면(도착지)에서 데이터를 꺼낼 때 사용함.

- 역할: 이전 화면에서 `putExtra`로 넣어둔 데이터를 Key를 이용해 꺼냄
- 특징: 웹에서는 `request.getAttribute()` 하나로 다 꺼내서 캐스팅(Casting)을 하지만, 안드로이드의 Intent는 타입별로 꺼내는 함수가 따로 나뉘어져 있음.
  - 문자열을 꺼낼 땐 `getStringExtra("key")
  - 숫자를 꺼낼 땐 `getIntExtra("key", 기본값)`
  - 직렬화된 객체를 꺼낼 땐 `getParcelableExtra("key")`
- 웹 개발 비유:
  - Servlet의 `request.getParameter("key");` 또는 `request.getAttribute("key");`
  - Spring의 `@RequestParam("key")` 또는 `@ModelAttribute`로 값을 받아오는 것과 같음.

> 웹 개발에서 클라이언트의 요청(Request)을 받아 데이터를 꺼내고(getParameter), 모델에 데이터를 담아(addAttribute), 다음 페이지로 이동(redirect)시키는 일련의 과정이 있듯이,

> 안드로이드에서는 그 과정을 Intent 객체 생성 👉 putExtra로 데이터 담기 👉 startActivity로 화면 이동 👉 새 화면에서 get...Extra로 데이터 꺼내기 라는 공식(API)으로 안드로이드 프레임워크가 제공하고 있음!

### `savedInstanceState` 란?

> 안드로이드 운영체제는 화면 회전, 메모리 부족으로 인한 앱 종료 등의 상황에서 액티비티(화면)를 파괴하고 새로 생성(Recreate)하는 경우가 있습니다.
> 이때 기존 화면의 상태(예: 입력 필드의 텍스트, 스크롤 위치 등) 정보를 잃지 않도록 임시로 저장해 두는 객체가 **`savedInstanceState`** 입니다.
>
> - 처음 화면이 실행될 때: 이전 상태가 없으므로 `null`이 전달됩니다.
> - 화면이 재생성될 때: 이전에 저장된 데이터가 담긴 `Bundle` 객체가 전달되어 기존 상태를 복원할 수 있게 합니다.

### `savedInstanceState: Bundle?`

> 이 코드는 메서드의 파라미터 정의입니다. 자바와 코틀린의 변수/파라미터 선언 방식의 차이에서 비롯됨.

- 자바 방식: `타입 변수명` -> `Bundle savedInstanceState`
- 코틀린 방식: `변수명: 타입` -> `savedInstanceState: Bundle?`
  즉, `Bundle?` 타입의 `savedInstanceState`라는 이름의 파라미터를 받는다는 의미

### 물음표(?)의 의미 (코틀린의 핵심 기능: Null Safety)

> 코틀린은 Null Pointer Exception(NPE)을 컴파일 단계에서 방지하기 위해 **"Null을 가질 수 있는 타입(Nullable)"** 과 **"Null을 가질 수 없는 타입(Non-Nullable)"** 을 엄격히 구분함.
> 여기서 타입 뒤에 붙은 물음표(`?`)는 이 변수가 `null`일 수도 있음을 뜻한다.

- `Bundle` (물음표 없음): 절대 `null`이 될 수 없음. 만약 여기에 `null`을 대입하려 하면 컴파일 에러가 발생합니다.
- `Bundle?` (물음표 있음): `Bundle` 객체가 들어올 수도 있고, `null`이 들어올 수도 있습니다.

> 액티비티가 처음 실행될 때는 이전 상태가 없기 때문에 `savedInstanceState`에 `null`이 전달되어야 합니다. 따라서 이 파라미터는 반드시 `null`을 허용하는 타입인 `Bundle?`로 정의되어야 합니다.
