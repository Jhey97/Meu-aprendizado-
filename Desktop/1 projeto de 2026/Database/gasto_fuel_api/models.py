from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Importa apenas a Base vinda do database.py
from database import Base

class Veiculo(Base):
    __tablename__ = "veiculo"

    id_veiculo = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), unique=True, nullable=False)
    modelo = Column(String(50), nullable=False)
    marca = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    tipo_combustivel = Column(String(20), nullable=False)
    eh_alugado = Column(Boolean, default=False)
    valor_aluguel_mensal = Column(Float, default=0.0)
    odometro_atual = Column(Integer, nullable=False, default=0)

class Motorista(Base):
    __tablename__ = "motorista"

    id_motorista = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    cargo = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

class Abastecimento(Base):
    __tablename__ = "abastecimento"

    id_abastecimento = Column(Integer, primary_key=True, index=True)
    id_veiculo = Column(Integer, ForeignKey("veiculo.id_veiculo"), nullable=False)
    id_motorista = Column(Integer, ForeignKey("motorista.id_motorista"), nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)
    odometro = Column(Integer, nullable=False)
    tipo_combustivel = Column(String(20), nullable=False)
    valor_litro = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    litros = Column(Float, nullable=False)
    comprovante_url = Column(String(255), nullable=True)