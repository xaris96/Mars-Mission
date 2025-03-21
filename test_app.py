import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_user(client):
    response = client.post('/add', json={'name': 'John Doe', 'age': 30})
    assert response.status_code == 200
    assert b'User added successfully' in response.data

def test_edit_user(client):
    # Προσθήκη χρήστη για επεξεργασία
    client.post('/add', json={'name': 'Jane Doe', 'age': 25})
    
    # Επεξεργασία του χρήστη
    response = client.post('/edit', json={'id': 1, 'name': 'Jane Smith', 'age': 26})
    assert response.status_code == 200
    assert b'User updated successfully' in response.data

def test_delete_user(client):
    # Προσθήκη χρήστη για διαγραφή
    client.post('/add', json={'name': 'John Doe', 'age': 30})
    
    # Διαγραφή του χρήστη
    response = client.post('/delete', json={'id': 1})
    assert response.status_code == 200
    assert b'User deleted successfully' in response.data
