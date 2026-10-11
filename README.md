# Python Playwright Automation Practice

## About This Project

This repository contains my hands-on learning and practice in **Python, Playwright, and Pytest**. Through 17 tasks, I have learned the fundamentals of browser automation and progressively explored locators, assertions, waits, dynamic elements, and timeout handling.

The main objective of this project is to develop practical UI automation skills and understand how to write reliable, maintainable automated tests.

## Technologies Used

- **Python** – Programming language
- **Playwright** – Browser automation
- **Pytest** – Test execution and organization
- **pytest-asyncio** – Support for asynchronous tests
- **VS Code** – Development environment
- **Git and GitHub** – Version control

## Learning Tasks

### Tasks 1–11: Playwright Fundamentals

Practiced the fundamentals of browser automation and interacting with web pages.

Topics include:

- Browser and page initialization
- Opening web pages and navigating between pages
- Locating web elements
- Interacting with page elements
- Filling input fields and handling common UI controls
- Working with dropdowns
- Extracting text and element attributes
- Practicing different locator strategies

### Task 12 – Assertions

Learned how to validate page behavior and test results using:

- Playwright's `expect()` assertions
- Pytest's `assert` statement
- Validating page titles and URLs
- Checking element visibility and text
- Verifying expected and actual results

### Task 13 – Soft Assertions

Practiced collecting multiple validation failures before failing a test.

- Store assertion failures in a list
- Continue checking additional conditions after a failure
- Report collected failures at the end using `pytest.fail()`

### Task 14 – Multiple Locators

Practiced working with collections of matching elements.

- Count matching elements
- Use `.first`, `.last`, and `.nth()`
- Iterate through multiple elements
- Validate the number of matching elements
- Extract text from multiple elements

### Task 15 – Built-in Waits

Learned to wait for browser and page events instead of relying on fixed delays.

- Locator-based waits
- Page load states
- Navigation waits
- Waiting for elements before interacting with them

### Task 16 – Dynamic Waits

Practiced waiting for dynamically updated UI elements using a SauceDemo shopping-cart scenario.

- Interact with dynamic page elements
- Wait for the shopping-cart badge to update
- Validate the updated cart count
- Understand the importance of dynamic waits in modern web applications

### Task 17 – Timeouts and Custom Wait Conditions

Learned to handle slow responses and elements that do not appear as expected.

- Configure default action and navigation timeouts
- Handle Playwright timeout errors
- Test missing-element scenarios
- Implement custom wait conditions
- Improve test reliability by waiting for specific conditions

## Practice Application

**SauceDemo:** https://www.saucedemo.com/

SauceDemo is used for practicing browser automation scenarios, including login, product listing, locator strategies, and shopping-cart interactions.

Public demo credentials:

- **Username:** `standard_user`
- **Password:** `secret_sauce`

These credentials are for the public practice application only.

## Project Structure

```text
bhavya_project_python_playwright/
│
├── tests/
│   └── assignment1/
│       ├── test_task13.py
│       ├── test_task14.py
│       └── ... 
│
├── .venv/
├── README.md
├── requirements.txt
└── .gitignore
```


## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/bhavyabenzy-spec/bhavya_project_python_playwright.git
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the required packages

```bash
python -m pip install pytest pytest-asyncio playwright
```

### 5. Install Playwright browsers

```bash
python -m playwright install chromium firefox webkit
```

This installs the Chromium, Firefox, and WebKit browser engines supported by Playwright.

## Running Tests

### Run all discovered tests

```bash
python -m pytest -v
```

### Run tests with terminal output

```bash
python -m pytest -v -s
```

### Run a specific task

```bash
python -m pytest -v -s tests/assignment1/test_task13.py
```

Replace the file name with the test file you want to execute.

## Browser Execution Matrix

The following matrix tracks test execution across Chromium, Firefox, and WebKit.

| Test | Chromium | Firefox | WebKit |
|---|---|---|---|
| Login | Pass | Pass | Pass |
| Search | Pass | Pass | Pass |
| Navigation | Pass | Pass | Pass |
| Form Validation | Pass | Pass | Pass |

### Execution Status

- **PASS** – Test executed successfully.
- **FAIL** – Test executed but did not meet the expected result.
- **Not Run** – Test has not yet been executed in that browser.

*The matrix is a tracking table. Update each status only after executing the corresponding test in that browser. The four scenarios may require separate test cases if they are not already implemented.*

### Running Tests in Different Browsers

Run tests in Chromium:

```bash
python -m pytest --browser chromium -v
```

Run tests in Firefox:

```bash
python -m pytest --browser firefox -v
```

Run tests in WebKit:

```bash
python -m pytest --browser webkit -v
```

Run tests in all three browsers:

```bash
python -m pytest --browser chromium --browser firefox --browser webkit -v
```

These browser options require the `pytest-playwright` plugin. Install it if you want to use the plugin's browser options and fixtures:

```bash
python -m pip install pytest-playwright
```


