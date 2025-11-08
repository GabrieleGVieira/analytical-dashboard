# domain/repositories/venda_repository.py
import logging
from typing import List, Tuple, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from app.infrastructure.database.models import Venda

logger = logging.getLogger(__name__)

class SaleRepository:
    def __init__(self, session):
        self._session = session

    def get_sales_by_day(
            self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[Tuple[str, int]]:
        """
           Retorna a quantidade total de vendas por dia dentro do período.
           :param start_date: Data inicial no formato 'YYYY-MM-DD'
           :param end_date: Data final no formato 'YYYY-MM-DD'
           :return: Lista de tuplas (data, total_vendas)
           """
        try:
            query = (
                self._session.query(
                    func.date(Venda.data).label("date"),
                    func.sum(Venda.quantidade).label("sales_total")
                )
            )
            if start_date:
                query = query.filter(Venda.data >= start_date)
            if end_date:
                query = query.filter(Venda.data <= end_date)
            query = query.group_by(func.date(Venda.data))
            return query.all()
        except SQLAlchemyError as e:
            logger.exception("Erro ao consultar vendas por dia: %s", e)
            return []
