import requests
import pandas as pd
import pygsheets


class BalanceSheetError(Exception):
    """Custom exception for balance sheet errors."""

    pass


class IncomeStatementError(Exception):
    """Custom exception for Income statement errors."""

    pass


class StockClosePriceError(Exception):
    """Custom exception for Stock Prices errors."""

    pass


def balance_sheet(symbols, api_key, financial_analysis):

    for symbol in symbols:

        url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()

        quartely_reports = data["quarterlyReports"]

        df_quartely_report = pd.DataFrame(quartely_reports)

        df_quartely_report = df_quartely_report.rename(
            columns={
                "fiscalDateEnding": "fiscal_date_ending",
                "reportedCurrency": "reported_currency",
                "totalAssets": "total_assets",
                "totalCurrentAssets": "total_current_assets",
                "cashAndCashEquivalentsAtCarryingValue": "cash_and_cash_equivalents_at_carrying_value",
                "cashAndShortTermInvestments": "cash_and_short_term_investments",
                "inventory": "inventory",
                "currentNetReceivables": "current_net_receivables",
                "totalNonCurrentAssets": "total_non_current_assets",
                "propertyPlantEquipment": "property_plant_and_equipment",
                "accumulatedDepreciationAmortizationPPE": "accumulated_depreciation_amortization_ppe",
                "intangibleAssets": "intangible_assets",
                "intangibleAssetsExcludingGoodwill": "intangible_assets_excluding_goodwill",
                "goodwill": "goodwill",
                "investments": "investments",
                "longTermInvestments": "long_term_investments",
                "shortTermInvestments": "short_term_investments",
                "otherCurrentAssets": "other_current_assets",
                "otherNonCurrentAssets": "other_non_current_assets",
                "totalLiabilities": "total_liabilities",
                "totalCurrentLiabilities": "total_current_liabilities",
                "currentAccountsPayable": "current_accounts_payable",
                "deferredRevenue": "deferred_revenue",
                "currentDebt": "current_debt",
                "shortTermDebt": "short_term_debt",
                "totalNonCurrentLiabilities": "total_non_current_liabilities",
                "capitalLeaseObligations": "capital_lease_obligations",
                "longTermDebt": "long_term_debt",
                "currentLongTermDebt": "current_long_term_debt",
                "longTermDebtNoncurrent": "long_term_debt_noncurrent",
                "shortLongTermDebtTotal": "short_long_term_debt_total",
                "otherCurrentLiabilities": "other_current_liabilities",
                "otherNonCurrentLiabilities": "other_non_current_liabilities",
                "totalShareholderEquity": "total_shareholder_equity",
                "treasuryStock": "treasury_stock",
                "retainedEarnings": "retained_earnings",
                "commonStock": "common_stock",
                "commonStockSharesOutstanding": "common_stock_shares_outstanding",
            }
        )

        for col in df_quartely_report.columns:
            df_quartely_report[col] = df_quartely_report[col].fillna(0)
            df_quartely_report[col] = df_quartely_report[col].replace("None", 0)

        symbol_worksheet = f"balance_sheet_{symbol}"
        try:
            wks = financial_analysis.worksheet_by_title(symbol_worksheet)
        except pygsheets.WorksheetNotFound:
            wks = financial_analysis.add_worksheet(symbol_worksheet)

        wks.clear()
        wks.set_dataframe(df_quartely_report, "A1")

    return "Balance sheet created"


def income_statement(symbols, api_key, financial_analysis):

    for symbol in symbols:

        url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()

        quartely_reports = data["quarterlyReports"]

        df_quartely_report = pd.DataFrame(quartely_reports)

        new_columns = {
            "fiscalDateEnding": "fiscal_date_ending",
            "reportedCurrency": "reported_currency",
            "grossProfit": "gross_profit",
            "totalRevenue": "total_revenue",
            "costOfRevenue": "cost_of_revenue",
            "costofGoodsAndServicesSold": "cost_of_goods_and_services_sold",
            "operatingIncome": "operating_income",
            "sellingGeneralAndAdministrative": "selling_general_and_administrative",
            "researchAndDevelopment": "research_and_development",
            "operatingExpenses": "operating_expenses",
            "investmentIncomeNet": "investment_income_net",
            "netInterestIncome": "net_interest_income",
            "interestIncome": "interest_income",
            "interestExpense": "interest_expense",
            "nonInterestIncome": "non_interest_income",
            "otherNonOperatingIncome": "other_non_operating_income",
            "depreciation": "depreciation",
            "depreciationAndAmortization": "depreciation_and_amortization",
            "incomeBeforeTax": "income_before_tax",
            "incomeTaxExpense": "income_tax_expense",
            "interestAndDebtExpense": "interest_and_debt_expense",
            "netIncomeFromContinuingOperations": "net_income_from_continuing_operations",
            "comprehensiveIncomeNetOfTax": "comprehensive_income_net_of_tax",
            "ebit": "ebit",
            "ebitda": "ebitda",
            "netIncome": "net_income",
        }

        df_quartely_report = df_quartely_report.rename(columns=new_columns)

        for col in df_quartely_report.columns:
            df_quartely_report[col] = df_quartely_report[col].fillna(0)
            df_quartely_report[col] = df_quartely_report[col].replace("None", 0)

        symbol_worksheet = f"income_statement_{symbol}"
        try:
            wks = financial_analysis.worksheet_by_title(symbol_worksheet)
        except pygsheets.WorksheetNotFound:
            wks = financial_analysis.add_worksheet(symbol_worksheet)

        wks.clear()
        wks.set_dataframe(df_quartely_report, "A1")

    return "Income statement sheet created"


def close_value_stock_monthly(symbols, api_key, wks_stock_prices):

    for symbol in symbols:

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()

        monthly_prices = data["Monthly Time Series"]
        df_monthly_prices = pd.DataFrame(monthly_prices).T
        df_monthly_prices_close = df_monthly_prices["4. close"].reset_index()

        df_monthly_prices_close = df_monthly_prices_close.rename(
            columns={"index": "date", "4. close": "value"}
        )

        end_date = pd.Timestamp.now()  # Current date
        start_date = end_date - pd.DateOffset(years=20)  # Date 20 years ago

        # Generate the last day of each month
        last_days = pd.date_range(start=start_date, end=end_date, freq="M")
        if end_date != end_date + pd.offsets.MonthEnd(0):
            # If not the last day, exclude the current month
            last_days = last_days[:-1]

        last_days_str = last_days.strftime("%Y-%m-%d").tolist()

        df_monthly_prices_close_filtered = df_monthly_prices_close[
            df_monthly_prices_close["date"].isin(last_days_str)
        ]

        df_monthly_prices_close_filtered["symbol"] = symbol

        df_stock_close_price = pd.DataFrame(wks_stock_prices.get_all_records())

        if len(df_stock_close_price) > 0:
            df_stock_close_price = pd.concat(
                [df_stock_close_price, df_monthly_prices_close_filtered],
                ignore_index=True,
            )
            df_stock_close_price = df_stock_close_price.drop_duplicates(
                subset=["date", "symbol"], keep="last"
            )

            wks_stock_prices.clear()
            wks_stock_prices.set_dataframe(df_stock_close_price, "A1")
        else:
            wks_stock_prices.set_dataframe(df_monthly_prices_close_filtered, "A1")

    return "Stock prices added"
