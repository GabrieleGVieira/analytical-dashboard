from typing import List, Dict

from app.domain.entities import SellerPerformance
from app.modules.repositories import SaleRepository, GoalRepository

class SellerRanking:
    def __init__(self, sale_repo: SaleRepository, goal_repo: GoalRepository):
        self.sale_repo = sale_repo
        self.goal_repo = goal_repo

    def run(self, year: int, month: int) -> List[SellerPerformance]:
        sales_data = self.sale_repo.get_sales_summary_by_seller(year, month)
        goals = self.goal_repo.get_goals_for_month(year, month)

        ranking = []
        for row in sales_data:
            margin = self.get_profit_margin(row.total_profit, row.total_sales)
            goal_achieved, target_value = self.get_goal_achieved(row, goals)

            perf = SellerPerformance(
                vendedor=row.seller,
                vendas_totais=float(row.total_sales),
                lucro_total=float(row.total_profit),
                margem_lucro=round(margin, 2),
                quantidade_vendida=int(row.total_quantity),
                meta_batida=round(goal_achieved, 2),
                meta_valor=target_value
            )

            ranking.append(perf)

        return ranking

    @staticmethod
    def get_profit_margin(total_profit, total_sales) -> int:
        return (total_profit / total_sales * 100) if total_sales > 0 else 0
    @staticmethod
    def get_goal_achieved(sale, goals):
        goal = next(
            (g for g in goals if g.categoria == sale.category and g.regiao == sale.region),
            None
        )

        target_value = goal.meta_valor if goal else 0
        goal_achieved = (sale.total_sales / target_value * 100) if target_value > 0 else 0

        return goal_achieved, target_value

