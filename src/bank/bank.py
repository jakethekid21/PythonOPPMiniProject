from __future__ import annotations

import logging
from uuid import uuid4

from src.bank.models.account import Account, CheckingAccount, SavingsAccount
from src.bank.models.credit_card import CreditCard
from src.bank.models.customer import Customer
from src.bank.models.employee import Employee
from src.bank.models.loan import Loan
from src.bank.storage.json_storage import JSONStorage
from src.bank.utils.exceptions import NotFoundError, ValidationError


class Bank:
    """
    Bank main controller

    Manages in memory objects and persists them to json storage after each operation
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        # Storage
        self.customer_store = JSONStorage("data/customers.json")
        self.account_store = JSONStorage("data/accounts.json")
        self.employee_store = JSONStorage("data/employees.json")
        self.loan_store = JSONStorage("data/loans.json")
        self.card_store = JSONStorage("data/credit_cards.json")

        # In-memory maps
        self.customers: dict[str, Customer] = {}
        self.accounts: dict[str, Account] = {}
        self.employees: dict[str, Employee] = {}
        self.loans: dict[str, Loan] = {}
        self.cards: dict[str, CreditCard] = {}

        self._load_all()

    @staticmethod
    def _new_id(prefix: str) -> str:
        """Generate a unique ID with a prefix"""
        return f"{prefix}_{uuid4().hex[:10]}"

    def _load_all(self) -> None:
        """Load all entities from JSON files into memory"""
        self.customers = {
            c["customer_id"]: Customer.from_dict(c) for c in self.customer_store.load()
        }
        self.accounts = {
            a["account_id"]: Account.from_dict(a) for a in self.account_store.load()
        }
        self.employees = {
            e["employee_id"]: Employee.from_dict(e) for e in self.employee_store.load()
        }
        self.loans = {l["loan_id"]: Loan.from_dict(l) for l in self.loan_store.load()}
        self.cards = {c["card_id"]: CreditCard.from_dict(c) for c in self.card_store.load()}

        self.logger.info(
            "Loaded %d customers, %d accounts, %d employees, %d loans, %d cards.",
            len(self.customers),
            len(self.accounts),
            len(self.employees),
            len(self.loans),
            len(self.cards),
        )

    def _save_all(self) -> None:
        """Persist all entities to JSON files."""
        self.customer_store.save([c.to_dict() for c in self.customers.values()])
        self.account_store.save([a.to_dict() for a in self.accounts.values()])
        self.employee_store.save([e.to_dict() for e in self.employees.values()])
        self.loan_store.save([l.to_dict() for l in self.loans.values()])
        self.card_store.save([c.to_dict() for c in self.cards.values()])

    # ---------------- Customers ----------------
    def create_customer(self, first_name: str, last_name: str, address: str) -> str:
        """Create new customer"""
        if not first_name or not last_name or not address:
            raise ValidationError("First name last name and address are required")

        customer_id = self._new_id("cust")
        self.customers[customer_id] = Customer(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
        )
        self._save_all()
        self.logger.info("Created customer %s (%s %s).", customer_id, first_name, last_name)
        return customer_id

    def _require_customer(self, customer_id: str) -> Customer:
        """Return customer if exists else raise"""
        customer = self.customers.get(customer_id)
        if not customer:
            raise NotFoundError(f"Customer not found: {customer_id}")
        return customer

    # ---------------- Accounts ----------------
    def open_account(self, customer_id: str, account_type: str) -> str:
        """Open checking or savings account for a customer"""
        self._require_customer(customer_id)

        acct_type = account_type.strip().lower()
        if acct_type not in {"checking", "savings"}:
            raise ValidationError("Account type must be 'checking' or 'savings'.")

        account_id = self._new_id("acct")

        if acct_type == "checking":
            account: Account = CheckingAccount(
                account_id=account_id,
                customer_id=customer_id,
                account_type="checking",
                balance=0.0,
            )
        else:
            account = SavingsAccount(
                account_id=account_id,
                customer_id=customer_id,
                account_type="savings",
                balance=0.0,
            )

        self.accounts[account_id] = account
        self._save_all()
        self.logger.info("Opened %s account %s for customer %s.", acct_type, account_id, customer_id)
        return account_id

    def _require_account(self, account_id: str) -> Account:
        """Return account if exists else raise"""
        account = self.accounts.get(account_id)
        if not account:
            raise NotFoundError(f"Account not found: {account_id}")
        return account

    def deposit(self, account_id: str, amount: float) -> None:
        """Deposit money to account"""
        account = self._require_account(account_id)
        account.deposit(amount)
        self._save_all()
        self.logger.info("Deposited %.2f to %s.", amount, account_id)

    def withdraw(self, account_id: str, amount: float) -> None:
        """Withdraw money from account."""
        account = self._require_account(account_id)
        account.withdraw(amount)
        self._save_all()
        self.logger.info("Withdrew %.2f from %s.", amount, account_id)

    def get_balance(self, account_id: str) -> float:
        """Return account balance"""
        account = self._require_account(account_id)
        return float(account.balance)

    def list_customer_accounts(self, customer_id: str) -> list[dict]:
        """List all accounts belonging customer"""
        self._require_customer(customer_id)
        return [
            {
                "account_id": a.account_id,
                "account_type": a.account_type,
                "balance": float(a.balance),
            }
            for a in self.accounts.values()
            if a.customer_id == customer_id
        ]

    # ---------------- Employees ----------------
    def create_employee(self, name: str, role: str) -> str:
        """Create new employee record"""
        if not name or not role:
            raise ValidationError("Employee name and role required")

        employee_id = self._new_id("emp")
        self.employees[employee_id] = Employee(
            employee_id=employee_id,
            name=name,
            role=role,
        )
        self._save_all()
        self.logger.info("Created employee %s (%s).", employee_id, role)
        return employee_id

    def list_employees(self) -> list[dict]:
        """List all employees"""
        return [
            {"employee_id": e.employee_id, "name": e.name, "role": e.role}
            for e in self.employees.values()
        ]

    # ---------------- Loans ----------------
    def apply_for_loan(self, customer_id: str, amount: float, term_months: int, interest_rate: float) -> str:
        """Create a loan record """
        self._require_customer(customer_id)

        if amount <= 0:
            raise ValidationError("Loan amount must be positive")
        if term_months <= 0:
            raise ValidationError("Loan term must be positive")
        if interest_rate <= 0:
            raise ValidationError("Interest rate must be positive and valid")

        loan_id = self._new_id("loan")
        self.loans[loan_id] = Loan(
            loan_id=loan_id,
            customer_id=customer_id,
            principal=float(amount),
            term_months=int(term_months),
            interest_rate=float(interest_rate),
            status="active",
        )
        self._save_all()
        self.logger.info("Created loan %s for customer %s.", loan_id, customer_id)
        return loan_id

    # ---------------- Credit Cards ----------------
    def create_credit_card(self, customer_id: str, credit_limit: float, interest_rate: float) -> str:
        """Create a credit card record """
        self._require_customer(customer_id)

        if credit_limit <= 0:
            raise ValidationError("Credit limit must be positive and valid ")
        if interest_rate <= 0:
            raise ValidationError("Interest rate must be positive and valid")

        card_id = self._new_id("card")
        self.cards[card_id] = CreditCard(
            card_id=card_id,
            customer_id=customer_id,
            credit_limit=float(credit_limit),
            interest_rate=float(interest_rate),
            balance=0.0,
            status="active",
        )
        self._save_all()
        self.logger.info("Created credit card %s for customer %s.", card_id, customer_id)
        return card_id

    def _require_card(self, card_id: str) -> CreditCard:
        """Return credit card if exists, else raise."""
        card = self.cards.get(card_id)
        if not card:
            raise NotFoundError(f"Credit card not found: {card_id}")
        return card

    def charge_card(self, card_id: str, amount: float) -> None:
        """Charge an amount to a card."""
        card = self._require_card(card_id)
        card.charge(amount)
        self._save_all()
        self.logger.info("Charged %.2f to card %s.", amount, card_id)

    def pay_card(self, card_id: str, amount: float) -> None:
        """Pay down card balance."""
        card = self._require_card(card_id)
        card.pay(amount)
        self._save_all()
        self.logger.info("Payment %.2f to card %s.", amount, card_id)