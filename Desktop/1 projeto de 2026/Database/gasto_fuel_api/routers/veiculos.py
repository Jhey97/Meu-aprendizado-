from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.VeiculoResponse)
def criar_veiculo(veiculo: schemas.VeiculoCreate, db: Session = Depends(get_db)):
    db_veiculo = db.query(models.Veiculo).filter(models.Veiculo.placa == veiculo.placa).first()
    if db_veiculo:
        raise HTTPException(status_code=400, detail="Placa já cadastrada!")
    
    novo_veiculo = models.Veiculo(**veiculo.model_dump())
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    return novo_veiculo

@router.get("/", response_model=List[schemas.VeiculoResponse])
def listar_veiculos(db: Session = Depends(get_db)):
    return db.query(models.Veiculo).all()

@router.get("/{id_veiculo}", response_model=schemas.VeiculoResponse)
def buscar_veiculo(id_veiculo: int, db: Session = Depends(get_db)):
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == id_veiculo).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    return veiculo

@router.put("/{id_veiculo}", response_model=schemas.VeiculoResponse)
def atualizar_veiculo(id_veiculo: int, veiculo_dados: schemas.VeiculoCreate, db: Session = Depends(get_db)):
    veiculo_db = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == id_veiculo).first()
    if not veiculo_db:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    
    for chave, valor in veiculo_dados.model_dump().items():
        setattr(veiculo_db, chave, valor)
        
    db.commit()
    db.refresh(veiculo_db)
    return veiculo_db

@router.delete("/{id_veiculo}")
def deletar_veiculo(id_veiculo: int, db: Session = Depends(get_db)):
    veiculo_db = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == id_veiculo).first()
    if not veiculo_db:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")
    
    db.delete(veiculo_db)
    db.commit()
    return {"message": f"Veículo ID {id_veiculo} removido com sucesso."}