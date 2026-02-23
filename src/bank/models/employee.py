from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Employee:
    """Represents a bank employee"""

    employee_id: str
    name: str
    role: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict"""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Employee":
        """Deserialize from dict"""
        return Employee(
            employee_id=data["employee_id"],
            name=data["name"],
            role=data["role"],
        )