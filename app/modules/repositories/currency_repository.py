import logging
from typing import List, Tuple, Optional
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database.models import Cotacao

logger = logging.getLogger(__name__)


class CurrencyRepository:
    def __init__(self, session):
        self._session = session

    def get_currency_price_by_day(
            self,
            currency: str = "USD",
            start_date: Optional[str] = None,
            end_date: Optional[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Retorna a cotação média diária de uma moeda dentro do período.

        :param currency: Código da moeda (ex: "USD", "EUR")
        :param start_date: Data inicial no formato 'YYYY-MM-DD'
        :param end_date: Data final no formato 'YYYY-MM-DD'
        :return: Lista de tuplas (data, cotação_média)
        """
        try:
            query = (
                self._session.query(
                    func.date(Cotacao.data_hora).label("date"),
                    func.avg(Cotacao.valor).label("currency_price")
                )
                .filter(Cotacao.moeda == currency)
            )

            if start_date:
                query = query.filter(Cotacao.data_hora >= start_date)
            if end_date:
                query = query.filter(Cotacao.data_hora <= end_date)

            query = query.group_by(func.date(Cotacao.data_hora))

            results = query.all()
            return results

        except SQLAlchemyError as e:
            logger.exception("Erro ao consultar cotação de %s: %s", currency, e)
            return []
