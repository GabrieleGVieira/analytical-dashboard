from app.modules.repositories import SaleRepository

class ProfitMargin:
    def __init__(self, sale_repo: SaleRepository):
        self.sale_repo = sale_repo

    def run(self, start_date: str, end_date: str):
        sales_total, costs_total = self.sale_repo.get_costs_sales_total(start_date, end_date)
        profit = sales_total - costs_total
        percent = self._calculate_percent(sales_total, profit)
        return sales_total, costs_total, profit, percent

    @staticmethod
    def _calculate_percent(sales_total,profit):
        return (profit / sales_total * 100) if sales_total > 0 else 0
