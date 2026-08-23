import unittest # TestCase 슈퍼클래스 사용에 필요한 unittest 패키지를 가져온다.

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


if __name__ == '__main__':
    unittest.main()

"""
파이썬은 unittest 패키지를 가져온 후(import), 
TestCase를 상속하는 클래스를 생성하고 test로 시작하는 이름의 함수 선언을 해야 한다.
독립적 프로그램으로 클래스 실행이 가능하게 하기 위해, 
직접 test_money.py를 실행할 때 unittest.main() 함수를 실행하는
일반적인 파이썬 이디엄(https://doc.python.org/3/library/__main__.html)을 사용한다.
"""