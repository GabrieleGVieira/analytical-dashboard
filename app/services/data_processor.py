"""
Serviço de processamento de dados.
"""
import pandas as pd
from datetime import datetime
from flask import current_app
from app import db
from app.infrastructure.database.models import Venda, Custo


class DataProcessor:
    """Processa e valida dados."""
    
    def processar_upload(self, file, tipo):
        """
        Processa arquivo enviado via upload.
        
        Args:
            file: Arquivo FileStorage do Flask
            tipo: Tipo de dados (vendas, custos)
            
        Returns:
            int: Número de registros processados
        """
        if tipo == 'vendas':
            return self._processar_vendas_csv(file)
        elif tipo == 'custos':
            return self._processar_custos_csv(file)
        else:
            raise ValueError(f"Tipo não suportado: {tipo}")
    
    def _processar_vendas_csv(self, file):
        """Processa CSV de vendas."""
        try:
            # Lê CSV
            df = pd.read_csv(file)
            
            # Valida colunas obrigatórias
            colunas_obrigatorias = [
                'data', 'produto', 'categoria', 'quantidade',
                'preco_unitario', 'regiao', 'vendedor'
            ]
            self._validar_colunas(df, colunas_obrigatorias)
            
            # Processa cada linha
            registros_processados = 0
            for _, row in df.iterrows():
                try:
                    # Calcula valor total
                    valor_total = row['quantidade'] * row['preco_unitario']
                    
                    venda = Venda(
                        data=pd.to_datetime(row['data']).date(),
                        produto=str(row['produto']),
                        categoria=str(row['categoria']),
                        quantidade=int(row['quantidade']),
                        preco_unitario=float(row['preco_unitario']),
                        valor_total=valor_total,
                        regiao=str(row['regiao']),
                        vendedor=str(row['vendedor'])
                    )
                    
                    db.session.add(venda)
                    registros_processados += 1
                    
                except Exception as e:
                    current_app.logger.warning(f"Erro ao processar linha: {e}")
                    continue
            
            db.session.commit()
            return registros_processados
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao processar vendas: {e}")
    
    def _processar_custos_csv(self, file):
        """Processa CSV de custos."""
        try:
            df = pd.read_csv(file)
            
            colunas_obrigatorias = ['produto', 'categoria', 'custo_unitario']
            self._validar_colunas(df, colunas_obrigatorias)
            
            registros_processados = 0
            for _, row in df.iterrows():
                try:
                    # Verifica se já existe
                    custo_existente = Custo.query.filter_by(
                        produto=str(row['produto'])
                    ).first()
                    
                    if custo_existente:
                        # Atualiza
                        custo_existente.custo_unitario = float(row['custo_unitario'])
                        custo_existente.data_atualizacao = datetime.utcnow().date()
                    else:
                        # Cria novo
                        custo = Custo(
                            produto=str(row['produto']),
                            categoria=str(row['categoria']),
                            custo_unitario=float(row['custo_unitario']),
                            data_atualizacao=datetime.utcnow().date()
                        )
                        db.session.add(custo)
                    
                    registros_processados += 1
                    
                except Exception as e:
                    current_app.logger.warning(f"Erro ao processar linha: {e}")
                    continue
            
            db.session.commit()
            return registros_processados
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao processar custos: {e}")
    
    def _validar_colunas(self, df, colunas_obrigatorias):
        """Valida se DataFrame possui colunas obrigatórias."""
        colunas_faltantes = set(colunas_obrigatorias) - set(df.columns)
        if colunas_faltantes:
            raise ValueError(
                f"Colunas obrigatórias faltando: {', '.join(colunas_faltantes)}"
            )

