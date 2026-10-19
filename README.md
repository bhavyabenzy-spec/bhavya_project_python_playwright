# Python Playwright Automation Practice

## About This Project

This repository contains my hands-on learning and practice in **Python, Playwright, and Pytest**. The project is organized into two assignments, progressing from Playwright fundamentals to advanced e-commerce automation.

- **Assignment 1:** Playwright fundamentals, locators, assertions, waits, browser interactions, and timeout handling.
- **Assignment 2:** Advanced e-commerce automation using Amazon India, including product discovery, dynamic product selection, auto-suggestions, browser tabs, robust locators, and test reporting.

The main objective is to develop practical UI automation skills and understand how to write reliable, reusable, and maintainable automated tests.

## Technologies Used

- **Python** – Programming language
- **Playwright** – Browser automation
- **Pytest** – Test execution and organization
- **pytest-asyncio** – Support for asynchronous tests
- **pytest-playwright** – Browser automation integration, where configured
- **pytest-html** – HTML test reports, when installed
- **VS Code** – Development environment
- **Git and GitHub** – Version control

---

# Assignment 1 – Playwright Fundamentals

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

---

# Assignment 2 – Advanced E-commerce Automation

## Project Overview

Assignment 2 focuses on automating e-commerce scenarios on **Amazon India** using Python, Playwright, and Pytest.

The assignment emphasizes reusable helper functions, reliable element selection, dynamic page interactions, browser tabs, and organized test execution.

**Practice application:** https://www.amazon.in/

## Learning Tasks

### Task 1 – Product Discovery

- Search for products using the Amazon search box.
- Identify product search results.
- Validate that relevant results are displayed.

### Task 2 – Dynamic Product Selection

- Work with dynamically displayed product results.
- Identify products from search result collections.
- Select products using their displayed information.

### Task 3 – Auto-Suggest

- Practice interacting with search auto-suggestions.
- Identify and select relevant suggestions.
- Validate search behavior.

### Task 4 – Product Page and Browser Tab Handling

- Open a product from search results.
- Handle a product page opening in a new tab.
- Use Playwright's `expect_popup()` to capture the new page.
- Verify product details.

### Tasks 5–8 – E-commerce Automation Practice

- Continue practicing the assigned e-commerce scenarios.
- Validate product and page interactions.
- Use Playwright locators and assertions to verify expected behavior.
- Practice handling dynamic elements and browser interactions.

*The exact scenario descriptions for Tasks 5–8 should be updated to match the individual task specifications.*

### Task 9 – Robust Locator Challenge

- Locate a product using its visible title.
- Find the containing product card.
- Perform actions within the selected card.
- Avoid relying on fixed product positions.
- Validate that the correct product details page opens.
- Handle a new browser tab and verify the product title.

### Task 10 – Mini Project and Test Report

Organize the e-commerce automation scenarios into a small, maintainable test suite.

- Create separate pytest test functions.
- Use descriptive test names.
- Create reusable helper functions for product search and product-card selection.
- Validate search results, product cards, product links, and product details.
- Run tests and record passed, failed, and skipped counts.
- Capture screenshots when tests fail.
- Document the root cause and suggested fix for each failure.
- Prepare a test execution report.

## Assignment 2 – Test Organization

The mini project uses reusable helper functions to reduce duplication and improve maintainability.

Examples of test scenarios include:

- `test_product_search`
- `test_correct_product_card`
- `test_product_link`
- `test_product_details`

The test suite uses the existing `async_page` fixture from `conftest.py` to manage browser setup and execution.

## Test Reports and Screenshots

The test report can include:

- Total tests collected
- Passed tests
- Failed tests
- Skipped tests
- Failure details
- Root-cause analysis
- Suggested fixes
- Screenshots of failed tests

Suggested artifact locations:

- **HTML report:** `test-results/report.html`
- **Failure screenshots:** `test-results/screenshots/`

These artifacts are generated when the relevant reporting and screenshot setup is configured and executed.

---

# Project Structure

