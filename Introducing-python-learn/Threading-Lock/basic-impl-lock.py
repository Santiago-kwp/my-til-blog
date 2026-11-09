import threading
class InsufficientFunds(Exception):
    pass

class AccountNotFound(Exception):
    pass

class BankService:
    def __init__(self):
        self._balances: dict[str, int] = {}
        self._lock = threading.Lock()

    def withdraw(self, aid: str, amount: int) -> None:
        with self._lock:
            bal = self._balance_unlocked(aid)
            if bal < amount:
                raise InsufficientFunds(aid)
            self._balances[aid] = bal - amount

    def deposit(self, aid: str, amount: int) -> None:
        if amount <= 0: raise ValueError

        with self._lock:
            self._balances[aid] = self._balance_unlocked(aid) + amount

    def transfer(self, src: str, dst: str, amount: int) -> None:
        with self._lock:
            if self._balance_unlocked(str) < amount:
                raise InsufficientFunds(src)
            self._balances[src] -= amount
            self._balances[dst] = self._balance_unlocked(dst) + amount

    def _balance_unlocked(self, aid: str):
        if aid not in self._balances:
            raise AccountNotFound(aid)
        return self._balances[aid]


