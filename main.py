# %%
import pandas as pd
import pygsheets
import os
from dotenv import load_dotenv
from finance_data.fundamental_data import balance_sheet, BalanceSheetError
from finance_data.fundamental_data import income_statement, IncomeStatementError
from finance_data.fundamental_data import (
    close_value_stock_monthly,
    StockClosePriceError,
)

# %%
load_dotenv()
service_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS")
api_key = os.getenv("FINANCIAL_API_KEY")

title = "Valoracion"

gc = pygsheets.authorize(service_file=service_file)


financial_analysis = gc.open(title)

# %%
worksheet_main_data = "Main"
worksheet_stock_data = "stock_close_price"

wks_data = financial_analysis.worksheet_by_title(worksheet_main_data)
wks_stock_prices = financial_analysis.worksheet_by_title(worksheet_stock_data)
df_symbols = pd.DataFrame(wks_data.get_all_records())
symbols = df_symbols["Symbol"].unique()

if len(symbols) > 0:
    try:
        balance_sheet(symbols, api_key, financial_analysis)
    except Exception as e:
        raise BalanceSheetError(
            "An error occurred while fetching the balance sheet."
        ) from e

    try:
        income_statement(symbols, api_key, financial_analysis)
    except Exception as e:
        raise IncomeStatementError(
            "An error occurred while fetching the Income statement sheet."
        ) from e

    try:
        close_value_stock_monthly(symbols, api_key, wks_stock_prices)
    except Exception as e:
        raise StockClosePriceError(
            "An error occurred while fetching the Stock Close Price sheet."
        ) from e


# %%
