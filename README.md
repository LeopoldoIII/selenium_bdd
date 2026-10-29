# Selenium & API Behave BDD Framework

An enterprise test automation framework for web applications (UI) and REST services (API), built with **Python**, **Behave**, **Selenium 4**, **Requests**, and **Allure Reports**.

---

## 🚀 Key Features

- **BDD with Gherkin & Behave**: Clear, human-readable specifications (`features/`).
- **Page Object Model (POM)**: Robust object-oriented architecture with explicit waits (`WebDriverWait`).
- **Multi-Browser Support**: Chrome, Firefox, Edge, and Safari with automatic driver management via Selenium Manager.
- **Hybrid Testing (UI + API)**: Tag separation (`@ui`, `@api`) with conditional WebDriver lifecycle to optimize execution speed and resource usage.
- **Configuration & Secrets via DotEnv**: Environment variables loaded from `.env` with a version-controlled `.env.example` template.
- **Interactive Allure Reports**: Metrics, detailed steps, failure screenshot attachments, and execution logs.
- **Flaky Test Re-run (`rerun`)**: Easily re-execute only failed tests (`make rerun`).
- **Antigravity AI Integration**: QA architectural guidelines in `AGENTS.md` and custom workspace skill `.agents/skills/bdd-runner/` for AI pair programming.

---

## 🛠️ Prerequisites

- Python 3.10+
- Google Chrome (or any other supported browser)
- Allure CLI (on macOS: `brew install allure`)

---

## 📦 Installation

1. Clone the repository and navigate to the project root:
   ```bash
   git clone <repo-url>
   cd selenium_bdd
   ```

2. Set up the virtual environment and install dependencies using `make`:
   ```bash
   make install
   ```
   *(Or manually: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt && cp .env.example .env`)*

---

## ⚙️ Configuration (`.env`)

Configure your `.env` file according to your test environment needs:

```env
BROWSER=chrome
HEADLESS=true
BASE_URL=https://www.saucedemo.com
API_BASE_URL=https://reqres.in
LOG_LEVEL=INFO
```

You can also override any configuration directly from the command line with `-D`:
```bash
./venv/bin/behave -D browser=firefox -D headless=false
```

---

## 🧪 Test Execution

### Via Makefile:

```bash
# Run all tests (UI + API)
make test-all

# Run only UI tests
make test-ui

# Run only API tests
make test-api

# Re-run only failed tests
make rerun

# Generate static Allure HTML report
make report

# Open interactive Allure report in browser
make serve-report

# Clean temporary files, logs, and reports
make clean
```

### Via Behave CLI:

#### 1. Run a specific `.feature` file:

```bash
# Run a specific feature file (UI Login)
./venv/bin/behave features/login.feature

# Run an API feature file
./venv/bin/behave features/api_users.feature

# Run a feature generating Allure results
./venv/bin/behave features/login.feature -f allure -o allure-results

# Run a feature in headed mode (visible browser window)
./venv/bin/behave features/login.feature -D headless=false
```

#### 2. Run a specific scenario within a `.feature`:

```bash
# By line number (e.g. line 8 in login.feature)
./venv/bin/behave features/login.feature:8

# By scenario name (-n / --name)
./venv/bin/behave features/login.feature -n "Successful login with valid credentials"
```

#### 3. Run full suite or filter by tags:

```bash
# Run all features with Allure reporting and rerun tracking
./venv/bin/behave -f allure -o allure-results -f rerun -o rerun.txt

# Filter by tags across the entire suite or on a specific feature
./venv/bin/behave --tags=@smoke
./venv/bin/behave --tags=@regression
./venv/bin/behave features/login.feature --tags=@smoke
```

---

## 📊 Allure Reporting

To view the interactive dashboard after test execution:

```bash
allure serve allure-results
```

Or to generate a self-contained static report:

```bash
allure generate allure-results -o allure-report --clean
open allure-report/index.html
```

---

## 📁 Project Structure

```text
selenium_bdd/
├── .agents/
│   └── skills/
│       └── bdd-runner/         # Antigravity skill for execution and diagnostics
├── .github/
│   └── workflows/              # CI/CD Pipeline (GitHub Actions)
├── config/
│   └── config.json             # Default base configuration
├── data/
│   └── test_data.json          # Test fixtures and credentials
├── features/
│   ├── environment.py          # Lifecycle hooks (UI vs API, Allure, Logging)
│   ├── login.feature           # UI scenarios (SauceDemo)
│   ├── api_users.feature       # API scenarios (ReqRes)
│   └── steps/
│       ├── login_steps.py      # Login step definitions
│       └── api_steps.py        # Reusable API step definitions
├── pages/
│   ├── base_page.py            # Base Page Object with WebDriverWait helpers
│   ├── login_page.py           # Login Page Object
│   └── inventory_page.py       # Inventory Page Object
├── utils/
│   ├── api_client.py           # HTTP client with logging and Allure attachments
│   ├── config_reader.py        # Config resolver (CLI > .env > JSON)
│   ├── driver_factory.py       # Multi-browser Driver Factory
│   ├── logger.py               # Centralized rotating logger
│   └── screenshot_manager.py   # Screenshot capture manager
├── .env.example                # Environment variables template
├── AGENTS.md                   # AI agent architectural guidelines
├── behave.ini                  # Behave configuration and formatters
├── Makefile                    # Task runner
└── requirements.txt            # Project dependencies
```
