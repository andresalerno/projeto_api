from app import app
from flask import render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from . import mysql

@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM task")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', db='task')

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        description = request.form['description']
        due_date = request.form['due_date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO task (description, due_date) VALUES (%s, %s)", (description, due_date))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))