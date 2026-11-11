from pydantic import BaseModel, Field
from typing import Optional, Any

class DocumentoRequest(BaseModel):
    texto: str = Field(..., min_length=10, description="Texto do documento a ser processado pela IA")

class TaskResponse(BaseModel):
    task_id: str
    status: str
    mensagem: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    resultado: Optional[Any] = None