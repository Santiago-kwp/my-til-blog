import threading
from dataclasses import dataclass, field

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
        b = self.get(dst)

        # 교착 상태 방지: 항상 같은 순서(id 오름차순)로 락 획득
        first, second = sorted((a, b), key=lambda x: x.id)
        with first.lock, second.lock:
            if a.balance < amount:
                raise InsufficientFunds(a)
            a.balance -= amount
            b.balance += amount

    """
    정렬을 안하면 생기는 일(교착상태):
    스레드 1: transfer(A->B) A락 획득 -> B락 대기 ...
    스레드 2: transfer(B->A) B락 획득 -> A락 대기 ...
    -> 서로 상대가 가진 락을 영원히 기다림
    교착상태 4가지 필요조건 : 상호배제, 점유와 대기, 비선점, 순환대기. 락 순서 정렬은 순환 대기를 깨는 방법
    acqure(timeout=...) 후 포기하고 재시도하는 건 점유와 대기를 꺠는 방법
    """
    

"""
사용자 ID 같은 임의 키별 락이 필요할 때
"""

from collections import defaultdict

class KeyedLocks:
    def __init__(self):
        self._locks: dict[str, threading.Lock] = defaultdict(threading.Lock)
        self._gaurd = threading.Lock() # 락 딕셔너리 자체도 공유 상태다

    def get(self, key: str) -> threading.Lock:
        with self._guard:
            return self._locks[key]

"""
"락을 담는 dict도 동시에 수정되니 그걸 보호하는 락이 또 필요하다"는 점, 
그리고 "키가 무한히 늘면 메모리 누수 -> 고정 개수 버킷으로 해싱하는 lock striping(`locks[hash(key) % N]`)
으로 해결 가능하다.
"""


