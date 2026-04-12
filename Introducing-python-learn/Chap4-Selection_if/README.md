# 4장 선택하기: if

## 4.3 비교하기: if, elif, else

> 파이썬에서는 하나의 변수를 다음과 같이 여러 번 비교하는 것을 허용한다.

```python
5 < x < 10
>> True
5 < x < 10 < 999
>> True
```

## 4.4 True와 False

> 다음은 모두 False로 간주된다.

| 불리언       | false |
| ------------ | ----- |
| null         | none  |
| 정수0        | 0     |
| 부동소수점 0 | 0.0   |
| 빈 문자열    | ''    |
| 빈 리스트    | []    |
| 빈 튜플      | ()    |
| 빈 딕셔너리  | {}    |
| 빈 셋        | Set() |

> 이 외에 다른 것들은 True로 간주된다. 파이썬 프로그램은 데이터 자료구조가 False 조건인지 확인하기 위해 진실(truthiness) 혹은 거짓(falsiness)의 정의를 사용한다.

> "진실 혹은 거짓의 정의를 사용한다"는 말은, "파이썬은 모든 객체를 가지고 True인지 False인지 판별할 수 있는 기준을 가지고 있다. 그래서 굳이 `if x == True:`라고 쓰지 않고 `if x:`라고만 써도 파이썬이 알아서 '이 값이 비어있지 않으니 참이구나!'라고 판단한다"는 뜻.

## 4.5 여러 개 비교하기: in

> 한 변수에 여러 값을 비교할 때 파이썬 멤버쉽 연산자(membership operator) in을 사용할 수 있다.

> 딕셔너리의 경우 값 대신 키(`:`의 왼쪽)를 본다

## 4.6 새로운 기능: 바다코끼리 연산자

> 파이썬 3.8의 새로운 바다코끼리 연산자(walrus operator) 형식은 다음과 같다.

`이름 := 표현식`

> 바다 코끼리 연산자를 사용하여 할당과 테스트를 한 단계로 줄일 수 있다.

```python
tweet_limit = 280
tweet_string = "Blah" * 50
if diff := tweet_limit - len(tweet_string) >= 0
    print("A fitting tweet")
else:
    print("Went over by", abs(diff))

>> A fitting tweet
```
