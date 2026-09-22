import sys
from pathlib import Path

# 1. Configuração do sys.path (insert no topo para garantir prioridade em subprocessos)
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from database import engine
import models
from routers import (
    abastecimentos_router,
    auth_router,
    motoristas_router,
    relatorios_router,
    veiculos_router,
)

# 2. Criação das tabelas no Banco de Dados
models.Base.metadata.create_all(bind=engine)

# 3. Instância ÚNICA do FastAPI
app = FastAPI(
    title="Gasto Fuel API - Controle de Frota",
    version="1.0.0"
)

# 4. Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Mapeamento de Arquivos Estáticos
uploads_dir = ROOT_DIR / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# 6. Registro das Rotas
app.include_router(auth_router)
app.include_router(veiculos_router)
app.include_router(motoristas_router)
app.include_router(abastecimentos_router)
app.include_router(relatorios_router)


@app.get("/")
def read_root():
    return {"message": "API de Controle de Frota rodando com sucesso!"}


# 7. Execução do Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)