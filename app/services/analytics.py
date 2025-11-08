"""
Serviço de análises e agregações.
"""
import pandas as pd
from datetime import datetime
from sqlalchemy import func
from app import db
from app.infrastructure.database.models import Venda, Cotacao


class Analytics:
    """Realiza análises estatísticas e agregações."""
    
    def calcular_kpis(self, data_inicio=None, data_fim=None):
        """
        Calcula KPIs principais.
        
        Args:
            data_inicio: Data inicial (string YYYY-MM-DD)
            data_fim: Data final (string YYYY-MM-DD)
            
        Returns:
            dict: KPIs calculados
        """
        query = db.session.query(
            func.sum(Venda.valor_total).label('receita_total'),
            func.count(Venda.id).label('num_vendas'),
            func.avg(Venda.valor_total).label('ticket_medio')
        )
        
        query = self._aplicar_filtro_data(query, Venda, data_inicio, data_fim)
        resultado = query.first()
        
        return {
            'receita_total': float(resultado.receita_total or 0),
            'num_vendas': int(resultado.num_vendas or 0),
            'ticket_medio': float(resultado.ticket_medio or 0)
        }
    
    def vendas_ao_longo_tempo(self, data_inicio=None, data_fim=None):
        """
        Retorna série temporal de vendas.
        
        Returns:
            dict: Dados para gráfico de linhas
        """
        query = db.session.query(
            Venda.data,
            func.sum(Venda.valor_total).label('valor'),
            func.sum(Venda.quantidade).label('quantidade')
        )
        
        query = self._aplicar_filtro_data(query, Venda, data_inicio, data_fim)
        query = query.group_by(Venda.data).order_by(Venda.data)
        
        resultados = query.all()
        
        return {
            'labels': [r.data.strftime('%Y-%m-%d') for r in resultados],
            'valores': [float(r.valor) for r in resultados],
            'quantidades': [int(r.quantidade) for r in resultados]
        }
    
    def vendas_por_categoria(self, data_inicio=None, data_fim=None):
        """
        Retorna vendas agregadas por categoria.
        
        Returns:
            dict: Dados para gráfico de barras
        """
        query = db.session.query(
            Venda.categoria,
            func.sum(Venda.valor_total).label('valor'),
            func.sum(Venda.quantidade).label('quantidade')
        )
        
        query = self._aplicar_filtro_data(query, Venda, data_inicio, data_fim)
        query = query.group_by(Venda.categoria).order_by(func.sum(Venda.valor_total).desc())
        
        resultados = query.all()
        
        return {
            'labels': [r.categoria for r in resultados],
            'valores': [float(r.valor) for r in resultados],
            'quantidades': [int(r.quantidade) for r in resultados]
        }
    
    def vendas_por_regiao(self, data_inicio=None, data_fim=None):
        """
        Retorna vendas agregadas por região.
        
        Returns:
            dict: Dados para gráfico de pizza
        """
        query = db.session.query(
            Venda.regiao,
            func.sum(Venda.valor_total).label('valor')
        )
        
        query = self._aplicar_filtro_data(query, Venda, data_inicio, data_fim)
        query = query.group_by(Venda.regiao).order_by(func.sum(Venda.valor_total).desc())
        
        resultados = query.all()
        total = sum(r.valor for r in resultados)
        
        return {
            'labels': [r.regiao for r in resultados],
            'valores': [float(r.valor) for r in resultados],
            'percentuais': [round((r.valor / total * 100), 2) if total > 0 else 0 for r in resultados]
        }
    
    def top_produtos(self, data_inicio=None, data_fim=None, limite=10):
        """
        Retorna top produtos mais vendidos.
        
        Args:
            limite: Número de produtos a retornar
            
        Returns:
            dict: Dados para gráfico de barras horizontal
        """
        query = db.session.query(
            Venda.produto,
            func.sum(Venda.valor_total).label('valor'),
            func.sum(Venda.quantidade).label('quantidade')
        )
        
        query = self._aplicar_filtro_data(query, Venda, data_inicio, data_fim)
        query = query.group_by(Venda.produto).order_by(func.sum(Venda.valor_total).desc()).limit(limite)
        
        resultados = query.all()
        
        return {
            'labels': [r.produto for r in resultados],
            'valores': [float(r.valor) for r in resultados],
            'quantidades': [int(r.quantidade) for r in resultados]
        }

    def correlacao_vendas_cotacao(self, data_inicio=None, data_fim=None, moeda="USD"):
        """
        Calcula a correlação entre a quantidade de vendas e a cotação da moeda
        no período especificado.

        Args:
            data_inicio (datetime, opcional): Data inicial do período.
            data_fim (datetime, opcional): Data final do período.

        Returns:
            dict:
                - correlacao (float): Coeficiente de correlação entre vendas e dólar.
                - dados (list[dict]): Lista com data, quantidade de vendas e cotação do dólar.
        """
        # 1. Agregar vendas por dia
        query_vendas = (
            db.session.query(
                func.date(Venda.data).label("data"),
                func.sum(Venda.quantidade).label("qtd_vendas")
            )
        )

        query_vendas = self._aplicar_filtro_data(query_vendas, Venda, data_inicio, data_fim)
        query_vendas = query_vendas.group_by(func.date(Venda.data))
        vendas_por_dia = query_vendas.all()

        # 2. Buscar cotação da moeda por dia
        query_moeda = (
            db.session.query(
                func.date(Cotacao.data_hora).label("data"),
                func.avg(Cotacao.valor).label("cotacao")
            )
            .filter(Cotacao.moeda == moeda)
        )
        query_moeda = self._aplicar_filtro_data(query_moeda, Cotacao, data_inicio, data_fim)
        query_moeda = query_moeda.group_by(func.date(Cotacao.data))
        cotacoes_por_dia = query_moeda.all()

        # 3. Converter para DataFrame
        df_vendas = pd.DataFrame(vendas_por_dia, columns=["data", "qtd_vendas"])
        df_cotacao = pd.DataFrame(cotacoes_por_dia, columns=["data", "cotacao"])

        # 4. Juntar e calcular correlação
        df = pd.merge(df_vendas, df_cotacao, on="data")
        correlacao = df["qtd_vendas"].corr(df["cotacao"]) if not df.empty else None

        # 5. Retornar resultado no mesmo padrão de saída
        return {
            "moeda": moeda,
            "correlacao": float(round(correlacao, 3)) if correlacao is not None else None,
            "dados": [
                {
                    "data": row.data.strftime("%Y-%m-%d"),
                    "qtd_vendas": int(row.qtd_vendas),
                    "cotacao": float(row.cotacao)
                }
                for row in df.itertuples()
            ]
        }

    def _aplicar_filtro_data(self, query, model, data_inicio=None, data_fim=None):
        """Aplica filtros de data na query."""
        if data_inicio:
            try:
                dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                query = query.filter(model.data >= dt_inicio)
            except ValueError:
                pass
        
        if data_fim:
            try:
                dt_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
                query = query.filter(model.data <= dt_fim)
            except ValueError:
                pass
        
        return query
