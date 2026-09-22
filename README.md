# ⛽ Gasto Fuel API - Sistema de Controle de Frota e Abastecimentos

API RESTful desenvolvida em **FastAPI** para o gerenciamento de frotas de veículos, controle de consumo de combustível, registros de motoristas e uploads de comprovantes. O sistema integra-se nativamente com um aplicativo mobile construído em **Flutter**.

---

## 🚀 Funcionalidades Principais

- 🔐 **Autenticação e Segurança:**
  - Login e autenticação via **OAuth2** com suporte a tokens **JWT (JSON Web Tokens)**.
  - Criptografia de senhas utilizando `passlib` e `bcrypt`.

- 👨‍✈️ **Gestão de Motoristas:**
  - Cadastro de motoristas com validação de CPF e e-mail únicos.
  - Perfil do usuário logado (`/auth/me`).

- 🚗 **Gestão de Veículos:**
  - CRUD completo para cadastro e controle da frota de veículos.

- ⛽ **Controle de Abastecimentos:**
  - Registro de abastecimentos com cálculo de custo total e consumo médio.
  - Suporte a upload de até 3 comprovantes/fotos em formato multipart (`foto_placa`, `foto_odometro`, `foto_comprovante`).

- 📊 **Relatórios:**
  - Rotas dedicadas para geração de relatórios de consumo e custos por veículo/período.

---

## 🛠️ Tecnologias Utilizadas

### **Backend (API)**
- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM / Banco de Dados:** SQLAlchemy & SQLite (desenvolvimento)
- **Validação de Dados:** Pydantic (v2)
- **Segurança:** PyJWT / python-jose, Passlib

### **Mobile (App Client)**
- **Framework:** Flutter (Dart)
- **Persistência Local:** `flutter_secure_storage`
- **Comunicação HTTP:** `http` package

---

## 📁 Estrutura do Projeto Backend

```text
gasto_fuel_api/
├── database.py              # Conexão e sessão com o banco SQLite
├── main.py                  # Ponto de entrada da aplicação FastAPI
├── models.py                # Modelos de tabelas SQLAlchemy
├── auth.py                  # Lógica de autenticação e emissão de JWT
├── routers/                 # Endpoints organizados por módulos
│   ├── __init__.py
│   ├── abastecimentos.py
│   ├── motoristas.py
│   ├── relatorios.py
│   └── veiculos.py
├── services/                # Regras de negócio e cálculos
│   └── abastecimento_service.py
└── uploads/                 # Diretório de persistência de imagens/comprovantes
