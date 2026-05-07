# Blood Management System (Python)

A simple console-based Blood Management System built with Python and SQLite. It helps administrators manage blood donors, record blood donations, track available inventory, and perform blood requests with compatibility handling.

---

## ✅ Features

- ✅ User authentication with login and password change
- ✅ Add and manage donor records
- ✅ Record blood donations with expiration tracking
- ✅ View available blood units by blood type
- ✅ Request blood units by type with partial fulfillment fallback
- ✅ Emergency-compatible blood request lookup
- ✅ Add new users and reset database from settings
- ✅ Console-based menu-driven interface
- ✅ SQLite storage using `blood_management.db`

---

## 🧰 Prerequisites

- **Python 3.8+**
- Optional: **pytest** for running unit tests

---

## 🚀 Getting Started

1. Clone or download this repository.
2. Open a terminal in the repository folder.
3. Run the application:

```bash
python main.py
```

On first run, the app creates the SQLite database file `blood_management.db` and prompts you to create the first administrator user.

---

## 🧭 Usage

When you run `python main.py`, the default menu offers:

- **Login** — Authenticate and access the admin menu
- **View Available Blood Units** — See current stock without logging in
- **Exit** — Quit the application

### Logged-in menu options

- View available blood units by blood type
- Request blood units by blood type
- Add a new blood donation record
- Add a new donor record
- View and update donor information
- Perform an emergency blood request lookup for compatible types
- Change password
- Add another user
- Reset the database
- Logout / Exit

### Supported blood types

- A+, A-, B+, B-, AB+, AB-, O+, O-

Blood donations are tracked with expiration dates, and expired units are automatically marked as expired on startup.

---

## 🧪 Running Tests

This repository includes a small test suite.

Install `pytest` if needed:

```bash
pip install pytest
```

Run the tests:

```bash
pytest unit_test.py
```

---

## 📁 Project Structure

- `main.py` — Main command-line interface and user interaction flows
- `db_operations.py` — SQLite database setup, queries, inserts, and updates
- `models.py` — Simple `User`, `Donor`, and `BloodDonation` data models
- `utils.py` — Utility functions such as password hashing
- `unit_test.py` — Test suite for password validation and authentication logic
- `blood_management.db` — SQLite database file created at runtime

---

## 🧩 Notes / Next Improvements

- Add more robust input validation and error handling
- Improve donor update/delete workflows
- Complete emergency donor urgency matching
- Expand unit tests and test coverage
- Add a richer user interface and pagination for long lists
