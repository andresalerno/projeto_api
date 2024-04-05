# 
# Baseado em: https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
#
# Modificado para estudo de casos e uso
#
from flask import Flask, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'EVERYBODY SAY ABOUT THE BIRD'

def check_csv(csv):
    if  csv[-4:] == '.csv':
        return True
    return False

# Global para testes de sucesso e erro
title = ''
cond = ''

@app.route('/', methods=['GET', 'POST'])
def TESTE_CSV():
    global cond
    if request.method == 'POST':
        dados = request.files['dados_csv']

        if dados.filename == '':
            #return redirect('/empty')
            cond = 'VAZIO'
            return redirect(request.url)
        if not check_csv(dados.filename):
            cond = 'INVÁLIDO'
            return redirect(request.url)
        if dados and check_csv(dados.filename): # Redundante com "accept=".csv" " em navegadores modernos
            filename = secure_filename(dados.filename)
            dados.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect('/success')
            flash('test SUCESSO')
            cond = 'SUCESSO'
            #return redirect(request.url)
            return redirect(url_for('TESTE_CSV'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=dados_csv accept=".csv" value=''>
      <input type=submit value=Upload>
    </form>
    <h2>'''+cond+'''</h2>
    '''

@app.route('/success')
def success():
    return '''
    <!doctype html>
    <title>SUCESSO</title>
    <h1>SUCESSO</h1>
    '''

@app.route('/empty')
def empty():
    return '''
    <!doctype html>
    <title>ERRO</title>
    <h1>VAZIO</h1>
    '''
