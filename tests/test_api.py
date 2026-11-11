from unittest.mock import patch

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "mensagem" in response.json()

def test_enviar_documento_com_sucesso(client):
    # Mock do Celery para não depender do worker rodando durante os testes unitários
    with patch("app.tasks.processar_documento_task.delay") as mock_task:
        mock_task.return_value.id = "test-task-123"
        
        payload = {"texto": "Este é um texto válido com mais de 10 caracteres."}
        response = client.post("/processar-documento", json=payload)
        
        assert response.status_code == 202
        assert response.json()["task_id"] == "test-task-123"
        assert response.json()["status"] == "PENDING"

def test_enviar_documento_texto_curto_falha(client):
    # Deve falhar com 422 por ter menos de 10 caracteres (regra do Pydantic)
    payload = {"texto": "curto"}
    response = client.post("/processar-documento", json=payload)
    assert response.status_code == 422

def test_listar_historico_vazio(client):
    response = client.get("/historico")
    assert response.status_code == 200
    assert response.json() == []