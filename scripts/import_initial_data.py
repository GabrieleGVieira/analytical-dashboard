"""
Script para importar dados iniciais dos CSVs e JSON fornecidos.
"""
import json
import csv
from pathlib import Path
from datetime import datetime
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.infrastructure.database.models import Venda, Custo, Meta


def importar_vendas(app):
    """Importa dados de vendas do CSV."""
    csv_path = Path(__file__).parent.parent / 'data' / 'csv' / 'vendas.csv'
    
    if not csv_path.exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        return 0
    
    print(f"Importando vendas de {csv_path}...")
    
    with app.app_context():
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    valor_total = float(row['quantidade']) * float(row['preco_unitario'])
                    
                    venda = Venda(
                        data=datetime.strptime(row['data'], '%Y-%m-%d').date(),
                        produto=row['produto'],
                        categoria=row['categoria'],
                        quantidade=int(row['quantidade']),
                        preco_unitario=float(row['preco_unitario']),
                        valor_total=valor_total,
                        regiao=row['regiao'],
                        vendedor=row['vendedor']
                    )
                    db.session.add(venda)
                    count += 1
                    
                    if count % 100 == 0:
                        db.session.commit()
                        print(f"  Importados {count} registros...")
                        
                except Exception as e:
                    print(f"  ⚠️  Erro ao importar linha: {e}")
                    continue
        
        db.session.commit()
        print(f"✓ Total de {count} vendas importadas")
        return count


def importar_custos(app):
    """Importa dados de custos do CSV."""
    csv_path = Path(__file__).parent.parent / 'data' / 'csv' / 'custos.csv'
    
    if not csv_path.exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        return 0
    
    print(f"Importando custos de {csv_path}...")
    
    with app.app_context():
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    custo = Custo(
                        produto=row['produto'],
                        categoria=row['categoria'],
                        custo_unitario=float(row['custo_unitario']),
                        data_atualizacao=datetime.strptime(row['data_atualizacao'], '%Y-%m-%d').date()
                    )
                    db.session.add(custo)
                    count += 1
                    
                except Exception as e:
                    print(f"  ⚠️  Erro ao importar linha: {e}")
                    continue
        
        db.session.commit()
        print(f"✓ Total de {count} custos importados")
        return count


def importar_metas(app):
    """Importa dados de metas do JSON."""
    json_path = Path(__file__).parent.parent / 'data' / 'json' / 'metas.json'
    
    if not json_path.exists():
        print(f"❌ Arquivo não encontrado: {json_path}")
        return 0
    
    print(f"Importando metas de {json_path}...")
    
    with app.app_context():
        count = 0
        with open(json_path, 'r', encoding='utf-8') as f:
            metas_data = json.load(f)
            
            for item in metas_data:
                try:
                    meta = Meta(
                        ano=item['ano'],
                        mes=item['mes'],
                        categoria=item['categoria'],
                        regiao=item['regiao'],
                        meta_valor=item['meta_valor'],
                        meta_quantidade=item['meta_quantidade']
                    )
                    db.session.add(meta)
                    count += 1
                    
                    if count % 50 == 0:
                        db.session.commit()
                        print(f"  Importadas {count} metas...")
                    
                except Exception as e:
                    print(f"  ⚠️  Erro ao importar meta: {e}")
                    continue
        
        db.session.commit()
        print(f"✓ Total de {count} metas importadas")
        return count


def main():
    """Função principal."""
    print("=" * 60)
    print("Importando dados iniciais para o banco de dados")
    print("=" * 60)
    
    app = create_app('development')
    
    with app.app_context():
        # Cria tabelas se não existirem
        db.create_all()
        print("✓ Tabelas do banco de dados verificadas\n")
    
    # Importa dados
    total_vendas = importar_vendas(app)
    total_custos = importar_custos(app)
    total_metas = importar_metas(app)
    
    print("\n" + "=" * 60)
    print("Importação concluída!")
    print("=" * 60)
    print(f"  Vendas:  {total_vendas} registros")
    print(f"  Custos:  {total_custos} registros")
    print(f"  Metas:   {total_metas} registros")
    print(f"  Total:   {total_vendas + total_custos + total_metas} registros")


if __name__ == '__main__':
    main()

