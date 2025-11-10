"""
Rotas do módulo Analytics (API de dados para o dashboard).
"""

from flask import Blueprint
from app.modules.controllers.analytics_controller import AnalyticsController


def analytics_routes(app):
    """
    Registra as rotas do módulo Analytics no app Flask.
    """

    analytics_bp = Blueprint('analytics', __name__, url_prefix="/api/analytics")

    controller = AnalyticsController()

    # --- Rotas de dados analíticos ---
    # analytics_bp.add_url_rule('/kpis', view_func=controller.get_kpis, methods=['GET'])
    # analytics_bp.add_url_rule('/vendas-tempo', view_func=controller.get_vendas_tempo, methods=['GET'])
    # analytics_bp.add_url_rule('/vendas-categoria', view_func=controller.get_vendas_categoria, methods=['GET'])
    # analytics_bp.add_url_rule('/vendas-regiao', view_func=controller.get_vendas_regiao, methods=['GET'])
    # analytics_bp.add_url_rule('/top-produtos', view_func=controller.get_top_produtos, methods=['GET'])
    analytics_bp.add_url_rule('/sales-currency-correlation', view_func=controller.get_sales_currency_correlation, methods=['GET'])
    analytics_bp.add_url_rule('/long-term-sales', view_func=controller.get_long_term_sales, methods=['GET'])
    analytics_bp.add_url_rule("/profit-margin", view_func=controller.get_profit_margin, methods=['GET'])
    analytics_bp.add_url_rule("/seller-ranking", view_func=controller.get_seller_ranking, methods=['GET'])
    analytics_bp.add_url_rule("/sales-by-category", view_func=controller.get_total_sales_by_category, methods=['GET'])

    app.register_blueprint(analytics_bp)
