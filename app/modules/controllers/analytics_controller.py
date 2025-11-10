import logging
from flask import request, jsonify
from app.modules.repositories import SaleRepository, CurrencyRepository
from app import db
from app.modules.usecases.analytics import SalesCurrencyCorrelation, MultiplePeriodSales, LongTermSales, ProfitMargin

logger = logging.getLogger(__name__)

class AnalyticsController:
    def __init__(self):
        self.sale_repo = None
        self.currency_repo = None
        self.use_case = None
        self.session = db.session

    def get_sales_currency_correlation(self):
        try:
            start_date = request.args.get("data_inicio")
            end_date = request.args.get("data_fim")
            currency = request.args.get("currency", "USD")

            logger.info(
                "Iniciando requisição de correlação de vendas x %s de %s até %s",
                currency, start_date, end_date
            )

            self.sale_repo = SaleRepository(self.session)
            self.currency_repo = CurrencyRepository(self.session)
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

    def get_long_term_sales(self):
        try:
            start_date = request.args.get("data_inicio")
            end_date = request.args.get("data_fim")
            logger.info(
                "Iniciando requisição para pegar evolução de vendas de %s até %s",
                start_date, end_date
            )

            self.sale_repo = SaleRepository(self.session)
            self.use_case = LongTermSales(self.sale_repo)

            sales = self.use_case.run(start_date, end_date)

            response = {
            'labels': [s.date.strftime('%Y-%m-%d') for s in sales],
            'valores': [float(s.values) for s in sales],
            'quantidades': [int(s.amount) for s in sales]
        }

            logger.info(
                "Requisição concluída. Registros retornados: %d", len(response["valores"])
            )
            return jsonify(response), 200

        except Exception as e:
            logger.exception("Erro ao processar requisição para evolução de vendas: %s", e)
            return jsonify({"error": str(e)}), 500

    def get_profit_margin(self):
        try:
            start_date = request.args.get("data_inicio")
            end_date = request.args.get("data_fim")
            logger.info(
                "Iniciando requisição para pegar margem de lucro de %s até %s",
                start_date, end_date
            )

            self.sale_repo = SaleRepository(self.session)
            self.use_case = ProfitMargin(self.sale_repo)

            sales_total, costs_total, profit, percent = self.use_case.run(start_date, end_date)

            response = {
            "total_vendas": sales_total,
            "total_custos": costs_total,
            "lucro_total": profit,
            "margem_percentual": percent
        }

            return jsonify(response), 200

        except Exception as e:
            logger.exception("Erro ao processar requisição pegar margem de lucris: %s", e)
            return jsonify({"error": str(e)}), 500

