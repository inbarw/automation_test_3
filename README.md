# Gmail to Trello Sync Automation

## Overview

This project automates the synchronization of Gmail emails with Trello cards. The automation performs the following tasks:

- Fetches emails from a Gmail inbox.
- Extracts email subjects and bodies.
- Checks if emails marked as "urgent" are properly labeled in Trello.
- Ensures emails with the same subject are merged correctly in Trello cards.

## Technologies Used

- **Python**
- **pytest** (for test execution)
- **Allure** (for reporting)
- **Google API Client** (for Gmail integration)
- **Trello API** (for Trello board management)

## Project Structure

```
project_root/
│── api_utils/
│   ├── gmail_client.py    # Handles Gmail authentication & email retrieval
│   ├── trello_client.py   # Handles Trello API interactions
│── tests/
│   ├── test_gmail_trello_sync.py
    ├── test_sending_email.py
│── config/
│   ├── config.py          # Configuration file for credentials & API keys
│── README.md              # Project documentation
```

## Installation & Setup

1. Clone the repository:

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Install Allure for test reporting:

   ```sh
   pip install allure-pytest
   ```

   If you haven't installed Allure command-line tools, install them as well:

   - **Mac/Linux:**
     ```sh
     brew install allure
     ```
   - **Windows:** Download and install Allure from [Allure Command Line](https://github.com/allure-framework/allure2/releases)

5. Create .env:
    ```sh
    TRELLO_API_KEY={API Key}
    TRELLO_TOKEN={Token}
    ```

## Running Tests

Execute the tests using:

    ```sh
    pytest tests
    ```

To run generate a test report:

    ```sh
    ./run_tests.sh
    ```

## Test Case Notes
### test_gmail_trello_sync
- Tests for urgent emails are failing because the expected synchronization does not seem to be working correctly.
- Cards that should receive an "urgent" label are not being labeled as expected.

### test_merge
- There are cases where cards contain incorrect body text.
- There are cases where cards contain incorrect body text.

### test_sending_email
- Used mock instead of actually sending an email to avoid requiring another client setup.
- However, the send_email method is implemented and working correctly.



