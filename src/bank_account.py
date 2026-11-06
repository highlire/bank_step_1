from abstract_account import AbstractAccount, Status
from exceptions import InsufficientFundsError, InvalidOperationError, AccountClosedError, AccountFrozenError
import uuid
from enum import Enum
from decimal import Decimal

class Currency(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    KZT = "KZT"
    CNY = "CNY"

class BankAccount(AbstractAccount):

    account_type = "Банковский" #Заглушка, по тз не было информации как его реализовывать

    currency: Currency

    def __init__(self, user_data, _protect_balance = Decimal("0"), currency = Currency.RUB, id_account = None, status=Status.ACTIVE):

    #Userdata analysis#
        if not isinstance(user_data,str):
            raise TypeError("Некорректный тип строки.")
        userdata_process = user_data.strip().split()
        if len(userdata_process) != 3:
            raise ValueError("Некорректный формат строки.")
        normalize_userdata = " ".join(userdata_process)

    #Protected_balance analysis#
        if not isinstance(_protect_balance, Decimal):
            raise TypeError("Некорректный тип баланса.")
        if (not _protect_balance.is_finite()) or (_protect_balance < Decimal(0.0)):
            raise ValueError("Некорректный баланс.")

    #Currency analysis#
        if not isinstance(currency, Currency):
            raise TypeError("Передан некорректный тип валюты.")         

    #ID analysis#
        if id_account is None : 
            id_account = str(uuid.uuid4())
        if not isinstance(id_account,str):
            raise TypeError("Передан неверный тип ID.")
        if len(id_account.strip()) < 4:
            raise ValueError("Передан неверный ID.")

        #Status analysis#
        if not isinstance(status, Status):
            raise TypeError("Передан некорректный тип статуса.") 
        if status == Status.CLOSED:
            raise InvalidOperationError("Невозможно создать счет со статусом 'закрыт'.")
        

 
        
        super().__init__(id_account.strip(), normalize_userdata, _protect_balance, status)



        self.currency = currency



    def __str__(self):
        return f"***Банковский счет***, \nТип счета: {self.account_type}\nФИО: {self.user_data}\nID (последние 4 цифры): {self.id_account[-4:]}\nСтатус: {self.status.value}\nТекущий Баланс: {self._protect_balance:.2f} {self.currency.name}"

    def deposit(self, amount: Decimal):
        if not isinstance(amount, Decimal):
            raise TypeError("Передан некорректный тип данных для пополнения.")
        if (not amount.is_finite()) or (amount <= Decimal(0.0)):
            raise InvalidOperationError("Передано некорректное значение для пополнения.")
        if self.status.value == "Закрытый":
            raise AccountClosedError("Невозможно изменить баланс, аккаунт закрыт.")
        if self.status.value == "Замороженный":
            raise AccountFrozenError("Невозможно изменить баланс, аккаунт заморожен.")
        self._protect_balance += amount

    def withdraw(self, amount: Decimal):
        if not isinstance(amount, Decimal):
            raise TypeError("Передан некорректный тип данных для снятия.")
        if (not amount.is_finite()) or (amount <= Decimal(0.0)):
            raise InvalidOperationError("Передано некорректное значение для снятия.")
        if self.status.value == "Закрытый":
            raise AccountClosedError("Невозможно изменить баланс, аккаунт закрыт.")
        if self.status.value == "Замороженный":
            raise AccountFrozenError("Невозможно изменить баланс, аккаунт заморожен.")
        if self._protect_balance - amount < Decimal(0.0):
            raise InsufficientFundsError("Запрошенная сумма превышает имеющуюся на балансе.")
        self._protect_balance -= amount

    def get_account_info(self): #пока избыточен, логика реализована в main
        return {
            "type": self.account_type,
            "userdata": self.user_data,
            "id": self.id_account,
            "status": self.status.value,
            "balance": self._protect_balance,
            "currency": self.currency.name
        }

    def activate(self):
        if self.status == Status.CLOSED:
            raise AccountClosedError("Счет закрыт, действия невозможны.")
        elif self.status == Status.ACTIVE:
            raise InvalidOperationError("Счет уже в статусе активен.")
        self.status = Status.ACTIVE

    def freeze(self):
        if self.status == Status.CLOSED:
            raise AccountClosedError("Счет закрыт, действия невозможны.")
        elif self.status == Status.FROZEN:
            raise AccountFrozenError("Счет уже в статусе заморожен.")
        self.status = Status.FROZEN        

    def close(self):
        if self.status == Status.ACTIVE or self.status == Status.FROZEN:
            self.status = Status.CLOSED
        else:
            raise AccountClosedError("Счет уже в статусе закрыт.")
    