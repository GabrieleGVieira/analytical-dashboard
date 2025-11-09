from apscheduler.schedulers.background import BackgroundScheduler
import logging

from app.modules.controllers.collector_controller import CollectorController

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler(app):
    """
    Inicializa o scheduler com jobs agendados.
    """
    controller = CollectorController()
    scheduler.add_job(
        func=lambda: collect_currency_job(app, controller),
        trigger='cron',
        hour=21,
        minute=0,
        id='daily_currency_collection',
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler iniciado com job de coleta diária de cotações.")

def collect_currency_job(app, controller):
    """
    Job executado automaticamente pelo scheduler.
    """
    try:
        with app.app_context():  # garante que current_app e db funcionem
            num = controller.collect_currency()
            logger.info(f"Coleta automática de cotações concluída. Registros processados: {num}")
    except Exception as e:
        logger.exception(f"Erro ao coletar cotações automaticamente: {e}")
