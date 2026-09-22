from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
from database import get_db
import models
import schemas

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. Busca o motorista pelo e-mail
    motorista = db.query(models.Motorista).filter(models.Motorista.email == form_data.username).first()
    
    # 2. Valida usuário e hash da senha
    if not motorista or not auth.verificar_senha(form_data.password, motorista.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Gera o Token de Acesso JWT
    access_token = auth.criar_token_acesso(data={"sub": motorista.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }