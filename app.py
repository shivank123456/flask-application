#!python

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3,os
from sqlite3 import Error

app = Flask(__name__)

# Configuration
DATABASE = 'database.db'
TABLE_NAME = 'tasks'


# Create a table to store tasks if it doesn't exists
def create_table():
    try:
        conn = sqlite3.connect(DATABASE)
        print(sqlite3.version)
        print(conn)
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               title TEXT NOT NULL, 
               description TEXT, 
               status INTEGER DEFAULT 0);''')
    except Error as e:
        print(e)

    conn.close()


create_table()


# Home page — Display tasks

def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        flash('wrong username and password!')
        return home()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {TABLE_NAME}')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return index()
        else:
            return render_template('login.html')
    else:
        return home()
# Add new task
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {TABLE_NAME} (title, description) VALUES (?, ?)', (title, description))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return home()


# Update task status
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE {TABLE_NAME} SET title=?, description=? WHERE id=?', (title,description, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return home()
@app.route('/edit/<int:task_id>/<string:title>/<string:description>', methods=['GET', 'POST'])
def edit_page(task_id,title,description):
    return render_template('update.html', task_id=task_id,title=title,description=description)

# Delete task
@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {TABLE_NAME} WHERE id=?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8010, host='0.0.0.0')
