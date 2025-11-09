import logging
from typing import List, Dict
from app.modules.repositories import SaleRepository

logger = logging.getLogger(__name__)

class MultiplePeriodSales:
    """
    Caso de uso para obter o resumo de vendas em um período específico.
    """

    def __init__(self, sale_repo: SaleRepository):
        self.sale_repo = sale_repo

    def run(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Retorna o resumo diário de vendas entre start_date e end_date.

        Args:
            start_date (str): Data inicial no formato 'YYYY-MM-DD'
            end_date (str): Data final no formato 'YYYY-MM-DD'

        Returns:
            List[Dict]: Lista de dicionários com 'data', 'valor' e 'quantidade'
        """
        try:
            sales = self.sale_repo.get_daily_sales_summary(start_date, end_date)
            return sales
        except Exception as e:
            logger.exception(f"Erro ao executar resumo de vendas: {e}")
            return []
