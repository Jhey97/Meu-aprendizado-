from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import auth
import models
import schemas
from database import get_db
from security import get_password_hash

router = APIRouter()

# 1. Cadastrar Motorista
@router.post("/", response_model=schemas.MotoristaResponse, status_code=status.HTTP_201_CREATED)
def criar_motorista(motorista: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    # Verifica se CPF já está cadastrado
    motorista_cpf = db.query(models.Motorista).filter(models.Motorista.cpf == motorista.cpf).first()
    if motorista_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Já existe um motorista cadastrado com este CPF."
        )
    
    # Verifica se E-mail já está cadastrado
    motorista_email = db.query(models.Motorista).filter(models.Motorista.email == motorista.email).first()
    if motorista_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Já existe um motorista cadastrado com este e-mail."
        )

    # Criação do objeto Motorista
    novo_motorista = models.Motorista(
        nome=motorista.nome,
        cpf=motorista.cpf,
        cargo=motorista.cargo,
        email=motorista.email,
        senha_hash=motorista.senha  # Nota: Em produção, aplique um hash (ex: passlib/bcrypt)
    )

    db.add(novo_motorista)
    db.commit()
    db.refresh(novo_motorista)
    return novo_motorista


# 2. Listar Todos os Motoristas
@router.get("/", response_model=List[schemas.MotoristaResponse])
def listar_motoristas(db: Session = Depends(get_db)):
    return db.query(models.Motorista).all()


# 3. Buscar Motorista por ID
@router.get("/{id_motorista}", response_model=schemas.MotoristaResponse)
def buscar_motorista(id_motorista: int, db: Session = Depends(get_db)):
    motorista = db.query(models.Motorista).filter(models.Motorista.id_motorista == id_motorista).first()
    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Motorista não encontrado."
        )
    return motorista


# 4. Atualizar Motorista
@router.put("/{id_motorista}", response_model=schemas.MotoristaResponse)
def atualizar_motorista(
    id_motorista: int, 
    motorista_dados: schemas.MotoristaCreate, 
    db: Session = Depends(get_db)
):
    motorista_db = db.query(models.Motorista).filter(models.Motorista.id_motorista == id_motorista).first()
    if not motorista_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Motorista não encontrado."
        )

    # Atualiza as propriedades
    motorista_db.nome = motorista_dados.nome
    motorista_db.cpf = motorista_dados.cpf
    motorista_db.cargo = motorista_dados.cargo
    motorista_db.email = motorista_dados.email
    if motorista_dados.senha:
        motorista_db.senha_hash = motorista_dados.senha

    db.commit()
    db.refresh(motorista_db)
    return motorista_db


# 5. Deletar Motorista
@router.delete("/{id_motorista}")
def deletar_motorista(id_motorista: int, db: Session = Depends(get_db)):
    motorista_db = db.query(models.Motorista).filter(models.Motorista.id_motorista == id_motorista).first()
    if not motorista_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Motorista não encontrado."
        )

    db.delete(motorista_db)
    db.commit()
    return {"message": f"Motorista ID {id_motorista} removido com sucesso."}

@router.post("/", response_model=schemas.MotoristaResponse, status_code=status.HTTP_201_CREATED)
def criar_motorista(motorista: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    # ... (validações de CPF e Email mantidas) ...

    novo_motorista = models.Motorista(
        nome=motorista.nome,
        cpf=motorista.cpf,
        cargo=motorista.cargo,
        email=motorista.email,
        senha_hash=auth.gerar_hash_senha(motorista.senha)  # Hash gerado com bcrypt
    )

    

    db.add(novo_motorista)
    db.commit()
    db.refresh(novo_motorista)
    return novo_motorista