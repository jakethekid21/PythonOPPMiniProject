from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.bank.utils.exceptions import InsufficientFundsError, ValidationError


@dataclass
class Account:
    """Base class for bank account"""

    account_id: str
    customer_id: str
    account_type: str
    balance: float = 0.0

    def deposit(self, amount: float) -> None:
        """Deposit funds into the account"""
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive and valid")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw funds from the account"""
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insuficient funds ")
        self.balance -= amount

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "account_type": self.account_type,
            "balance": float(self.balance),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Account":
        """Deserialize from a dictionary"""
        return Account(
            account_id=data["account_id"],
            customer_id=data["customer_id"],
            account_type=data["account_type"],
            balance=float(data.get("balance", 0.0)),
        )


class CheckingAccount(Account):
    """Checking account type"""
    pass


class SavingsAccount(Account):
    """Savings account type."""
    pass