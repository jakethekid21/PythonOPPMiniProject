"""
Entry point for the Banking System OPP Project

Run:
    python main.py to start this app
"""

from __future__ import annotations

import logging

from src.bank.bank import Bank
from src.bank.utils.exceptions import BankingError
from src.bank.utils.logger import setup_logging


def display_menu() -> None:
    """Display the main CLI menu."""
    print("\n====== BANKING SYSTEM ======")
    print("1. Create Customer")
    print("2. Open Account (Checking/Savings)")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. View Account Balance")
    print("6. List Customer Accounts")
    print("7. Create Employee")
    print("8. List Employees")
    print("9. Apply for Loan")
    print("10. Create Credit Card")
    print("11. Charge Credit Card")
    print("12. Pay Credit Card")
    print("13. Exit")


def main() -> None:
    """Run the banking system interactive"""
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Banking system started --->")

    bank = Bank()

    while True:
        try:
            display_menu()
            choice = input("Enter choice: ").strip()

            if choice == "1":
                first = input("First name: ").strip()
                last = input("Last name: ").strip()
                address = input("Address: ").strip()
                customer_id = bank.create_customer(first, last, address)
                print(f"Customer created ID: {customer_id}")

            elif choice == "2":
                customer_id = input("Customer ID: ").strip()
                account_type = input("Account type: ").strip()
                account_id = bank.open_account(customer_id, account_type)
                print(f"Account opened. ID: {account_id}")

            elif choice == "3":
                account_id = input("Account ID: ").strip()
                amount = float(input("Amount to deposit: ").strip())
                bank.deposit(account_id, amount)
                print("Deposit successful.")

            elif choice == "4":
                account_id = input("Account ID: ").strip()
                amount = float(input("Amount to withdraw: ").strip())
                bank.withdraw(account_id, amount)
                print("Withdrawal successful.")

            elif choice == "5":
                account_id = input("Account ID: ").strip()
                balance = bank.get_balance(account_id)
                print(f"Balance: ${balance:.2f}")

            elif choice == "6":
                customer_id = input("Customer ID: ").strip()
                accounts = bank.list_customer_accounts(customer_id)
                if not accounts:
                    print("No accounts found for that customer")
                else:
                    print("\nAccounts:")
                    for a in accounts:
                        print(
                            f"- {a['account_id']} ({a['account_type']}) "
                            f"balance=${a['balance']:.2f}"
                        )

            elif choice == "7":
                name = input("Employee name: ").strip()
                role = input("Employee role: ").strip()
                employee_id = bank.create_employee(name, role)
                print(f"Employee created. ID: {employee_id}")

            elif choice == "8":
                employees = bank.list_employees()
                if not employees:
                    print("No employees found.")
                else:
                    print("\nEmployees:")
                    for e in employees:
                        print(f"- {e['employee_id']}: {e['name']} ({e['role']})")

            elif choice == "9":
                customer_id = input("Customer ID: ").strip()
                amount = float(input("Loan amount: ").strip())
                term_months = int(input("Term: ").strip())
                interest_rate = float(input("Interest rate: ").strip())
                loan_id = bank.apply_for_loan(customer_id, amount, term_months, interest_rate)
                print(f"Loan created ID: {loan_id}")

            elif choice == "10":
                customer_id = input("Customer ID: ").strip()
                limit_amount = float(input("Credit limit: ").strip())
                interest_rate = float(input("Interest rate (e.g., 0.22): ").strip())
                card_id = bank.create_credit_card(customer_id, limit_amount, interest_rate)
                print(f"Credit card created ID: {card_id}")

            elif choice == "11":
                card_id = input("Card ID: ").strip()
                amount = float(input("Amount to charge: ").strip())
                bank.charge_card(card_id, amount)
                print("charge successful")

            elif choice == "12":
                card_id = input("Card ID: ").strip()
                amount = float(input("amount to pay: ").strip())
                bank.pay_card(card_id, amount)
                print("payment successful")

            elif choice == "13":
                logger.info("Program exited")
                print("Goodbye ")
                break

            else:
                print("Invalid choice")

        except ValueError:
            # Handdles conversion errors from input
            logger.warning("Invalid numeric input from user.", exc_info=True)
            print("Please enter a valid number.")

        except BankingError as exc:
            # business errors
            logger.warning("Banking error: %s", exc, exc_info=True)
            print(f"Error: {exc}")

        except Exception as exc:
            # unexpected error
            logger.error("Unexpected error: %s", exc, exc_info=True)
            print("An unexpected error occurred, try again.")


if __name__ == "__main__":
    main()