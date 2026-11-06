import threading
import time

class BankAccount:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.lock = threading.Lock()
    

    def deposit(self, amount):
        with self.lock:
            current = self.balance
            # 경쟁 상태를 유발하기 위해 미세한 지연 추가
            time.sleep(0.00001)
            self.balance = current + amount
        

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                current = self.balance
                time.sleep(0.00001)
                self.balance = current - amount

account = BankAccount(1000)

def user_deposit():
    for i in range(500):
        print(f"{i}번째 입금")
        account.deposit(100)

def user_withdraw():
    for i in range(500):
        print(f"{i}번째 출금")
        account.withdraw(100)

if __name__ == "__main__":

    t1 = threading.Thread(target=user_deposit)
    t2 = threading.Thread(target=user_withdraw)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"최종 잔액: {account.balance}원")




