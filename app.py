from flask import Flask, render_template
import plotly.graph_objects as go
import plotly.io as pio
from gerar_grafico import grafico

app = Flask(__name__)

@app.route('/')
def plotly_chart():
    div_html = grafico("Temperatura")
    div_html1 = grafico("Umidade solo") 
    div_html2 = grafico("Umidade Ambiente") 
    div_html3 = grafico("Volume Água (L)") 
    return render_template('index.html', plotly_div=div_html, plotly_div1=div_html1, plotly_div2=div_html2, plotly_div3=div_html3)

if __name__ == '__main__':
    app.run(debug=True)