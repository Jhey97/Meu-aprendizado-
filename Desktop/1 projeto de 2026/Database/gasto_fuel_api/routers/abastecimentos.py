import os
import sys
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, status
from sqlalchemy.orm import Session

# Garante que a raiz do projeto (gasto_fuel_api) esteja no topo do sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database import get_db
import models
import schemas
import auth
from services.abastecimento_service import calcular_custo_total, calcular_consumo_medio
router = APIRouter(prefix="/abastecimentos", tags=["Abastecimentos"])

# Diretório base para salvar as fotos enviadas pelo Flutter
UPLOADS_DIR = ROOT_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def salvar_arquivo_local(file: UploadFile, categoria: str) -> str:
    """Salva a foto no diretório de uploads e retorna a URL relativa."""
    extensao = Path(file.filename).suffix or ".jpg"
    nome_arquivo = f"{categoria}_{uuid.uuid4().hex}{extensao}"
    caminho_completo = UPLOADS_DIR / nome_arquivo

    with open(caminho_completo, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/uploads/{nome_arquivo}"


@router.post("/", response_model=schemas.AbastecimentoResponse, status_code=status.HTTP_201_CREATED)
def registrar_abastecimento(
    id_veiculo: int = Form(...),
    odometro: int = Form(...),
    tipo_combustivel: str = Form(...),
    preco_por_litro: float = Form(...),
    litros: float = Form(...),
    foto_placa: Optional[UploadFile] = File(None),
    foto_odometro: Optional[UploadFile] = File(None),
    foto_comprovante: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    usuario_atual: models.Motorista = Depends(auth.obter_usuario_atual)
):
    # 1. Verifica se o veículo existe
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == id_veiculo).first()
    if not veiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Veículo não encontrado."
        )

    # 2. Valida se o odômetro informado é coerente
    if odometro < veiculo.odometro_atual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O odômetro informado ({odometro} km) não pode ser menor que o atual do veículo ({veiculo.odometro_atual} km)."
        )

    # 3. Processa e salva os arquivos de imagem (se enviados)
    url_placa = salvar_arquivo_local(foto_placa, "placa") if foto_placa and foto_placa.filename else None
    url_odometro = salvar_arquivo_local(foto_odometro, "odometro") if foto_odometro and foto_odometro.filename else None
    url_comprovante = salvar_arquivo_local(foto_comprovante, "comprovante") if foto_comprovante and foto_comprovante.filename else None

    # 4. Executa os cálculos do service
    custo_total = calcular_custo_total(
        litros=litros,
        preco_por_litro=preco_por_litro
    )

    consumo_medio = calcular_consumo_medio(
        db=db,
        veiculo_id=id_veiculo,
        odometro_atual=odometro,
        litros_abastecidos=litros
    )

    # 5. Instancia a model com os dados capturados
    novo_abastecimento = models.Abastecimento(
        id_veiculo=id_veiculo,
        id_motorista=usuario_atual.id_motorista,
        odometro=odometro,
        tipo_combustivel=tipo_combustivel,
        preco_por_litro=preco_por_litro,
        litros=litros,
        valor_total=custo_total,
        consumo_medio=consumo_medio,
        foto_placa_url=url_placa,
        foto_odometro_url=url_odometro,
        comprovante_url=url_comprovante
    )

    # 6. Atualiza o odômetro do veículo
    if odometro > veiculo.odometro_atual:
        veiculo.odometro_atual = odometro

    # 7. Persiste no banco de dados
    db.add(novo_abastecimento)
    db.commit()
    db.refresh(novo_abastecimento)

    return novo_abastecimento


@router.get("/", response_model=list[schemas.AbastecimentoResponse])
def listar_abastecimentos(
    db: Session = Depends(get_db),
    usuario_atual: models.Motorista = Depends(auth.obter_usuario_atual)
):
    return db.query(models.Abastecimento).all()