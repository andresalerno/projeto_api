from flask import Flask, render_template, send_from_directory, request, redirect

from gerar_grafico import grafico, gerar_tabela, obter_ultimos_valores
from Classes.RegisterClass import Register

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def main():

    if request.method == "POST":
        csv_recebido = request.files['arquivo_csv']
        if Register.check_csv(csv_recebido.filename):
            redirect("/")
        csv_recebido = str(csv_recebido.read().decode())
        Register.setup_list(csv_recebido)


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


@app.route('/Baixar', methods=['GET'])
def tabela():
    gerar_tabela()
    return send_from_directory(directory='static', path='relatorio.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)