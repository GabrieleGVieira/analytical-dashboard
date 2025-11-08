# domain/repositories/cotacao_repository.py
from sqlalchemy import func
from app.infrastructure.database.models import Cotacao


class CurrencyRepository:
    def __init__(self,session):
        self._session = session

    def get_currency_price_by_day(self, currency="USD", start_date=None, end_date=None) -> int:
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
        return query.all()
