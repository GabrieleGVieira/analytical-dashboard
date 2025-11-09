from app.modules.repositories import CurrencyRepository
from app.modules.services.collector_service import CollectorService


class CollectCurrency:
    def __init__(self, currency_repo: CurrencyRepository):
        self.currency_repo = currency_repo
        self.collector_service = CollectorService()

    def run(self):
        currency_list = self.collector_service.collect_latest_quotes()
        for currency in currency_list:
            self.currency_repo.add_or_update(currency)
        return len(currency_list)
