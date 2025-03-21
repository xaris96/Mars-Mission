import pytest
from app import app
import sqlite3

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_database():
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

def test_add_user(client, setup_database):
    response = client.post('/add', json={'name': 'Test User', 'age': 30, 'test_data': True}, follow_redirects=True)
    assert response.status_code == 200  # Η τελική απάντηση πρέπει να είναι 200
    assert b'Test User' in response.data  # Ελέγχει ότι ο χρήστης εμφανίζεται στη σελίδα index

def test_edit_user(client, setup_database):
    # Προσθήκη χρήστη για επεξεργασία
    client.post('/add', json={'name': 'Jane Doe', 'age': 25, 'test_data': True})

    # Επεξεργασία του χρήστη
    response = client.post('/edit', json={'id': 1, 'name': 'Jane Smith', 'age': 26}, follow_redirects=True)
    assert response.status_code == 200  # Η τελική απάντηση πρέπει να είναι 200
    assert b'Jane Smith' in response.data  # Ελέγχει ότι ο χρήστης ενημερώθηκε στη σελίδα index

def test_delete_user(client, setup_database):
    # Προσθήκη χρήστη για διαγραφή
    client.post('/add', json={'name': 'John Doe', 'age': 30, 'test_data': True})

    # Διαγραφή του χρήστη
    response = client.post('/delete', json={'id': 1}, follow_redirects=True)
    assert response.status_code == 200  # Η τελική απάντηση πρέπει να είναι 200
    assert b'John Doe' not in response.data  # Ελέγχει ότι ο χρήστης δεν εμφανίζεται στη σελίδα index

