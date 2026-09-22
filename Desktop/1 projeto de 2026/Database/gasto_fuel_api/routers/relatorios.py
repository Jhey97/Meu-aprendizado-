from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db

router = APIRouter()

@router.get("/resumo-geral")
def resumo_geral(db: Session = Depends(get_db)):
    total_gasto_combustivel = db.query(func.sum(models.Abastecimento.valor_total)).scalar() or 0.0
    total_litros = db.query(func.sum(models.Abastecimento.litros)).scalar() or 0.0
    total_veiculos = db.query(models.Veiculo).count()
    total_motoristas = db.query(models.Motorista).count()
    total_aluguel = db.query(func.sum(models.Veiculo.valor_aluguel_mensal)).filter(models.Veiculo.eh_alugado == True).scalar() or 0.0

    return {
        "total_veiculos_cadastrados": total_veiculos,
        "total_motoristas_cadastrados": total_motoristas,
        "gasto_mensal_aluguéis_rs": round(total_aluguel, 2),
        "total_gasto_combustivel_rs": round(total_gasto_combustivel, 2),
        "total_litros_abastecidos": round(total_litros, 2),
        "custo_total_operacional_rs": round(total_gasto_combustivel + total_aluguel, 2)
    }

@router.get("/por-veiculo/{id_veiculo}")
def relatorio_veiculo(id_veiculo: int, db: Session = Depends(get_db)):
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == id_veiculo).first()
    if not veiculo:
        return {"error": "Veículo não encontrado"}

    qtd_abastecimentos = db.query(models.Abastecimento).filter(models.Abastecimento.id_veiculo == id_veiculo).count()
    total_gasto = db.query(func.sum(models.Abastecimento.valor_total)).filter(models.Abastecimento.id_veiculo == id_veiculo).scalar() or 0.0
    total_litros = db.query(func.sum(models.Abastecimento.litros)).filter(models.Abastecimento.id_veiculo == id_veiculo).scalar() or 0.0

    return {
        "placa": veiculo.placa,
        "modelo": veiculo.modelo,
        "odometro_atual": veiculo.odometro_atual,
        "quantidade_abastecimentos": qtd_abastecimentos,
        "total_gasto_rs": round(total_gasto, 2),
        "total_litros": round(total_litros, 2),
        "media_rs_por_litro": round(total_gasto / total_litros, 2) if total_litros > 0 else 0.0
    }