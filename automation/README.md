# Playwright Data-Driven POM Framework (Python)

A complete, runnable Playwright + pytest framework demonstrating:

- **Page Object Model (POM)**
- **Data-driven testing** from both **CSV** and **Excel**
- **Environment configuration** via **YAML** (switch environments with one env var)
- **Login Once, Reuse Login** using Playwright's `storage_state` (cookies + session persisted to disk)
- Logging, screenshot-on-failure, and a clean folder structure ready to extend

Built against **[saucedemo.com](https://www.saucedemo.com)** - a free, open, purpose-built demo site for
practicing exactly this kind of login/session/e-commerce testing. No account or API key needed.

---

## Folder Structure

```
playwright_data_driven_framework/
|
|-- config/
|     |-- environments.yaml       # base_url, browser, timeouts per environment
|
|-- data/
|     |-- login_data.csv          # data-driven test cases
|     |-- login_data.xlsx         # same data, Excel format
|
|-- pages/
|     |-- base_page.py            # shared Page Object functionality
|     |-- login_page.py           # Login Page Object
|     |-- inventory_page.py       # Post-login Products Page Object
|
|-- tests/
|     |-- test_login.py           # data-driven login tests (CSV + Excel)
|     |-- test_inventory.py       # tests that reuse a saved session
|     |-- test_session_reuse.py   # explicit proof that login happens once
|
|-- utils/
|     |-- config_reader.py        # loads environments.yaml
|     |-- data_reader.py          # reads CSV/Excel into parametrize-ready data
|     |-- auth_manager.py         # login-once / storage_state logic
|     |-- logger.py               # centralized logging
|
|-- auth/                         # saved storage_state JSON files land here (git-ignored)
|-- reports/                      # logs + failure screenshots land here (git-ignored)
|
|-- conftest.py                   # all shared pytest fixtures
|-- pytest.ini
|-- requirements.txt
|-- .gitignore
|-- README.md
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install
```

---

## Running the Tests

```bash
# Run everything against the default environment (qa)
pytest

# Run against a specific environment defined in environments.yaml
ENV=staging pytest
ENV=prod pytest

# Run just the data-driven login tests
pytest tests/test_login.py -v

# Run just the session-reuse tests
pytest tests/test_inventory.py tests/test_session_reuse.py -v

# Run in parallel (requires pytest-xdist: pip install pytest-xdist)
pytest -n 4

# Force a fresh login next run (deletes the saved session)
python -c "from utils.config_reader import get_config; from utils.auth_manager import clear_saved_session; clear_saved_session(get_config())"
```

---

## How "Login Once, Reuse Login" Works Here

1. `conftest.py` defines a **session-scoped** fixture `storage_state_path`, which calls
   `utils/auth_manager.ensure_logged_in()`.
2. The first time any test needs authentication, `ensure_logged_in()` checks whether
   `auth/qa_state.json` (or the relevant environment's file) already exists.
   - If **not**, it launches a real browser, logs in through the actual UI **once**,
     and saves the resulting cookies + local storage using
     `context.storage_state(path=...)`.
   - If it **does** exist, it's reused immediately - no UI login happens.
3. Every test that uses the `authenticated_page` fixture gets a browser context created
   with `storage_state=<saved file>` - Playwright restores the cookies and local storage
   before the first `page.goto()`, so the app treats the session as already logged in.
4. `tests/test_session_reuse.py` explicitly inspects `context.cookies()` to prove the
   `session-username` cookie exists **without that test ever calling `.login()`.**

This is the same pattern you'd use in a real framework to avoid the slowest, most repeated
step in any UI suite - logging in - while still testing against a real, working session.

---

## Switching to Your Own Application

To point this framework at a different app instead of saucedemo:

1. Update `base_url` (and add real environments) in `config/environments.yaml`.
2. Update the locators in `pages/login_page.py` and `pages/inventory_page.py` (or add new
   Page Object classes for your app's pages, following the same `BasePage` pattern).
3. Update `utils/auth_manager.py` with your app's real login field selectors and valid
   test credentials.
4. Update/replace `data/login_data.csv` and `data/login_data.xlsx` with your own test data -
   the column headers become the parametrize keys automatically.

No other file needs to change - the fixtures, data-reading, and session-reuse logic are
all generic.
