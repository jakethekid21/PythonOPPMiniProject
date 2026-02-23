#Custom exceptions for the banking system project


class BankingError(Exception):
    """Base exception for banking system errors"""


class NotFoundError(BankingError):
    """Raised when a requested entity cannot be found"""


class ValidationError(BankingError):
    """Raised when input validation fails."""


class InsufficientFundsError(BankingError):
    """Raised when an account has insufficient funds for a withdrawal/charge."""