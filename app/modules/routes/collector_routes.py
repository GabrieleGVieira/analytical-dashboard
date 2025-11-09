"""
Rotas do módulo Currency (API para coleta de cotações).
"""

from flask import Blueprint

from app.modules.controllers.collector_controller import CollectorController


def collector_routes(app):
    """
    Registra as rotas do módulo Currency no app Flask.
    """

    currency_bp = Blueprint('currency', __name__, url_prefix="/api/currency")

    controller = CollectorController()

    currency_bp.add_url_rule('/collect-currency', view_func=controller.collect_currency, methods=['POST'])

    app.register_blueprint(currency_bp)
