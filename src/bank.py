from bankDB import DBController

"""
class for get_or_create account and card
"""
class Bank:
    def __init__(self):
        self.__bankAPI = BankAPI()

    def get_or_create_account(self, name):
        return self.__bankAPI.get_or_create_account(name)

    def get_or_create_card(self, name, pin_number):
        result = self.__bankAPI.get_or_create_card(name, pin_number)
        if not result:
            return "No account for {}".format(name)
        return result

"""
BankAPI

for mediate DB to outer
"""
class BankAPI:
    def __init__(self):
        self.DB = DBController()

    def get_or_create_account(self,name):
        return self.DB.get_or_create_account(name)

    def get_or_create_card(self,name,pin_number):
        return self.DB.get_or_create_card(name,pin_number)

    def request_account_info(self,card_number,pin_number):
        return self.DB.request_account_info(card_number,pin_number)

    def deposit(self,account,value):
        return self.DB.deposit(account,value)

    def withdraw(self,account,value):
        return self.DB.withdraw(account,value)

    def get_balance(self,account):
        return self.DB.get_balance(account)