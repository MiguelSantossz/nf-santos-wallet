# NF Santos Wallet — V2

A clean, modular personal finance and investment portfolio manager built in Python. This second version rebuilds the original prototype with clear separation of concerns, strict domain invariants, and test-driven financial logic.

## Overview

NF Santos Wallet allows users to manage cash balances, track financial transactions, fetch market quotes, and simulate or record asset purchases and sales with accurate average cost and profit/loss calculations.

### Key Architectural Goals
- **Domain Encapsulation:** Financial balances and positions are mutated strictly through domain models and services.
- **Separation of Concerns:** Clear boundaries between domain models (`models/`), business logic (`services/`), persistence (`repositories/`), and user interface (`cli/`).
- **Financial Precision:** Monetary values handled safely using `Decimal` and explicit validation rules.
- **Testability:** Core business rules covered by unit and integration tests from the ground up.

## Project Structure

```text
NF-SANTOS-WALLET-V2/
├── app/
│   ├── cli/            # Command-line interface and user interaction
│   ├── models/         # Core domain entities (User, Wallet, Asset, Position, Transaction)
│   ├── repositories/   # Data persistence layer
│   ├── services/       # Application services (auth, wallet operations, market data)
│   └── main.py         # Application entry point
├── tests/
│   ├── unit/           # Unit tests for domain models and business rules
│   └── integration/    # End-to-end and service integration tests
├── .env.example        # Environment variables template
├── .gitignore
├── README.md
└── requirements.txt
```

## MVP Scope (Current Phase)

- [ ] User registration and authentication
- [ ] Wallet cash operations (deposit, withdrawal, transfer) with transaction history
- [ ] Market data lookup and asset quotes
- [ ] Asset buy/sell workflows with average cost and realized/unrealized P&L tracking
- [ ] Interactive CLI

## Future Roadmap

- Persistence with SQLite / PostgreSQL via repository pattern
- REST API layer with FastAPI
- Containerization with Docker

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NF-SANTOS-WALLET-V2
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Run tests**
   ```bash
   pytest
   ```