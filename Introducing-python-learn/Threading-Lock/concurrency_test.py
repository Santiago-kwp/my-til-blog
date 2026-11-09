from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import threading

class InsufficientFunds(Exception):
    pass

class AccountNotFound(Exception):
    pass



@dataclass
class Account:
    id: str
    balance: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

class BankService:
    def __init__(self):
        self._accounts: dict[str, Account] = {}
        self._registry_lock = threading.Lock() # 계좌 "목록" 보호용

    # 계좌 생성
    def create(self, aid: str, initial: int = 0) -> None:
        with self._registry_lock:
            if aid in self._accounts:
                raise ValueError("duplicate")
            self._accounts[aid] = Account(aid, initial)

    # 계좌 조회
    def _get(self, aid: str) -> Account:
        acc = self._accounts.get(aid)
        if acc is None:
            raise AccountNotFound(aid)
        return acc

    # 외부에서 계좌 금액 조회
    def get_balance(self, aid: str) -> int:
        acc = self._get(aid)
        with acc.lock:  # 조회할 때도 락을 걸어 안전하게 최신 값을 읽음
            return acc.balance

    # 계좌 출금
    def withdraw(self, aid: str, amount:int) -> None:
        acc = self._get(aid)
        with acc.lock:  # 이 계좌만 잠금
            if acc.balance < amount:
                raise InsufficientFunds(aid)
            acc.balance -= amount

    # 계좌 이체
    def transfer(self, src: str, dst: str, amount:int) -> None:
        if src == dst:
            raise ValueError("same amount")
        
        a = self._get(src)
        b = self._get(dst)

        # 교착 상태 방지: 항상 같은 순서(id 오름차순)로 락 획득
        first, second = sorted((a, b), key=lambda x: x.id)
        with first.lock, second.lock:
            if a.balance < amount:
                raise InsufficientFunds(src)
            a.balance -= amount
            b.balance += amount


def test_concurrent_withdraw():
    print("▶ test_concurrent_withdraw 시작...")
    svc = BankService()
    svc.create("A", 1000)
    n = 50
    barrier = threading.Barrier(n)

    def task(_):
        barrier.wait()  # 50개가 모두 준비되면 동시에 출발
        try:
            svc.withdraw("A", 30)
            return True
        except InsufficientFunds:
            return False

    with ThreadPoolExecutor(max_workers=n) as ex:
        results = list(ex.map(task, range(n)))

    assert sum(results) == 33
    assert svc.get_balance("A") == 10


def test_transfer_no_deadlock():
    print("▶ test_transfer_no_deadlock 시작...")
    svc = BankService()
    svc.create("A", 10_000); svc.create("B", 10_000)

    def ping(_):
        svc.transfer("A", "B", 1)
        svc.transfer("B", "A", 1)

    with ThreadPoolExecutor(max_workers=20) as ex:
        list(ex.map(ping, range(1000))) # 교착 상태면 여기서 멈춤

    assert svc.get_balance("A") + svc.get_balance("B") == 20_000 # 총액 보존


# 진입점
if __name__ == "__main__":
    test_concurrent_withdraw()
    test_transfer_no_deadlock()
    print("\n 모든 테스트가 성공적으로 통과되었습니다.") # 통과함