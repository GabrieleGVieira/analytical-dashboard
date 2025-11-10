import logging
from app.infrastructure.database.models import Meta

logger = logging.getLogger(__name__)

class GoalRepository:
    def __init__(self, session):
        self._session = session

    def get_goals_for_month(self, year: int, month: int):
        return self._session.query(Meta).filter_by(ano=year, mes=month).all()