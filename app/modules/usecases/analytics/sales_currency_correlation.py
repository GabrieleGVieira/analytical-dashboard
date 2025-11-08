from app.modules.repositories import SaleRepository, CurrencyRepository
from app.modules.services.analysis_service import DataAnalysisService


class SalesCurrencyCorrelation:
    def __init__(self, sale_repo: SaleRepository, currency_repo: CurrencyRepository):
        self.sale_repo = sale_repo
        self.currency_repo = currency_repo
        self.analysis_service = DataAnalysisService

    def run(self, start_date, end_date, currency):
        sales = self.sale_repo.get_sales_by_day(start_date, end_date)
        currency_price = self.currency_repo.get_currency_price_by_day(currency, start_date, end_date)

        df, correlation = self.analysis_service.calculate_correlation(sales, currency_price)
        return df, correlation
