# Kotlin에서의 if와 when

> Kotlin에서는 `if` 와 `when` 둘 다 조건 분기에 사용하지만, 용도가 조금 다르다.

## 1. if
일반적인 조건식을 처리할 때 사용함.

```kotlin
val score = 85

if (score >= 90) {
    println("A")
} else if (score >= 80) {
    println("B")
} else {
    println("C")
}
```

또는 Kotlin에서는 `if` 도 expression(표현식)이라 값을 반환할 수 있음

```kotlin
val result = if (score >= 60) "합격" else "불합격"
```

### if를 사용하는 경우
- 범위 비교 (`>`,`<`,`>=`,`<=`)
- 여러 조건을 조합 (`&&`, `||`)
- 복잡한 Boolean 조건

```kotlin
if (speed > 1.0 && confidence > 0.8) {
    // 유속 계산
}
```

---

## 2. when
Java의 `switch`보다 훨씬 강력한 문법

```kotlin
when (status) {
    0 -> println("대기")
    1 -> println("실행")
    2 -> println("완료")
    else -> println("알 수 없음")
}
```

값 매핑이 많을 때 가독성이 좋음

### expression으로도 사용 가능
```kotlin
val statusText = when (status) {
    0 -> "대기"
    1 -> "실행"
    2 -> "완료"
    else -> "알 수 없음"
}
```

### 여러 값 매칭
```kotlin
when (code) {
    200, 201, 204 -> "성공"
    400, 404 -> "클라이언트 오류"
    else -> "기타"
}
```

### 범위 매칭
```kotlin
when (score) {
    in 90..100 -> "A"
    in 80..89 -> "B"
    else -> "C"
}
```

### 타입 검사
```kotlin
when (obj) {
    is String -> println(obj.length)
    is Int -> println(obj * 2)
    else -> println("unknown")
}
```

### 조건식 형태
`when` 뒤에 값을 안 써도 됩니다.
```kotlin
when {
    score >= 90 -> "A"
    score >= 80 -> "B"
    else -> "C"
}
```
위는 사실상 if-else if 체인과 동일함

## if 와 when 구분 사용 예

### if 추천
조건 자체가 중요할 때
```kotlin
if (velocity > threshold && quality > 0.8) {
    ...
}

if (frameCount > 10 && !isTracking) {
    ...
}
```

### when 추천
하나의 값을 여러 경우로 나누는 경우
```kotlin
when (analysisMode) {
    AnalysisMode.STIV -> ...
    AnalysisMode.LSPIV -> ...
    AnalysisMode.OPTICAL_FLOW -> ...
}
```
`Enum`을 처리할 때 많이 사용함

```kotlin
enum class State {
    READY,
    RUNNING,
    STOPPED
}

when (state) {
    State.READY -> ...
    State.RUNNING -> ...
    State.STOPPED -> ...
}
```

> "조건에 따라 검사한다" -> `if`
"값에 따라 분기한다" -> `when`
"boolean 조건 -> if", "enum/상태값/타입 분기 -> when" 패턴이 많이 사용됨.