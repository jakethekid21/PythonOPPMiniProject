from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from src.bank.utils.exceptions import InsufficientFundsError, ValidationError


@dataclass
class CreditCard:
    """Represents a credit card service"""

    card_id: str
    customer_id: str
    credit_limit: float
    interest_rate: float
    balance: float = 0.0
    status: str = "active"

    def charge(self, amount: float) -> None:
        """Charge an amount to the card increases balance"""
        if amount <= 0:
            raise ValidationError("Charge amount must be positive")
        if self.balance + amount > self.credit_limit:
            raise InsufficientFundsError("Charge would exceed limit")
        self.balance += amount

    def pay(self, amount: float) -> None:
        """Pay down the card balance"""
        if amount <= 0:
            raise ValidationError("Payment amount must be positive and valid")
        self.balance = max(0.0, self.balance - amount)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "CreditCard":
        """Deserialize from dict"""
        return CreditCard(
            card_id=data["card_id"],
            customer_id=data["customer_id"],
            credit_limit=float(data["credit_limit"]),
            interest_rate=float(data["interest_rate"]),
            balance=float(data.get("balance", 0.0)),
            status=data.get("status", "active"),
        )