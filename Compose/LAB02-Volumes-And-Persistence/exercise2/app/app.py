from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres-db",
        database="persistence_demo",
        user="dbuser",
        password="example"
    )
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC;')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (title, content) VALUES (%s, %s);',
                (title, content))
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_note(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s;', (id,))
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Wait for the database to be ready
    time.sleep(2)
    app.run(host='0.0.0.0', port=8080, debug=True) 