"""
Unit tests for the Mars Mission Flask application.
"""

import sqlite3
import pytest
from app import app, init_db

@pytest.fixture
def client():
    """Fixture for Flask test client."""
    with app.test_client() as client_instance:
        yield client_instance

@pytest.fixture
def setup_database():
    """Fixture for setting up and tearing down the database."""
    init_db()
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # Καθαρισμός μόνο των εγγραφών που δημιουργήθηκαν από τα tests
    cursor.execute("DELETE FROM users WHERE test_data = 1")
    conn.commit()

    yield  # Εκτέλεση του test

    # Καθαρισμός μετά το test
    cursor.execute("DELETE FROM users WHERE test_data = 1")
    conn.commit()
    conn.close()

def test_add_user(client_instance, setup_db):  # noqa: W0613
    """Test adding a user."""
    response = client_instance.post(
        '/add',
        json={'name': 'Test User', 'age': 30, 'test_data': True},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Test User' in response.data

def test_edit_user(client_instance, setup_db):  # noqa: W0613
    """Test editing a user."""
    client_instance.post(
        '/add',
        json={'name': 'Jane Doe', 'age': 25, 'test_data': True}
    )
    response = client_instance.post(
        '/edit',
        json={'id': 1, 'name': 'Jane Smith', 'age': 26},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Jane Smith' in response.data

def test_delete_user(client_instance, setup_db):  # noqa: W0613
    """Test deleting a user."""
    client_instance.post(
        '/add',
        json={'name': 'John Doe', 'age': 30, 'test_data': True}
    )
    response = client_instance.post(
        '/delete',
        json={'id': 1},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'John Doe' not in response.data
