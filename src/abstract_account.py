import abc
from enum import Enum
from decimal import Decimal

class Status(Enum):
    ACTIVE = "Активный"
    FROZEN = "Замороженный"
    CLOSED = "Закрытый"



class AbstractAccount(abc.ABC):

    id_account: str

    user_data: str

    _protect_balance: Decimal

    status: Status

    def __init__(self, id_account, user_data, _protect_balance, status):
        self.id_account = id_account
        self.user_data = user_data
        self._protect_balance = _protect_balance
        self.status = status


    @abc.abstractmethod
    def deposit(self, amount: Decimal):
        pass

    @abc.abstractmethod
    def withdraw(self, amount: Decimal):
        pass

    @abc.abstractmethod
    def get_account_info(self):
        pass
