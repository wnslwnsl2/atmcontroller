import sqlite3
import datetime

class DBController:
    def __init__(self):
        self.dbname = "bank.db"

        """
        initialize cards and accounts database if doesn't exist
        """
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        cards_create_sql = """CREATE TABLE IF NOT EXISTS accounts(
                    id INTEGER PRIMARY KEY,
                    customer_name VARCHAR(30) NOT NULL unique,
                    account_number VARCHAR(12) NOT NULL unique,
                    balance INTEGER default 0
                )"""
        cur.execute(cards_create_sql)

        cards_create_sql="""CREATE TABLE IF NOT EXISTS cards(
            id INTEGER PRIMARY KEY,
            card_number VARCHAR(12) NOT NULL unique,
            card_pin VARCHAR(4) NOT NULL,
            account_id INT unique,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )"""
        cur.execute(cards_create_sql)

        conn.commit()
        conn.close()


    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbname)
        except Exception as e:
            print(e)
        return conn


    """
    get_or_create_account
    
    create if account doesn't exist
    """
    def get_or_create_account(self,name):
        account_number = self.__create_number()
        conn = self.create_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO accounts(customer_name,account_number) VALUES(?,?)",(name,account_number))
            conn.commit()
            ret = account_number
        except Exception as e:
            cur.execute("SELECT account_number FROM accounts WHERE customer_name==?",(name,))
            rows = cur.fetchall()
            ret = rows[0][0]
        finally:
            conn.close()
            return ret

    """
    get_or_create_card
    """
    def get_or_create_card(self,name,pin_number):
        card_number = self.__create_number()
        conn = self.create_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM accounts WHERE customer_name==?",(name,))
        rows = cur.fetchall()

        if len(rows)==0:
            return False

        account_id = rows[0][0]

        try:
            cur.execute("INSERT INTO cards(card_number,card_pin,account_id) VALUES(?,?,?)",(card_number,pin_number,account_id))
            conn.commit()
            ret = card_number
        except Exception as e:
            cur.execute("UPDATE cards SET card_pin=? WHERE account_id==?",(pin_number,account_id))
            cur.execute("SELECT card_number FROM cards WHERE account_id==?",(account_id,))
            rows = cur.fetchall()
            ret = rows[0][0]
        finally:
            conn.close()
            return ret

    """
    create card and account number for 12 digit(HHMMSSFFFFFF)
    """
    def __create_number(self):
        return datetime.datetime.now().strftime("%H%M%S%f")

    """
    receive card_number and pin
    return account_info
    """
    def request_account_info(self,card_number,card_pin):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM cards WHERE card_number==?",(card_number,))
        rows = cur.fetchall()

        if len(rows)==0:
            conn.close()
            return False,"Card doesn't registered in database."

        card_row = rows[0]
        correct_card_pin = card_row[2]

        if correct_card_pin!=card_pin:
            conn.close()
            return False,"Wrong pin number."

        account_id = card_row[3]
        cur.execute("SELECT * FROM accounts WHERE id==?",(account_id,))
        account_data = cur.fetchone()
        conn.close()
        return True,account_data

    def deposit(self,account,value):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE account_number=?",(value,account.account,))
        conn.commit()
        conn.close()
        return True

    def withdraw(self,account,value):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accounts WHERE account_number==?",(account.account,))
        rows = cur.fetchall()
        if rows[0][0] >= value:
            cur.execute("UPDATE accounts SET balance = balance - ? WHERE account_number=?",(value,account.account,))
            conn.commit()
            ret = True
        else:
            ret = False
        conn.close()
        return ret

    def get_balance(self,account):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accounts WHERE account_number==?", (account.account,))
        rows = cur.fetchall()
        conn.close()

        return rows[0][0]