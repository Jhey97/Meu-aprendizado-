from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados local SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./fuel_control.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa que será herdada em models.py
Base = declarative_base()

# Dependência para abrir e fechar conexões nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()