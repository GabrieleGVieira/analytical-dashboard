import logging
from datetime import datetime
from typing import List

import requests
from flask import current_app

from app.infrastructure.database.models import Cotacao

logger = logging.getLogger(__name__)

class CollectorService:
    @staticmethod
    def collect_latest_quotes() -> List[Cotacao]:
        """
        Coleta as cotações atuais de moedas (USD e EUR) e retorna
        como lista de objetos Cotacao.

        :return: Lista de Cotacao
        """
        base_url = current_app.config.get('AWESOMEAPI_BASE_URL')
        if not base_url:
            logger.error("Configuração 'AWESOMEAPI_BASE_URL' não encontrada.")
            return []

        try:
            response = requests.get(f'{base_url}/last/USD-BRL,EUR-BRL', timeout=10)
            response.raise_for_status()
            data = response.json()

            cotacoes: List[Cotacao] = []

            # Processa USD
            if 'USDBRL' in data:
                usd_data = data['USDBRL']
                cotacao_usd = Cotacao(
                    moeda='USD',
                    valor=float(usd_data['bid']),
                    data_hora=datetime.fromtimestamp(int(usd_data['timestamp']))
                )
                cotacoes.append(cotacao_usd)
            else:
                logger.warning("Cotação USD não encontrada na resposta.")

            # Processa EUR
            if 'EURBRL' in data:
                eur_data = data['EURBRL']
                cotacao_eur = Cotacao(
                    moeda='EUR',
                    valor=float(eur_data['bid']),
                    data_hora=datetime.fromtimestamp(int(eur_data['timestamp']))
                )
                cotacoes.append(cotacao_eur)
            else:
                logger.warning("Cotação EUR não encontrada na resposta.")

            return cotacoes

        except requests.RequestException as e:
            logger.error("Erro ao coletar cotações: %s", e)
            return []
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Erro ao processar dados da API: %s", e)
            return []