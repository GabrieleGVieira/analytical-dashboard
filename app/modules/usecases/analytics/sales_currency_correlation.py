import logging
from typing import Tuple
import pandas as pd
from app.modules.repositories import SaleRepository, CurrencyRepository
from app.modules.services.analysis_service import DataAnalysisService

logger = logging.getLogger(__name__)


class SalesCurrencyCorrelation:
    def __init__(self, sale_repo: SaleRepository, currency_repo: CurrencyRepository):
        self.sale_repo = sale_repo
        self.currency_repo = currency_repo
        self.analysis_service = DataAnalysisService()

    def run(
            self, start_date: str, end_date: str, currency: str
    ) -> Tuple[pd.DataFrame, float]:
        """
        Calcula a correlação entre vendas e cotação de uma moeda.

        :param start_date: Data inicial no formato 'YYYY-MM-DD'
        :param end_date: Data final no formato 'YYYY-MM-DD'
        :param currency: Código da moeda (ex: "USD", "EUR")
        :return: Tuple com DataFrame e valor da correlação
        """
        try:
            logger.info(
                "Iniciando análise de correlação de vendas x %s de %s até %s",
                currency, start_date, end_date
            )

            sales = self.sale_repo.get_sales_by_day(start_date, end_date)
            currency_price = self.currency_repo.get_currency_price_by_day(currency, start_date, end_date)
            print(currency_price)

            if not sales or not currency_price:
                logger.warning("Dados insuficientes para calcular correlação.")
                return pd.DataFrame(), 0.0

            df, correlation = self.analysis_service.calculate_correlation(sales, currency_price)

            logger.info(
                "Análise concluída. Correlação: %.4f", correlation
            )
            return df, correlation

        except Exception as e:
            logger.exception("Erro ao calcular correlação: %s", e)
            return pd.DataFrame(), 0.0
