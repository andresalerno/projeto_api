# importa a classe flask
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# cria uma instancia dessa classe
app = Flask(__name__)

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DATABASE'] = 'db'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_ROOT_PASSWORD'] = 'password'

mysql = MySQL(app)

from app import routes

if __name__ == '__main__':
    app.run(debug=True)