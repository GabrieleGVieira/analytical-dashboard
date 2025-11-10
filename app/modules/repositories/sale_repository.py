import logging
from typing import List, Tuple, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.domain.entities import SellerPerformance
from app.infrastructure.database.models import Venda, Custo

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

    def get_sales_mount_and_values_by_day(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        try:
            query = self._session.query(
                Venda.data.label("date"),
                func.sum(Venda.valor_total).label('values'),
                func.sum(Venda.quantidade).label('amount')
            )

            if start_date:
                query = query.filter(Venda.data >= start_date)
            if end_date:
                query = query.filter(Venda.data <= end_date)

            query = query.group_by(Venda.data).order_by(Venda.data)

            results = query.all()
            return results

        except Exception as e:
            logger.exception(f"Erro ao buscar resumo diário de vendas: {e}")
            return []

    def get_costs_sales_total(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """
                           Retorna vendas e custos totais de um produto.
                           """
        try:

            query = (
                self._session.query(
                    func.sum(Venda.valor_total).label("sales_total"),
                    func.sum(Venda.quantidade * Custo.custo_unitario).label("costs_total")
                )
                .join(Custo, Venda.produto == Custo.produto)
                .filter(Venda.data.between(start_date, end_date))
            )
            result = query.first()
            sales_total = result.sales_total or 0
            costs_total = result.costs_total or 0
            return sales_total, costs_total
        except Exception as e:
            logger.exception(f"Erro ao buscar total de vendas: {e}")
            return []

    def get_sales_summary_by_seller(self, year: int, month: int) -> List[SellerPerformance]:
        """
        Retorna total de vendas, quantidade e lucro por vendedor no mês.
        """
        subquery_cost = (
            self._session.query(
                Custo.produto,
                Custo.custo_unitario.label("custo_unitario")
            ).subquery()
        )

        query = (
            self._session.query(
                Venda.vendedor.label("seller"),
                Venda.categoria.label("category"),
                Venda.regiao.label("region"),
                func.sum(Venda.valor_total).label("total_sales"),
                func.sum(Venda.quantidade).label("total_quantity"),
                func.sum(
                    Venda.valor_total -
                    (Venda.quantidade * func.coalesce(subquery_cost.c.custo_unitario, 0))
                ).label("total_profit")
            )
            .join(subquery_cost, subquery_cost.c.produto == Venda.produto, isouter=True)
            .filter(func.extract('year', Venda.data) == year)
            .filter(func.extract('month', Venda.data) == month)
            .group_by(Venda.vendedor)
            .all()
        )

        return query
