from database import SessionLocal
import models

def cadastrar_dados_iniciais():
    db = SessionLocal()
    try:
        # Criando um veículo de teste
        veiculo_teste = models.Veiculo(
            placa="XYZ9876",
            modelo="Corolla",
            marca="Toyota",
            ano=2024,
            tipo_combustivel="Flex",
            eh_alugado=True,
            valor_aluguel_mensal=2500.0,
            odometro_atual=5000
        )
        
        db.add(veiculo_teste)
        db.commit()
        db.refresh(veiculo_teste)
        print(f"Veículo cadastrado com sucesso! ID: {veiculo_teste.id_veiculo}")

    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cadastrar_dados_iniciais()