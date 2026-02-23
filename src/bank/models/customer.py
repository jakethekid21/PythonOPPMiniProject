from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Customer:
    """Represents a bank customer"""

    customer_id: str
    first_name: str
    last_name: str
    address: str

    @property
    def full_name(self) -> str:
        """Return full name"""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Customer":
        """Deserialize from a dictionary"""
        return Customer(
            customer_id=data["customer_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            address=data["address"],
        )