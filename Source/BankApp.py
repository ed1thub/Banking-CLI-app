import os
import json
import datetime

DATA_DIR = 'data'

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Utility functions for file read/write with JSON format
def read_json_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_json_file(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

# Customer Class
class Customer:
    def __init__(self, customer_id, name, address, contact):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.contact = contact
        self.accounts = []  # list of account numbers

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "contact": self.contact,
            "accounts": self.accounts
        }

    @classmethod
    def from_dict(cls, data):
        cust = cls(data['customer_id'], data['name'], data['address'], data['contact'])
        cust.accounts = data.get('accounts', [])
        return cust

# Base Account class
class Account:
    def __init__(self, account_number, customer_id, balance=0.0):
        self.account_number = account_number
        self.customer_id = customer_id
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "customer_id": self.customer_id,
            "balance": self.balance,
            "type": "Account"
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['account_number'], data['customer_id'], data['balance'])

# SavingAccount subclass
class SavingAccount(Account):
    interest_rate = 0.02  # 2% monthly interest as example

    def add_monthly_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['type'] = "SavingAccount"
        base_dict['interest_rate'] = self.interest_rate
        return base_dict

    @classmethod
    def from_dict(cls, data):
        account = cls(data['account_number'], data['customer_id'], data['balance'])
        cls.interest_rate = data.get('interest_rate', cls.interest_rate)
        return account

# CurrentAccount subclass
class CurrentAccount(Account):
    def __init__(self, account_number, customer_id, balance=0.0, overdraw_limit=0.0):
        super().__init__(account_number, customer_id, balance)
        self.overdraw_limit = overdraw_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraw_limit:
            raise ValueError("Withdrawal exceeds overdraw limit.")
        self.balance -= amount

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['type'] = "CurrentAccount"
        base_dict['overdraw_limit'] = self.overdraw_limit
        return base_dict

    @classmethod
    def from_dict(cls, data):
        return cls(data['account_number'], data['customer_id'], data['balance'], data.get('overdraw_limit', 0.0))

# Transaction class
class Transaction:
    def __init__(self, transaction_id, account_number, transaction_type, amount):
        self.transaction_id = transaction_id
        self.timestamp = datetime.datetime.now().isoformat()
        self.account_number = account_number
        self.transaction_type = transaction_type  # 'deposit' or 'withdrawal'
        self.amount = amount

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "account_number": self.account_number,
            "transaction_type": self.transaction_type,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        trans = cls(data['transaction_id'], data['account_number'], data['transaction_type'], data['amount'])
        trans.timestamp = data['timestamp']
        return trans

