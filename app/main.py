from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from typing import List

from app.schemas import DocumentoRequest, TaskResponse, TaskStatusResponse
from app.tasks import processar_documento_task
from app.celery_app import celery_app
from app.database import engine, Base, get_db
import app.models as models

# Cria as tabelas na base de dados PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Processor API",
    description="API para processamento assíncrono de documentos e resumos com IA",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"mensagem": "API de Processamento de Documentos com IA está rodando!"}

@app.post("/processar-documento", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def enviar_documento(payload: DocumentoRequest):
    task = processar_documento_task.delay(payload.texto)
    return TaskResponse(
        task_id=task.id,
        status="PENDING",
        mensagem="Documento enviado para a fila de processamento com sucesso."
    )

@app.get("/status/{task_id}", response_model=TaskStatusResponse)
def consultar_status_tarefa(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == "PENDING":
        return TaskStatusResponse(task_id=task_id, status="EM_PROCESSAMENTO", resultado=None)
    elif task_result.state == "SUCCESS":
        return TaskStatusResponse(task_id=task_id, status="CONCLUIDO", resultado=task_result.result)
    elif task_result.state == "FAILURE":
        return TaskStatusResponse(task_id=task_id, status="ERRO", resultado={"erro": str(task_result.info)})
    
    return TaskStatusResponse(task_id=task_id, status=task_result.state, resultado=None)

@app.get("/historico")
def listar_historico(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Lista o histórico de resumos processados salvos no PostgreSQL.
    """
    documentos = db.query(models.DocumentoProcessado).offset(skip).limit(limit).all()
    return documentos