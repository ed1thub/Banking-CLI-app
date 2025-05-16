# Object-Oriented Programming Assignment: Command Line Bank Application

Objective: Design and implement a command line application for a bank that manages different types of accounts (Savings Account and Current Account), customers, and transactions. The application should utilize object-oriented programming principles and store data persistently in files.

Requirements: 
1. Account Types:
- Create a class Account that has attributes such as account number, balance, and customer associated with them.
- The Account class should have methods for deposit, withdrawal, and checking balance.
- Implement two subclasses of Account: SavingAccount and CurrentAccount.
- SavingAccount has, in addition to the data field of Account, a class variable interestRate and a function addMonthlyInterest() that will add the monthly interest for that account.
- CurrentAccount has, in addition to the data field of Account, a data field overdrawLimit. 
2. Customer:
- Implement a customer class to store customer information such as name, address, contact details, and a list of accounts associated with them.
- Ensure that a customer can have multiple accounts (both Savings and Current). 
3. Transaction:
- Implement a Transaction class to track transactions made on accounts.
- Each transaction should include details such as transaction ID, timestamp, account involved, transaction type (deposit or withdrawal), and amount. 
4. File Handling:
- Implement file handling to persistently store account and customer data.
- Use text files to store SavingAccount and CurrentAccount information, customer details (including yourself), and transaction history. Create these 4 data files and put some records in them.
- Ensure that the application can read data from files at startup and update files after any changes (e.g., new account creation, transaction recording). 
5. Command Line Interface: 
- Develop a command line interface (CLI) for interacting with the bank application.
- Include options for creating customers, creating accounts, making transactions, checking balances, and viewing transaction history.
- Ensure the CLI provides clear instructions and error messages for users. 
6. Error Handling:
- Implement robust error handling mechanisms to handle invalid inputs, insufficient balances, file read/write errors, etc.
- Provide informative error messages to guide users in case of errors. 
7. Documentation: 
- Provide documentation explaining the functionality of each class, method, and file structure. 
- Include instructions on how to run the application and interact with the command line interface.
