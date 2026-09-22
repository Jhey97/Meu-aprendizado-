from sqlalchemy.orm import Session
from typing import Optional
import models


def calcular_custo_total(litros: float, preco_por_litro: float) -> float:
    """Calcula o valor total do abastecimento."""
    return round(litros * preco_por_litro, 2)


def calcular_consumo_medio(
    db: Session,
    veiculo_id: int,
    odometro_atual: int,
    litros_abastecidos: float
) -> Optional[float]:
    """
    Calcula o consumo médio (km/l) em relação ao último abastecimento
    registrado para o mesmo veículo.
    """
    if litros_abastecidos <= 0:
        return None

    ultimo_abastecimento = (
        db.query(models.Abastecimento)
        .filter(models.Abastecimento.id_veiculo == veiculo_id)
        .order_by(models.Abastecimento.odometro.desc())
        .first()
    )

    if not ultimo_abastecimento or odometro_atual <= ultimo_abastecimento.odometro:
        return None

    km_rodados = odometro_atual - ultimo_abastecimento.odometro
    return round(km_rodados / litros_abastecidos, 2)