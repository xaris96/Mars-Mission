from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_path = "db.sqlite3"

# Database Setup
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
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
def add_user(name, age):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
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
    name = request.form['name']
    age = request.form['age']
    add_user(name, age)
    return redirect(url_for('index'))

#Edit User
@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        update_user(id, name, age)
        return redirect(url_for('index'))
    #prefill the form with user data
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

#Delete User
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    delete_user(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
