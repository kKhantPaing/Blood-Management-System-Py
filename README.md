# Blood Management System (Python)

A simple console-based Blood Management System built with Python and SQLite. It allows administrators to manage blood donors, record blood donations, track available blood units, and handle user authentication.

---

## ✅ Features

- ✅ User authentication (login / password change)
- ✅ Add and manage donors
- ✅ Record blood donations with expiration tracking
- ✅ View available blood units by blood type
- ✅ Request blood units (including handling partial fulfillment)
- ✅ Console-based menu-driven interface
- ✅ SQLite database storage (`blood_management.db`)

---

## 🧰 Prerequisites

- **Python 3.8+** (recommended)
- Optionally **pytest** for running unit tests

---

## 🚀 Getting Started

1. **Clone or download** this repository.
2. Open a terminal in the repository folder.
3. Run the application:

```bash
python main.py
```

On first run, the app will create a fresh SQLite database (`blood_management.db`) and prompt you to create the first administrator user.

---

## 🧭 Usage

When you run `python main.py`, you'll see a menu:

- **Login** — Access the full feature set
- **View Available Blood Units** — See current stock without logging in
- **Exit** — Close the program

Once logged in, you can:

- View available blood units
- Request blood units by blood type
- Add new blood donations
- Add new donors
- View donor information
- Change password, reset database, or add another user

---

## 🧪 Running Tests

This project includes a small test suite using `pytest`.

Install pytest (if not already installed):

```bash
pip install pytest
```

Run the tests:

```bash
pytest unit_test.py
```

---

## 📁 Project Structure

- `main.py` — Main CLI entrypoint and application logic
- `db_operations.py` — SQLite DB setup and data-access operations
- `models.py` — Simple data models (User / Donor / BloodDonation)
- `utils.py` — Utility helpers (password hashing, strength check)
- `unit_test.py` — Basic unit tests (password strength)
- `blood_management.db` — SQLite database file (created at runtime)

---

## 🧩 Notes / Next Improvements

- Add more robust input validation, error handling and test cases.
- Implement donor update/delete
- Emergency blood request (compatible types + urgent donor list)
- Pagination for better views
- Add more test cases