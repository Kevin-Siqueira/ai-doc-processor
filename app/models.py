from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class DocumentoProcessado(Base):
    __tablename__ = "documentos_processados"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), unique=True, index=True, nullable=False)
    provedor = Column(String(100), nullable=False)
    tamanho_original = Column(Integer, nullable=False)
    resultado = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)