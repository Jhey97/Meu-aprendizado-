from typing import Optional
from sqlalchemy.orm import Session
from models import Abastecimento  # Ajuste a importação de acordo com a estrutura do seu projeto


def calcular_custo_total(litros: float, preco_por_litro: float) -> float:
    """
    Calcula o valor total pago no abastecimento (Litros * Preço por Litro).
    """
    if litros <= 0 or preco_por_litro <= 0:
        return 0.0
    return round(litros * preco_por_litro, 2)


def calcular_consumo_medio(
    db: Session,
    veiculo_id: int,
    odometro_atual: float,
    litros_abastecidos: float
) -> Optional[float]:
    """
    Calcula o consumo médio (km/l) com base no histórico do veículo.
    Retorna None caso seja o primeiro abastecimento ou se os dados forem inválidos.
    """
    if litros_abastecidos <= 0:
        return None

    # Busca o último abastecimento registrado para este mesmo veículo
    ultimo_abastecimento = (
        db.query(Abastecimento)
        .filter(Abastecimento.veiculo_id == veiculo_id)
        .order_by(Abastecimento.odometro.desc())
        .first()
    )

    # Se não houver registro anterior ou se o odômetro atual for menor/igual ao anterior
    if not ultimo_abastecimento or odometro_atual <= ultimo_abastecimento.odometro:
        return None

    km_rodados = odometro_atual - ultimo_abastecimento.odometro
    consumo = km_rodados / litros_abastecidos

    return round(consumo, 2)