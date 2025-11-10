import logging
from typing import List, Dict
from app.modules.repositories import SaleRepository

logger = logging.getLogger(__name__)

class SalesByCategory:
    def __init__(self, sale_repo: SaleRepository):
        self.sale_repo = sale_repo

    def run(self, start_date: str, end_date: str) -> List[Dict]:
        try:
            sales = self.sale_repo.get_sales_amount_by_category(start_date, end_date)
            return sales
        except Exception as e:
            logger.exception(f"Erro ao executar resumo de vendas: {e}")
            return []
