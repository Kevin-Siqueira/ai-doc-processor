import time
from app.celery_app import celery_app
from app.ai_service import gerar_resumo_ia
from app.database import SessionLocal
from app import models

@celery_app.task(name="processar_documento_task", bind=True)
def processar_documento_task(self, texto: str):
    time.sleep(3)
    
    resposta_ia = gerar_resumo_ia(texto)
    task_id = self.request.id

    # Salva o resultado no banco PostgreSQL
    db = SessionLocal()
    try:
        doc = models.DocumentoProcessado(
            task_id=task_id,
            provedor=resposta_ia["provedor"],
            tamanho_original=len(texto),
            resultado=resposta_ia["resultado"]
        )
        db.add(doc)
        db.commit()
    finally:
        db.close()

    return {
        "status": "CONCLUIDO",
        "provedor": resposta_ia["provedor"],
        "tamanho_original": len(texto),
        "resultado": resposta_ia["resultado"]
    }