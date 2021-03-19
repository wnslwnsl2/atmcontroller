from bank import BankAPI

class Account:
    """
    account class for atmController
    """
    def __init__(self,name,account):
        self.name = name
        self.account = account

class ATMController:
    """
    ATM Controller
    """
    def __init__(self):
        self.bankAPI = BankAPI()
        self.state = 0
        self.user = None

    """
    insert card
    """
    def insert_card(self,card_number,pin_number):
        result,data = self.bankAPI.request_account_info(card_number,pin_number)

        if result:
            self.user = Account(data[1],data[2])
            self.state = 1
            return "Hello {}!".format(self.user.name)
        else:
            return data

    def deposit(self,value):
        if self.state==0:
            return "Please insert Card."

        self.bankAPI.deposit(self.user,value)
        balance = self.__get_balance()
        self.end_process()
        return "deposit complete, {} to {}, balance:{}".format(value,self.user.name,balance)

    def withdraw(self,value):
        if self.state==0:
            return "Please insert Card."

        self.bankAPI.withdraw(self.user,value)
        balance = self.__get_balance()
        self.end_process()
        return "withdraw complete, {} from {}, balance:{}".format(value,self.user.name,balance)

    def get_balance(self):
        if self.state==0:
            return "Please insert Card."

        balance = self.bankAPI.get_balance(self.user)
        self.end_process()
        return "{}'s balance : {}".format(self.user.name,balance)

    def __get_balance(self):
        return self.bankAPI.get_balance(self.user)

    def end_process(self):
        self.state = 0
