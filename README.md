# 🧪 QA Automation Lab

A beginner-friendly **Python test automation project** that demonstrates both **API testing** and **UI (browser) testing** using industry-standard tools.

---

## 📁 Project Structure

```
QA-Automation-Lab/
├── tests/
│   ├── test_api.py          # API tests (JSONPlaceholder)
│   └── test_ui.py           # UI tests (Selenium – login page)
├── utils/
│   ├── api_client.py        # Reusable HTTP client wrapper
│   └── driver.py            # Selenium WebDriver setup
├── test_data.json            # Test inputs (credentials, endpoints)
├── run_tests.py              # One-click test runner
├── conftest.py               # Pytest path configuration
├── requirements.txt          # Python dependencies
└── README.md                 # You are here!
```

---

## 🛠️ Technology Stack

| Tool | Purpose |
|------|---------|
| **Python 3.9+** | Programming language |
| **pytest** | Test framework & runner |
| **requests** | HTTP client for API testing |
| **Selenium** | Browser automation for UI testing |
| **webdriver-manager** | Automatically downloads the correct ChromeDriver |

---

## 🚀 Getting Started

### 1. Clone or download this project

```bash
cd QA-Automation-Lab
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Make sure Google Chrome is installed

Selenium needs Chrome. `webdriver-manager` will download the matching ChromeDriver automatically.

---

## ▶️ Running the Tests

### Run all tests

```bash
pytest tests/ -v
```

### Run only API tests

```bash
pytest tests/test_api.py -v
```

### Run only UI tests

```bash
pytest tests/test_ui.py -v
```

### Use the helper script

```bash
python run_tests.py           # all tests
python run_tests.py --api     # API tests only
python run_tests.py --ui      # UI tests only
```

---

## 📝 What the Tests Cover

### API Tests (`test_api.py`)

Target: **https://jsonplaceholder.typicode.com** (free fake REST API)

| Test | What it checks |
|------|---------------|
| GET /posts | Status code 200, response is a list, correct keys |
| GET /posts/:id | Fetches a single post by ID |
| POST /posts | Creates a new post, verifies 201 status |
| PUT /posts/1 | Updates a post, checks returned data |
| DELETE /posts/1 | Deletes a post, checks 200 status |
| Parametrized GET | Data-driven test for multiple post IDs |

### UI Tests (`test_ui.py`)

Target: **https://the-internet.herokuapp.com/login** (free practice website)

| Test | What it checks |
|------|---------------|
| Page load | Title and heading are correct |
| Valid login | Success message appears, URL changes to /secure |
| Invalid login | Error message appears, stays on /login |
| Data-driven login | Multiple credential combos via `@pytest.mark.parametrize` |

---

## 🧩 Key Concepts Demonstrated

- **Test organization** – tests grouped into classes by feature
- **Reusable utilities** – `APIClient` and `get_chrome_driver` avoid code duplication
- **Data-driven testing** – `test_data.json` separates data from logic
- **Parametrized tests** – `@pytest.mark.parametrize` runs the same test with different inputs
- **Fixtures** – `@pytest.fixture` manages browser setup/teardown
- **Assertions with messages** – clear failure output for debugging
- **Logging** – every HTTP request is logged for traceability

---

## ⚙️ Configuration

Edit `test_data.json` to change URLs, credentials, or expected texts without touching the test code.

To run UI tests with a **visible browser** (useful for debugging), open `utils/driver.py` and change:

```python
driver = get_chrome_driver(headless=False)
```

---

## 📚 Learning Resources

- [pytest documentation](https://docs.pytest.org/)
- [Requests library](https://requests.readthedocs.io/)
- [Selenium with Python](https://selenium-python.readthedocs.io/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
- [The Internet – Herokuapp](https://the-internet.herokuapp.com/)

---

## 📄 License

This project is for educational purposes. Feel free to use and modify it.
