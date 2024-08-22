# Finance Data Retrieval Project
This project is designed to retrieve financial data from the Alpha Vantage API. The project is structured to keep the main functionality separate from modular components for better maintainability and scalability.
Connect to Google spreadsheet where you add symbol to get data, you can download fundamental data and paste into your file

## Project Structure

```plaintext
.
├── main.py
├── finance_data/
│   ├── fundalment_data.py
│   └── ...
├── .env
└── README.md
```

### main.py
The core functionality of the project, including the main script to run the data retrieval process.
Here it runs the functions to extract and load fundamental to spreedsheet
### finance_data
This directory contains modular scripts and functions used to interact with the Alpha Vantage API, handle data processing, and any other specific tasks related to finance data retrieval.
#### fundamental_data.py
There are functions to extract fundamental data
- Balance sheet
- Income statment
- Stock daily value

### .env
Create a .env file in the root directory to add your keys:
```plaintext
ALPHAVANTAGE_API_KEY=your_api_key_here
GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = path_to_your_credentials.json
```

## Installation
Clone the Repository:
```plaintext
git clone https://github.com/felixorte23/finance_data.git
cd finance_data
```

### Install Dependencies:
Make sure you have Python installed. Install the required Python packages:
```plaintext
pip install -r requirements.txt
```

## Usage

Fetch Data: The script will fetch the latest financial data based on the configurations in the finance_data modules.