```text
bhavya_project_python_playwright/
│
├── tests/
│   ├── assignment1-06OCTto12OCT-Bhavya/
│   │   ├── test_task1.py
│   │   ├── test_task2.py
│   │   └── ...
│   │
│   └── assignment2-10OCTto18OCT-Bhavya/
│       ├── test_task1_product_discovery.py
│       ├── test_task2_*.py
│       ├── test_task3_*.py
│       ├── ...
│       ├── test_task9_robust_locators.py
│       └── test_task10_mini_project.py
│
├── test-results/
│   ├── report.html
│   └── screenshots/
│
├── conftest.py
├── config.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The file names shown with `*` are illustrative. Keep the actual names of your existing test files. The `test-results` folder is created when test artifacts are generated.*

---

# Installation and Setup

## 1. Clone the repository

```bash
git clone https://github.com/bhavyabenzy-spec/bhavya_project_python_playwright.git
cd bhavya_project_python_playwright
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install the required packages

```bash
python -m pip install -r requirements.txt
```

If the requirements file does not include the packages needed for the project, install them with:

```bash
python -m pip install pytest pytest-asyncio playwright
```

For HTML reports:

```bash
python -m pip install pytest-html
```

## 5. Install Playwright browsers

```bash
python -m playwright install chromium firefox webkit
```

This installs the Chromium, Firefox, and WebKit browser engines supported by Playwright.

---

# Running Tests

## Run all discovered tests

```bash
python -m pytest -v
```

## Run tests with terminal output

```bash
python -m pytest -v -s
```

## Run a specific Assignment 1 task

```bash
python -m pytest -v -s tests/assignment1-06OCTto12OCT-Bhavya/test_task13.py
```

Replace the file name with the task you want to execute.

## Run the Assignment 2 mini project

```bash
python -m pytest tests/assignment2-10OCTto18OCT-Bhavya/test_task10_mini_project.py -v -s --tb=short
```

## Check which tests Pytest discovers

```bash
python -m pytest tests/assignment2-10OCTto18OCT-Bhavya/test_task10_mini_project.py --collect-only -v
```

## Run all Assignment 2 tests

```bash
python -m pytest tests/assignment2-10OCTto18OCT-Bhavya -v --tb=short
```

## Generate an HTML test report

Create the output folder if necessary:

```powershell
New-Item -ItemType Directory -Force test-results
```

Then run:

```bash
python -m pytest tests/assignment2-10OCTto18OCT-Bhavya -v --html=test-results/report.html --self-contained-html
```

Open `test-results/report.html` in a browser to review the test execution summary and failure details.

---

# Browser Execution Matrix

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
- **SKIP** – Test was skipped during execution.
- **Not Run** – Test has not yet been executed in that browser.

*The matrix above is the existing Assignment 1 tracking table. Update its statuses only after executing the corresponding scenarios in each browser.*

## Running Tests in Different Browsers

If your project is configured to use the `pytest-playwright` browser options, you can run:

```bash
python -m pytest --browser chromium -v
```

```bash
python -m pytest --browser firefox -v
```

```bash
python -m pytest --browser webkit -v
```

The available browser options depend on your installed plugin and project configuration.

---

# Assignment 2 – Test Execution Summary

Update this section after running the complete Assignment 2 test suite.

| Metric | Result |
|---|---:|
| Total tests collected | Pending execution |
| Passed | Pending execution |
| Failed | Pending execution |
| Skipped | Pending execution |

## Failure Analysis

For each failed test, record:

- **Test name**
- **Expected result**
- **Actual result**
- **Root cause**
- **Suggested fix**
- **Screenshot path**

If all tests pass, record that no failures were observed in the completed test run.

---

# Learning Outcomes

Through these assignments, I have gained practical experience with:

- Python-based browser automation
- Asynchronous testing using Playwright and pytest-asyncio
- Locator strategies and dynamic web elements
- Assertions and test validation
- Browser navigation and popup handling
- Waits and timeout management
- Reusable helper functions
- Organizing tests into separate functions
- Debugging failed test cases
- Test execution reporting and failure analysis

---

# Conclusion

This project documents my progress from Playwright fundamentals to more advanced e-commerce automation. It provides practical experience in writing, executing, debugging, and organizing automated UI tests using Python, Playwright, and Pytest.

The project will continue to evolve as I complete additional tasks and improve test reliability, maintainability, and reporting.
