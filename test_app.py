# Teste automatizado usando Flask test_client()

import pytest
from app import app

# Fixture do client
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Lista glogal para guardar ID das tarefas
tasks_ids = []

# Teste - Criar tarefa
def test_create_task(client):
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }
    response = client.post('/tasks', json=new_task_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    tasks_ids.append(1)  # ID fixo já que é a primeira 
    
# Teste - Obter todas as tarefas
def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert "total_tasks" in data
    assert isinstance(data["tasks"], list)

# Teste - Obter uma tarefa especifica
def test_get_task(client):
    task_id = tasks_ids[0]
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == task_id

# Teste - Atualizar tarefa
def test_update_task(client):
    task_id = tasks_ids[0]
    payload = {
        "title": "Título atualizado",
        "description": "Nova descrição",
        "completed": True
    }
    response = client.put(f'/tasks/{task_id}', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

    # Verifica se os dados foram realmente atualizados
    response = client.get(f'/tasks/{task_id}')
    updated_task = response.get_json()
    assert updated_task["title"] == payload["title"]
    assert updated_task["description"] == payload["description"]
    assert updated_task["completed"] == payload["completed"]

# Teste - Deletar tarefa
def test_delete_task(client):
    task_id = tasks_ids[0]
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data

    # Verifica se a tarefa foi removida
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 404
