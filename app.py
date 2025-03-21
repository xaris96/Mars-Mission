"""
Mars Mission Application
This application manages users for the Mars Mission project.
"""

import sqlite3  # Standard library imports
from flask import Flask, request, jsonify, render_template, redirect, url_for  # Third-party imports

# Initialize Flask application
app = Flask(__name__)

# Database file path
DB_PATH = "db.sqlite3"

# Database Setup
def init_db():
    """Initialize the database and create the users table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            test_data BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Get all users
def get_users():
    """Retrieve all users from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Add a user
def add_user(name, age, test_data=False):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, test_data) VALUES (?, ?, ?)",
        (name, age, test_data))
    conn.commit()
    conn.close()

# Update a user
def update_user(user_id, name, age):
    """Update an existing user's information in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, user_id))
    conn.commit()
    conn.close()

# Delete a user
def delete_user(user_id):
    """Delete a user from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Home Page
@app.route('/')
def index():
    """Render the index page with a list of users."""
    return render_template('index.html', users=get_users())

# Add User
@app.route('/add', methods=['POST'])
def add():
    """Handle adding a new user via JSON or form data."""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        test_data = data.get('test_data', False)  # Default to False if not provided
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        test_data = False  # Not supported via forms

    if not name or not age:
        return jsonify({'error': 'Invalid data'}), 400

    add_user(name, age, test_data)
    return redirect(url_for('index'))

# Edit User
@app.route('/edit', methods=['POST'])
def edit():
    """Handle editing an existing user via JSON or form data."""
    if request.is_json:
        data = request.get_json()
        user_id = data.get('id')
        name = data.get('name')
        age = data.get('age')
    else:
        user_id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')

    if not user_id or not name or not age:
        return jsonify({'error': 'Invalid data'}), 400

    update_user(user_id, name, age)
    return redirect(url_for('index'))

# Delete User
@app.route('/delete', methods=['POST'])
def delete():
    """Handle deleting a user via JSON or form data."""
    if request.is_json:
        data = request.get_json()
        user_id = data.get('id')
    else:
        user_id = request.form.get('id')

    if not user_id:
        return jsonify({'error': 'Invalid data'}), 400

    delete_user(user_id)
    return redirect(url_for('index'))

# Add User Form
@app.route('/add-form', methods=['GET'])
def add_form():
    """Render the form for adding a new user."""
    return render_template('add.html')

# Edit User Form
@app.route('/edit-form/<int:user_id>', methods=['GET'])
def edit_form(user_id):
    """Render the form for editing an existing user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

# Main entry point
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
