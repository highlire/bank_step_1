from bank_account import BankAccount, Currency, Status
from exceptions import AccountFrozenError, AccountClosedError, InsufficientFundsError, InvalidOperationError
from decimal import Decimal, InvalidOperation

accounts = [] #Хранилка аккаунтов для mvp.

def find_account():
    if not accounts:
        print("Банковские счета отсутствуют.")
        return

    id_account = input("Введите последние 4 цифры ID:\n").strip()
    if not id_account.isdigit() or len(id_account) != 4:
        raise ValueError("Введите корректный ID.")

    finds = []
    for i in accounts:
        if id_account == i.id_account[-4:]:
            finds.append(i)

    if len(finds) == 1:
        return finds[0]
    elif len(finds) == 0:
        return None
    else:
        print("Найдено несколько совпадений по указанному ID:")
        return None   

def get_info():
    account = find_account()

    if account is None:
        return
    
    print(f"Информация о счете:\n{account}")

def deposit():
    account = find_account()

    if account is None:
        print("Не найден счет с указанным ID для операции пополнения.")
        return

    amount = input("Введите сумму пополнения:\n").strip()

    amount = Decimal(amount)


    account.deposit(amount)

    print(f"Информация о счете: {account}")


def withdraw():
    account = find_account()

    if account is None:
        print("Не найден счет с указанным ID для операции снятия.")
        return

    amount = input("Введите сумму снятия:\n").strip()

    amount = Decimal(amount)

    account.withdraw(amount)

    print(f"Информация о счете:\n{account}")    

def change_status():
    account = find_account()
    
    if account is None:
        print("Не найден счет с указанным ID для смены статуса.")
        return

    print(f"Текущий статус счета:\n{account.status.value}")

    move = input("\nВыберите желаемое действие:\n1 - Активировать;\n2 - Заморозить;\n3 - Закрыть.\n").strip()

    match move:
        case "1":
            account.activate()
        case "2":
            account.freeze()
        case "3":
            account.close()
        case _:
            print("Введен неверный номер операции.")
            return

    print(f"Текущая информация об аккаунте:\n{account}")


def create_account():
    
    print("Введите ФИО:")
    user_data = input().strip()

    print("Введите начальный баланс (по умолчанию 0):")
    balance = input().strip()
    if balance == "":
        balance = Decimal("0")


    balance = Decimal(balance)

    print("Выберите желаемую валюту для счета:\n1 - RUB\n2 - USD\n3 - EUR\n4 - KZT\n5 - CNY\nПо умолчанию - RUB")
    match input().strip():
        case "1":
            currency = Currency.RUB
        case "2":
            currency = Currency.USD
        case "3":
            currency = Currency.EUR
        case "4":
            currency = Currency.KZT
        case "5":
            currency = Currency.CNY
        case "":
            currency = Currency.RUB
        case _:
            raise ValueError("Введите корректное значение от 1 до 5.")

    print("Выберите желаемый статус счета:\n1 - Активный;\n2 - Замороженный;\nПо умолчанию (активный).")
    match input().strip():
        case "1":
            status = Status.ACTIVE
        case "2":
            status = Status.FROZEN
        case "":
            status = Status.ACTIVE
        case _:
            raise ValueError("Введите корректное значение от 1 до 2.")

    account = BankAccount(user_data, balance, currency, status=status)

    accounts.append(account)

    print(f"Аккаунт успешно создан: \n{account}")




#---------------------Main------------------------
def main():
    while True:    
        # 1. Меню
        print("***Банковское приложение***")
        print("Выберите желаемое действие:")
        print("1 - Показать информацию о счете.\n2 - Внести депозит. \n3 - Вывести со счета. \n4 - Изменить статус счета. \n5 - Создание счета. \n0-Выход\n")



        try:

            i = input().strip()

            match i:
                case "1":
                    get_info()
                case "2":
                    deposit()
                case "3":
                    withdraw()
                case "4":
                    change_status()
                case "5":
                    create_account()
                case "0":
                    break
                case _:
                    print("Введите корректное значение.")
        except (AccountFrozenError, AccountClosedError,
        InsufficientFundsError, InvalidOperationError) as e:
            print(f"Ошибка операции: {e}.")
        except InvalidOperation:
            print("Передано некорректное число.")
        except (ValueError, TypeError) as e:
            print(f"Ошибка ввода: {e}.")




#Entry point
if __name__ == "__main__":
    main()
