from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Loan:
    """Represents a loan service"""

    loan_id: str
    customer_id: str
    principal: float
    term_months: int
    interest_rate: float
    status: str = "active"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Loan":
        """Deserialize from dict"""
        return Loan(
            loan_id=data["loan_id"],
            customer_id=data["customer_id"],
            principal=float(data["principal"]),
            term_months=int(data["term_months"]),
            interest_rate=float(data["interest_rate"]),
            status=data.get("status", "active"),
        )