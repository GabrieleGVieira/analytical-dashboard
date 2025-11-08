import logging
from flask import request, jsonify
from app.modules.repositories import SaleRepository, CurrencyRepository
from app.modules.usecases.analytics.sales_currency_correlation import SalesCurrencyCorrelation
from app import db

logger = logging.getLogger(__name__)

class AnalyticsController:
    def __init__(self):
        self.sale_repo = None
        self.currency_repo = None
        self.use_case = None

    def get_sales_currency_correlation(self):
        try:
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            currency = request.args.get("currency", "USD")

            logger.info(
                "Iniciando requisição de correlação de vendas x %s de %s até %s",
                currency, start_date, end_date
            )

            session = db.session
            self.sale_repo = SaleRepository(session)
            self.currency_repo = CurrencyRepository(session)
            self.use_case = SalesCurrencyCorrelation(self.sale_repo, self.currency_repo)

            df, corr = self.use_case.run(start_date, end_date, currency)

            response = {
                "moeda": currency,
                "correlacao": float(round(corr, 3)) if corr is not None else None,
                "dados": [
                    {
                        "data": row.data.strftime("%Y-%m-%d"),
                        "qtd_vendas": int(row.sales_total),
                        "cotacao": float(row.currency_price)
                    }
                    for row in df.itertuples()
                ]
            }

            logger.info(
                "Requisição concluída. Registros retornados: %d", len(response["dados"])
            )
            return jsonify(response), 200

        except Exception as e:
            logger.exception("Erro ao processar requisição de correlação: %s", e)
            return jsonify({"error": str(e)}), 500