# Bank system managing customers, accounts and transactions
class BankSystem:
    def __init__(self):
        self.customers_file = 'customers.json'
        self.accounts_file = 'accounts.json'
        self.transactions_file = 'transactions.json'

        self.customers = self.load_customers()
        self.accounts = self.load_accounts()
        self.transactions = self.load_transactions()

    def load_customers(self):
        data = read_json_file(self.customers_file)
        return {c['customer_id']: Customer.from_dict(c) for c in data}

    def save_customers(self):
        data = [cust.to_dict() for cust in self.customers.values()]
        write_json_file(self.customers_file, data)

    def load_accounts(self):
        data = read_json_file(self.accounts_file)
        accounts = {}
        for acc_data in data:
            if acc_data['type'] == "SavingAccount":
                accounts[acc_data['account_number']] = SavingAccount.from_dict(acc_data)
            elif acc_data['type'] == "CurrentAccount":
                accounts[acc_data['account_number']] = CurrentAccount.from_dict(acc_data)
            else:
                accounts[acc_data['account_number']] = Account.from_dict(acc_data)
        return accounts

    def save_accounts(self):
        data = [acc.to_dict() for acc in self.accounts.values()]
        write_json_file(self.accounts_file, data)

    def load_transactions(self):
        data = read_json_file(self.transactions_file)
        return [Transaction.from_dict(t) for t in data]

    def save_transactions(self):
        data = [t.to_dict() for t in self.transactions]
        write_json_file(self.transactions_file, data)

    def create_customer(self, name, address, contact):
        customer_id = f"C{len(self.customers)+1:04d}"
        customer = Customer(customer_id, name, address, contact)
        self.customers[customer_id] = customer
        self.save_customers()
        return customer

    def create_account(self, customer_id, account_type, initial_deposit=0, overdraw_limit=0):
        if customer_id not in self.customers:
            raise ValueError("Customer does not exist.")
        account_number = f"A{len(self.accounts)+1:06d}"

        if account_type == 'saving':
            account = SavingAccount(account_number, customer_id, initial_deposit)
        elif account_type == 'current':
            account = CurrentAccount(account_number, customer_id, initial_deposit, overdraw_limit)
        else:
            raise ValueError("Invalid account type.")

        self.accounts[account_number] = account
        self.customers[customer_id].accounts.append(account_number)

        self.save_accounts()
        self.save_customers()

        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    def make_transaction(self, account_number, transaction_type, amount):
        account = self.get_account(account_number)
        if not account:
            raise ValueError("Account not found.")

        if transaction_type == 'deposit':
            account.deposit(amount)
        elif transaction_type == 'withdrawal':
            account.withdraw(amount)
        else:
            raise ValueError("Invalid transaction type.")

        # Log transaction
        transaction_id = f"T{len(self.transactions)+1:08d}"
        transaction = Transaction(transaction_id, account_number, transaction_type, amount)
        self.transactions.append(transaction)

        # Save changes
        self.save_accounts()
        self.save_transactions()

        return transaction

    def check_balance(self, account_number):
        account = self.get_account(account_number)
        if not account:
            raise ValueError("Account not found.")
        return account.get_balance()

    def transaction_history(self, account_number):
        return [t for t in self.transactions if t.account_number == account_number]

    def add_interest_to_savings(self):
        for account in self.accounts.values():
            if isinstance(account, SavingAccount):
                account.add_monthly_interest()
        self.save_accounts()

    def create_accounts(self):
        print("\n--- Create Account ---")
        name = input("Customer Name: ").strip()
        address = input("Customer Address: ").strip()
        contact = input("Customer Contact: ").strip()

        customer = self.create_customer(name, address, contact)
        print(f"Customer created with ID: {customer.customer_id}")

        while True:
            print("\nCreate an account for this customer:")
            account_type = input("Account Type (saving/current): ").lower().strip()
            if account_type not in ('saving', 'current'):
                print("Invalid account type. Try again.")
                continue

            try:
                initial_deposit = float(input("Initial Deposit Amount: "))
                overdraw_limit = 0
                if account_type == 'current':
                    overdraw_limit = float(input("Overdraw Limit: "))
                account = self.create_account(customer.customer_id, account_type, initial_deposit, overdraw_limit)
                print(f"Account created with Account Number: {account.account_number}")
            except ValueError as ve:
                print(f"Error: {ve}")

            another = input("Create another account for this customer? (y/n): ").lower()
            if another != 'y':
                break

        return customer

# CLI Interface
def main():
    bank = BankSystem()

    while True:
        print("\n=== Welcome to the Bank CLI Application ===")
        print("1. Create Account")
        print("2. Make Deposit")
        print("3. Make Withdrawal")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. Add Monthly Interest to Savings Accounts")
        print("7. Exit")

        choice = input("Select an option: ").strip()

        try:
            if choice == '1':
                bank.create_accounts()

            elif choice == '2':
                account_number = input("Account Number: ").strip()
                amount = float(input("Deposit Amount: "))
                transaction = bank.make_transaction(account_number, 'deposit', amount)
                print(f"Deposit successful. Transaction ID: {transaction.transaction_id}")

            elif choice == '3':
                account_number = input("Account Number: ").strip()
                amount = float(input("Withdrawal Amount: "))
                transaction = bank.make_transaction(account_number, 'withdrawal', amount)
                print(f"Withdrawal successful. Transaction ID: {transaction.transaction_id}")

            elif choice == '4':
                account_number = input("Account Number: ").strip()
                balance = bank.check_balance(account_number)
                print(f"Current balance: ${balance:.2f}")

            elif choice == '5':
                account_number = input("Account Number: ").strip()
                transactions = bank.transaction_history(account_number)
                if not transactions:
                    print("No transactions found.")
                else:
                    print("Transaction History:")
                    for t in transactions:
                        print(f"{t.timestamp} | {t.transaction_type.title()} | Amount: ${t.amount:.2f} | ID: {t.transaction_id}")

            elif choice == '6':
                bank.add_interest_to_savings()
                print("Monthly interest added to all saving accounts.")

            elif choice == '7':
                print("Thank you for using the bank CLI. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        except ValueError as ve:
            print(f"Error: {ve}")

if __name__ == "__main__":
    main()
