from flask import Flask, render_template, send_from_directory, request, redirect
from gerar_grafico import grafico, gerar_tabela, obter_ultimos_valores
from banco import criar_banco
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def main():
    dados = obter_ultimos_valores("Umidade Ambiente")
    dados1 = obter_ultimos_valores("Umidade solo")
    dados2 = obter_ultimos_valores("Temperatura")
    dados3 = obter_ultimos_valores("Volume Água (L)")
    return render_template('index.html', dados=dados, dados1=dados1, dados2=dados2, dados3=dados3)

@app.route('/Graficos')
def especific():
    div_html = grafico("Temperatura")
    div_html1 = grafico("Umidade solo") 
    div_html2 = grafico("Umidade Ambiente") 
    div_html3 = grafico("Volume Água (L)") 
    return render_template('grafico.html', plotly_div=div_html, plotly_div1=div_html1, plotly_div2=div_html2, plotly_div3=div_html3)


@app.route('/Baixar', methods=['GET', 'POST'])
def tabela():
    gerar_tabela()
    return send_from_directory(directory='static', path='relatorio.xlsx', as_attachment=True) 

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/Importar', methods=['GET', 'POST'])
def upload_file():
    if 'arquivo_csv' not in request.files:
        print("Arquivo não encontrado")
        return redirect(request.url)
    file = request.files['arquivo_csv']
    if file.filename == '':
        print("Nenhum arquivo selecionado")
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"Arquivo salvo em: {filepath}")
        criar_banco()
        return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)