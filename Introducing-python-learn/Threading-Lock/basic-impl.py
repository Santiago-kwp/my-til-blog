class InsufficientFunds(Exception):
    pass

class AccountNotFound(Exception):
    pass

class BankService:
    def __init__(self):
        self._balances: dict[str, int] = {}

    # 계좌 생성
    def create(self, aid: str, initial: int = 0) -> None:
        if aid in self._balances:
            raise ValueError("duplicate account")
        self._balances[aid] = initial

    # 계좌 조회
    def balance(self, aid: str) -> int:
        if aid not in self._balances:
            raise AccountNotFound(aid)
        return self._balances[aid]

    # 계좌 입금
    def deposit(self, aid: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balances[aid] = self.balance(aid) + amount

    # 계좌 출금
    def withdraw(self, aid: str, amount: int) -> None:
        bal = self.balance(aid)
        if bal < amount:
            raise InsufficientFunds(aid)
        self._balances[aid] = bal - amount