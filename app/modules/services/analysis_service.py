import pandas as pd


class DataAnalysisService:
    @staticmethod
    def calculate_correlation(sales, currency):
            df_sales = pd.DataFrame(sales, columns=["date", "sales_total"])
            df_currency = pd.DataFrame(currency, columns=["date", "currency_price"])
            df = pd.merge(df_sales, df_currency, on="date")
            corr = df["sales_total"].corr(df["currency_price"]) if not df.empty else None
            return df, corr
