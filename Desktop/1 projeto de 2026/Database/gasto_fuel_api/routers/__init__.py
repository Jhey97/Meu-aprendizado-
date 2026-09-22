import sys
from pathlib import Path

# Garante que a raiz do projeto (gasto_fuel_api) esteja no sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Importa o módulo auth.py da raiz do projeto
import auth

from .abastecimentos import router as abastecimentos_router
from .motoristas import router as motoristas_router
from .relatorios import router as relatorios_router
from .veiculos import router as veiculos_router

# Exporta o router do auth.py renomeado como auth_router
auth_router = auth.router

__all__ = [
    "veiculos_router",
    "abastecimentos_router",
    "relatorios_router",
    "motoristas_router",
    "auth_router",
]