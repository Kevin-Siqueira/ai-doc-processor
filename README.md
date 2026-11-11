# 📄 AI Document Processor API

API REST para processamento assíncrono de documentos e geração de resumos com IA, construída em Python.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** (framework web e documentação OpenAPI)
- **Celery** (processamento de tarefas assíncronas em segundo plano)
- **Redis** (Message Broker e backend de resultados)
- **PostgreSQL** (base de dados relacional via Docker)
- **SQLAlchemy** (ORM)
- **Pydantic** (validação de schemas)
- **Pytest** (testes automatizados com Mocks)

## ⚙️ Funcionalidades

- ⚡ **Resposta Instantânea:** Recebe documentos e devolve `202 Accepted` com `task_id` sem bloquear a thread principal.
- 🤖 **Processamento com IA:** Módulo flexível para análise de texto via LLM / Inteligência Artificial.
- 📊 **Persistência de Histórico:** Armazena todas as análises concluídas no PostgreSQL.
- 🔄 **Consulta de Status:** Polling em tempo real do estado da tarefa (`PENDING`, `EM_PROCESSAMENTO`, `CONCLUIDO`).

## 🛠️ Como Executar o Projeto

1. Clone o repositório:

```bash
git clone [https://github.com/seu-usuario/ai-doc-processor.git](https://github.com/seu-usuario/ai-doc-processor.git)
cd ai-doc-processor
```

Crie e ative o ambiente virtual:

```Bash
python -m venv venv
```
No Windows (PowerShell):

```PowerShell
.\venv\Scripts\Activate.ps1
```
No Linux/Mac:


```Bash
source venv/bin/activate
```
Instale as dependências:

```Bash
pip install -r requirements.txt
```
Suba os containers do Redis e PostgreSQL via Docker:

```Bash
docker-compose up -d
```
Inicie o Worker do Celery (num terminal separado):

```PowerShell
celery -A app.celery_app.celery_app worker --loglevel=info -P threads
```
Inicie a API FastAPI:

```Bash
python -m uvicorn app.main:app --reload
```
Aceda à documentação interativa em: http://127.0.0.1:8000/docs

🧪 Como Executar os Testes
```Bash
pytest
```
