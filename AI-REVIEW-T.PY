import random
import json
import os

FILE_NAME = "bank_data.json"


# ---------------- LOAD DATA ----------------

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    return {}


# ---------------- SAVE DATA ----------------

def save_data(accounts):
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)


# ---------------- CREATE ACCOUNT ----------------

def create_account(accounts):

    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))

    if age < 18:
        print("Sorry! You must be 18+ to create an account.")
        return

    phone = input("Enter phone number: ")

    account_number = str(random.randint(100000, 999999))

    while account_number in accounts:
        account_number = str(random.randint(100000, 999999))

    accounts[account_number] = {
        "name": name,
        "age": age,
        "phone": phone,
        "balance": 0,
        "transactions": []
    }

    save_data(accounts)

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)


# ---------------- CHECK ACCOUNT ----------------

def check_account(accounts):

    print("\n========== ACCOUNT DETAILS ==========")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    account = accounts[account_number]

    print("\nName:", account["name"])
    print("Age:", account["age"])
    print("Phone:", account["phone"])
    print("Balance: ₹", account["balance"])


# ---------------- DEPOSIT ----------------

def deposit_money(accounts):

    print("\n========== DEPOSIT MONEY ==========")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        accounts[account_number]["balance"] += amount

        accounts[account_number]["transactions"].append(
            f"Deposited ₹{amount}"
        )
save_data(accounts)

        print("Money deposited successfully!")
        print("Current Balance: ₹", accounts[account_number]["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# ---------------- WITHDRAW ----------------

def withdraw_money(accounts):

    print("\n========== WITHDRAW MONEY ==========")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        balance = accounts[account_number]["balance"]

        if amount > balance:
            print("Insufficient balance!")
            return

        accounts[account_number]["balance"] -= amount

        accounts[account_number]["transactions"].append(
            f"Withdrawn ₹{amount}"
        )

        save_data(accounts)

        print("Withdrawal successful!")
        print("Remaining Balance: ₹",
              accounts[account_number]["balance"])

    except ValueError:
        print("Please enter a valid amount.")


# ---------------- TRANSACTION HISTORY ----------------

def transaction_history(accounts):

    print("\n========== TRANSACTION HISTORY ==========")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    transactions = accounts[account_number]["transactions"]

    if len(transactions) == 0:
        print("No transactions available.")
        return

    print("\nYour Transactions:")

    for number, transaction in enumerate(transactions, start=1):
        print(number, ".", transaction)


# ---------------- DELETE ACCOUNT ----------------

def delete_account(accounts):

    print("\n========== DELETE ACCOUNT ==========")

    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Account not found!")
        return

    confirmation = input(
        "Are you sure you want to delete this account? (yes/no): "
    )

    if confirmation.lower() == "yes":

        del accounts[account_number]

        save_data(accounts)

        print("Account deleted successfully!")

    else:
        print("Account deletion cancelled.")


# ---------------- MAIN MENU ----------------

def main():

    accounts = load_data()

    while True:

        print("\n")
        print("======================================")
        print("        PYTHON BANK MANAGEMENT")
        print("======================================")

        print("1. Create Account")
        print("2. Check Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transaction History")
        print("6. Delete Account")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_account(accounts)

        elif choice == "2":
            check_account(accounts)

        elif choice == "3":
            deposit_money(accounts)

        elif choice == "4":
            withdraw_money(accounts)

        elif choice == "5":
            transaction_history(accounts)

        elif choice == "6":
            delete_account(accounts)

        elif choice == "7":
            print("\nThank you for using Python Bank!")
            break

        else:
            print("Invalid choice! Please try again.")


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
