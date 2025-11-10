from dataclasses import dataclass, field


@dataclass
class SellerPerformance:
    """Representa as métricas de performance de um vendedor."""
    vendedor: str
    vendas_totais: float
    lucro_total: float
    margem_lucro: float
    quantidade_vendida: int
    meta_batida: float
    meta_valor: int
    indice_performance: float = field(init=False)

    def __post_init__(self):
        peso_lucro = 0.4
        peso_meta = 0.4
        peso_margem = 0.2

        score = (
                        (min(self.lucro_total / 10000, 1) * peso_lucro)
                        + (min(self.meta_batida / 100, 1) * peso_meta)
                        + (min(self.margem_lucro / 100, 1) * peso_margem)
                ) * 100

        self.indice_performance = round(score, 2)
    def to_dict(self) -> dict:
        """
        Serializa o objeto para JSON-friendly dict.
        """
        return {
            "vendedor": self.vendedor,
            "vendas_totais": self.vendas_totais,
            "lucro_total": self.lucro_total,
            "margem_lucro": self.margem_lucro,
            "quantidade_vendida": self.quantidade_vendida,
            "meta_batida": self.meta_batida,
            "indice_performance": self.indice_performance,
        }
