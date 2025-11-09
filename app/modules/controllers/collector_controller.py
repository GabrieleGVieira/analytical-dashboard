import logging
from flask import jsonify
from app.modules.repositories import CurrencyRepository
from app import db
from app.modules.usecases.collector.collect_currency import CollectCurrency

logger = logging.getLogger(__name__)

class CollectorController:
    def __init__(self):
        self.currency_repo = None
        self.use_case = None

    def collect_currency(self):
        """
        Controller para coletar cotações automáticas via API
        """
        try:
            session = db.session
            self.currency_repo = CurrencyRepository(session)
            self.use_case = CollectCurrency(self.currency_repo)

            num_collected = self.use_case.run()
            return jsonify({"collected": num_collected}), 200

        except Exception as e:
            logger.exception("Erro ao coletar cotações: %s", e)
            return jsonify({"error": str(e)}), 500
