from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


# --- SCHEMAS DE VEÍCULO ---
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    marca: str
    ano: int
    tipo_combustivel: str
    eh_alugado: bool = False
    valor_aluguel_mensal: float = 0.0
    odometro_atual: int = 0

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoResponse(VeiculoBase):
    id_veiculo: int
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS DE MOTORISTA ---
class MotoristaBase(BaseModel):
    nome: str
    cpf: str
    cargo: str
    email: EmailStr

class MotoristaCreate(MotoristaBase):
    senha: str

class MotoristaResponse(MotoristaBase):
    id_motorista: int
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS DE ABASTECIMENTO ---
class AbastecimentoBase(BaseModel):
    id_veiculo: int
    odometro: int
    tipo_combustivel: str
    preco_por_litro: float  # Padronizado com o cálculo do backend
    litros: float
    comprovante_url: Optional[str] = None
    foto_placa_url: Optional[str] = None
    foto_odometro_url: Optional[str] = None

class AbastecimentoCreate(AbastecimentoBase):
    # Opcional na criação, pois o id_motorista é capturado via Token JWT no backend
    id_motorista: Optional[int] = None

class AbastecimentoResponse(AbastecimentoBase):
    id_abastecimento: int
    id_motorista: int
    valor_total: float       # Retornado após o cálculo do backend
    consumo_medio: Optional[float] = None  # Calculado em km/l (None no 1º abastecimento)
    data_hora: datetime
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS DE AUTENTICAÇÃO ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None