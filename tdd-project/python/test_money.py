import unittest # TestCase 슈퍼클래스 사용에 필요한 unittest 패키지를 가져온다.
import functools # functools 패키지는 reduce 함수를 제공한다.
import operator # operator 패키지는 add 함수를 제공한다.

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
    
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
    
    def times(self, multiplier):
        return Money(self.amount * multiplier, self.currency)
    def divide(self, divisor):
        return Money(self.amount / divisor, self.currency)
    
class Portfolio:
    def __init__(self):
        self.moneys = []

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, currency):
        total = functools.reduce(
            operator.add, map(lambda m: m.amount, self.moneys), 0) # reduce의 마지막 매개변수는 (여기에선 0) 누적되는 결과의 초깃값이다. -> 코드가 빈 배열에도 잘 동작하도록 한다.
        return Money(total, currency)

"""
1. 필요한 패키지들을 가져온다.
2. 람다 표현식을 사용해 self.moneys 배열을 각 Money 객체 amount로만 구성된 map으로 매핑한다.
3. reduce에서 operator.add 연산으로 map을 단일 스칼라값으로 축약한다.
4. 스칼라값을 total로 명명된 변수에 할당한다.
5. 마지막으로 total과 evaluate 메소드의 첫 번째(유일한) 매개변수로 전달된 currency로 새로운 Money 객체를 생성한다.
"""

class TestMoney(unittest.TestCase): # unittest.TestCase 클래스의 자식 클래스가 돼야하는 테스트 클래스다.
    def testMultiplicationInDollars(self): # 테스트 메소드로 인정되기 위해 메소드 이름은 test로 시작해야 한다.
        fiver = Money(5,"USD") # USD 5. 를 표현하는 객체로 Dollar는 아직 존재하지 않는다.
        tenner = fiver.times(2) # 테스트 대상 메소드인 times로 아직 존재하지 않는다.
        self.assertEqual(10, tenner.amount) # assertEqual 단언문으로 실제값과 예상값을 비교한다.
        self.assertEqual("USD",tenner.currency)

    def testMultiplicationInEuros(self):
        tenEuros = Money(10, "EUR")
        twentyEuros = tenEuros.times(2)
        self.assertEqual(20, twentyEuros.amount)
        self.assertEqual("EUR", twentyEuros.currency)

    def testDivision(self):
        originalMoney = Money(4002, "KRW")
        actualMoneyAfterDivision = originalMoney.divide(4)
        expectedMoneyAfterDivision = Money(1000.5, "KRW")
        self.assertEqual(expectedMoneyAfterDivision.amount, actualMoneyAfterDivision.amount)
        self.assertEqual(expectedMoneyAfterDivision.currency, actualMoneyAfterDivision.currency)
    
    def testMultiplicationInKRW(self):
        fiveThousandsWon = Money(5000,"KRW")
        tenThousandsWon = Money(10000,"KRW")
        self.assertEqual(tenThousandsWon, fiveThousandsWon.times(2))
    
    def testAddtion(self):
        fiveDollars = Money(5, "USD")
        tenDollars = Money(10, "USD")
        fifteenDollars = Money(15, "USD")
        portfolio = Portfolio() # 빈 Portfolio 객체를 선언한다.
        portfolio.add(fiveDollars, tenDollars) # 같은 통화의 여러 Money 객체들을 Portfolio 객체에 더한다.
        self.assertEqual(fifteenDollars, portfolio.evaluate("USD")) # Portfolio를 같은 통화로 평가하고 기대하는 Money 객체와 결과를 비교한다.


if __name__ == '__main__':
    unittest.main()

"""
파이썬은 unittest 패키지를 가져온 후(import), 
TestCase를 상속하는 클래스를 생성하고 test로 시작하는 이름의 함수 선언을 해야 한다.
독립적 프로그램으로 클래스 실행이 가능하게 하기 위해, 
직접 test_money.py를 실행할 때 unittest.main() 함수를 실행하는
일반적인 파이썬 이디엄(https://doc.python.org/3/library/__main__.html)을 사용한다.
"""