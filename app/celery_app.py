from celery import Celery
from app.config import REDIS_URL

# Instancia o Celery usando o Redis tanto como Message Broker (fila) quanto como Result Backend (armazenamento de resultados)
celery_app = Celery(
    "doc_processor",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
)