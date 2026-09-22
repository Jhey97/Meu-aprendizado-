from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Motorista

# --- CONFIGURAÇÕES E SEGURANÇA ---

SECRET_KEY = "sua_chave_secreta_aqui_para_desenvolvimento"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Esquema OAuth2 para documentação do Swagger e extração do Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- FUNÇÕES UTILITÁRIAS DE SENHA E TOKEN ---

def verificar_senha(senha_plana: str, senha_hashed: str) -> bool:
    if not senha_hashed:
        return False
    try:
        return pwd_context.verify(senha_plana, senha_hashed)
    except Exception:
        return False


def get_password_hash(senha: str) -> str:
    return pwd_context.hash(senha)


def criar_token_acesso(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- SCHEMAS PYDANTIC ---

class UserCreate(BaseModel):
    nome: str
    cpf: str
    cargo: str
    email: str
    password: str


class UserResponse(BaseModel):
    # 'validation_alias' faz o Pydantic procurar por 'id_motorista' ou 'id' no objeto SQLAlchemy
    id: Optional[int] = Field(default=None, validation_alias="id_motorista")
    nome: str
    cpf: str
    cargo: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# --- DEPENDÊNCIA DE AUTENTICAÇÃO ---

def obter_usuario_atual(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Motorista:
    exception_unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception_unauthorized
    except JWTError:
        raise exception_unauthorized

    user = db.query(Motorista).filter(Motorista.email == username).first()
    if user is None:
        raise exception_unauthorized

    return user


# --- ROTAS DE AUTENTICAÇÃO ---

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Validação de e-mail duplicado
    if db.query(Motorista).filter(Motorista.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    # 2. Validação de CPF duplicado
    if db.query(Motorista).filter(Motorista.cpf == user.cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado.",
        )

    # 3. Hash da senha e persistência
    hashed_password = get_password_hash(user.password)
    new_user = Motorista(
        nome=user.nome,
        cpf=user.cpf,
        cargo=user.cargo,
        email=user.email,
        senha_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Motorista cadastrado com sucesso!",
        "email": new_user.email,
    }


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # 1. Busca motorista pelo e-mail
    user = db.query(Motorista).filter(Motorista.email == form_data.username).first()

    # 2. Valida existência do usuário e compara a senha
    if not user or not verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha incorretos.",
        )

    # 3. Emite o Token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(usuario_atual: Motorista = Depends(obter_usuario_atual)):
    """
    Retorna os dados do usuário autenticado no token Bearer enviado na requisição.
    """
    return usuario_atual