from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_path = "db.sqlite3"

# Database Setup
def init_db():
    conn = sqlite3.connect("db.sqlite3")
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
#Get all users
def get_users():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


#Add a user
def add_user(name, age, test_data=False):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, test_data) VALUES (?, ?, ?)", (name, age, test_data))
    conn.commit()
    conn.close()

#Update a user
def update_user(id, name, age):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, id))
    conn.commit()
    conn.close()

# Delete a user
def delete_user(id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#Home Page
@app.route('/')
def index():
    return render_template('index.html', users=get_users())

#Add User

@app.route('/add', methods=['POST'])
def add():
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        test_data = data.get('test_data', False)  # Προεπιλογή False αν δεν παρέχεται
    else:
        name = request.form['name']
        age = request.form['age']
        test_data = False  # Δεν υποστηρίζεται από φόρμες

    if not name or not age:
        return jsonify({'error': 'Invalid data'}), 400

    add_user(name, age, test_data)
    return redirect(url_for('index'))

#Edit User
@app.route('/edit', methods=['POST'])
def edit():
    if request.is_json:
        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        age = data.get('age')
    else:
        id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')

    if not id or not name or not age:
        return jsonify({'error': 'Invalid data'}), 400

    update_user(id, name, age)
    return redirect(url_for('index'))

#Delete User
@app.route('/delete', methods=['POST'])
def delete():
    if request.is_json:
        data = request.get_json()
        id = data.get('id')
    else:
        id = request.form.get('id')

    if not id:
        return jsonify({'error': 'Invalid data'}), 400

    delete_user(id)
    return redirect(url_for('index'))

# Add User Form
@app.route('/add-form', methods=['GET'])
def add_form():
    return render_template('add.html')

# Edit User Form
@app.route('/edit-form/<int:id>', methods=['GET'])
def edit_form(id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
