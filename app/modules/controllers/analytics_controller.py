# controllers/dashboard_controller.py
from flask import request

from app.modules.repositories import SaleRepository, CurrencyRepository
from app.modules.usecases.analytics.sales_currency_correlation import SalesCurrencyCorrelation
from app import db


class AnalyticsController:
    def __init__(self):
        self.sale_repo = None
        self.currency_repo = None
        self.use_case = None

    def get_sales_currency_correlation(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        currency = request.args.get("currency", "USD")
        session = db.session

        self.sale_repo = SaleRepository(session)
        self.currency_repo = CurrencyRepository(session)
        self.use_case = SalesCurrencyCorrelation(self.sale_repo, self.currency_repo)
        df, corr = self.use_case.run(start_date, end_date, currency)

        return {
            "moeda": currency,
            "correlacao": float(round(corr, 3)) if corr is not None else None,
            "dados": [
                {
                    "data": row.data.strftime("%Y-%m-%d"),
                    "qtd_vendas": int(row.sales_total),
                    "cotacao": float(row.currency_price)
                }
                for row in df.itertuples()
            ]
        }
