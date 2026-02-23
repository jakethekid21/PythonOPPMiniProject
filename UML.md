# UML Class Diagram for Banking System spring board oop project

This UML class diagram documents the banking system design including classes key fields
key methods and relationships, associations and inheritance

```mermaid
classDiagram
    class Bank {
      +create_customer(first_name, last_name, address) str
      +open_account(customer_id, account_type) str
      +deposit(account_id, amount) void
      +withdraw(account_id, amount) void
      +get_balance(account_id) float
      +list_customer_accounts(customer_id) list
      +create_employee(name, role) str
      +list_employees() list
      +apply_for_loan(customer_id, amount, term_months, interest_rate) str
      +create_credit_card(customer_id, credit_limit, interest_rate) str
      +charge_card(card_id, amount) void
      +pay_card(card_id, amount) void
    }

    class Customer {
      +customer_id: str
      +first_name: str
      +last_name: str
      +address: str
      +full_name: str
    }

    class Account {
      +account_id: str
      +customer_id: str
      +account_type: str
      +balance: float
      +deposit(amount) void
      +withdraw(amount) void
    }

    class CheckingAccount
    class SavingsAccount

    class Employee {
      +employee_id: str
      +name: str
      +role: str
    }

    class Loan {
      +loan_id: str
      +customer_id: str
      +principal: float
      +term_months: int
      +interest_rate: float
      +status: str
    }

    class CreditCard {
      +card_id: str
      +customer_id: str
      +credit_limit: float
      +interest_rate: float
      +balance: float
      +status: str
      +charge(amount) void
      +pay(amount) void
    }

    %% Relationships
    Bank --> Customer : manages
    Bank --> Account : manages
    Bank --> Employee : manages
    Bank --> Loan : manages
    Bank --> CreditCard : manages

    %% Inheritance
    Account <|-- CheckingAccount
    Account <|-- SavingsAccount
```
