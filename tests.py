# Testes utilizando o Postman

import pytest
import requests

# CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

# Teste - Criar Tarefas
def test_creat_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }
    response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "in" in response_json
    tasks.append(response_json['id'])
    
# Teste - Obter tarefa
def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

# Teste Obter tarefa especifica
def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = response.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']
        
# Teste - Atualizar tarefa
def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": 'Nova descriçao',
            "title": 'Título atualizado'
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)
        response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        
        # Nova requisição a tarefa especifica
        response = response.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]

# Teste - Deletar Tarefa        
def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        response.status_code == 200

        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404
       