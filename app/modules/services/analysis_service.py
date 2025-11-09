import logging
from typing import Tuple
import pandas as pd

logger = logging.getLogger(__name__)

class DataAnalysisService:
    @staticmethod
    def calculate_correlation(
            sales: list, currency: list
    ) -> Tuple[pd.DataFrame, float | None]:
        """
        Calcula a correlação entre vendas e cotação de moeda.

        :param sales: Lista de tuplas (data, sales_total)
        :param currency: Lista de tuplas (data, currency_price)
        :return: Tuple com DataFrame combinado e valor da correlação
        """
        try:
            df_sales = pd.DataFrame(sales, columns=["date", "sales_total"])
            df_currency = pd.DataFrame(currency, columns=["date", "currency_price"])

            df = pd.merge(df_sales, df_currency, on="date", how="inner")

            if df.empty:
                logger.warning("Dados combinados estão vazios. Correlação não calculada.")
                return df, None

            corr = df["sales_total"].corr(df["currency_price"])
            return df, corr

        except Exception as e:
            logger.exception("Erro ao calcular correlação: %s", e)
            return pd.DataFrame(), None
