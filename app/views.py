from flask import Flask, render_template, send_file, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import pytz
#nosso
from gerar_grafico import grafico, gerar_tabela
from banco import criar_banco, obter_valores, banco_arduino
#globals
import estaticos as statics

app = Flask(__name__)

@app.route('/')
def main():
    datahora = str(obter_valores(statics.db_est_data_hora, 0))
    data = datahora[8:10]+ "/" +datahora[5:7]
    hora = datahora[11:16]


    dados0 = obter_valores(statics.db_est_um_amb, 0)
    dados1 = obter_valores(statics.db_est_um_solo, 0)
    dados2 = obter_valores(statics.db_est_temp, 0)
    dados3 = obter_valores(statics.db_est_vol_aq, 0)
    print(dados0, dados1, dados2, dados3)


    ante0 = obter_valores(statics.db_est_um_amb, 1)
    ante1 = obter_valores(statics.db_est_um_solo, 1)
    ante2 = obter_valores(statics.db_est_temp, 1)
    ante3 = obter_valores(statics.db_est_vol_aq, 1)
    print(ante0, ante1, ante2, ante3)


    comp0 = statics.zero
    comp1 = statics.zero
    comp2 = statics.zero
    comp3 = statics.zero


    # Zero on 0
    if ante0 != 0:
        comp0 = (statics.data_aprox).format((dados0 / ante0) - 1).replace(".", ",")
    # Zero on 1
    if ante1 != 0:
        comp1 = (statics.data_aprox).format((dados1 / ante1) - 1).replace(".", ",")
    # Zero on 2
    if ante2 != 0:
        comp2 = (statics.data_aprox).format((dados2 / ante2) - 1).replace(".", ",")
    # Zero on 3
    if ante3 != 0:
        comp3 = (statics.data_aprox).format((dados3 / ante3) - 1).replace(".", ",")
    

    
    # 0
    if comp0[statics.zero_rlen:] == statics.zero:
        comp0 = ""
        ico0 = statics.svg_neutro
        res0 = statics.txt_neutro
    elif comp0[0] == '-':
        comp0+="%"
        ico0 = statics.svg_negativo
        res0 = statics.txt_negativo
    else:
        comp0+="%"
        ico0 = statics.svg_positivo
        res0 = statics.txt_positivo

    # 1
    if comp1[statics.zero_rlen:] == statics.zero:
        comp1 = ""
        ico1 = statics.svg_neutro
        res1 = statics.txt_neutro
    elif comp1[0] == '-':
        comp1+="%"
        ico1 = statics.svg_negativo
        res1 = statics.txt_negativo
    else:
        comp1+="%"
        ico1 = statics.svg_positivo
        res1 = statics.txt_positivo

    # 2
    if comp2[statics.zero_rlen:] == statics.zero:
        comp2 = ""
        ico2 = statics.svg_neutro
        res2 = statics.txt_neutro
    elif comp2[0] == '-':
        comp2+="%"
        ico2 = statics.svg_negativo
        res2 = statics.txt_negativo
    else:
        comp2+="%"
        ico2 = statics.svg_positivo
        res2 = statics.txt_positivo

    # 3
    if comp3[statics.zero_rlen:] == statics.zero:
        comp3 = ""
        ico3 = statics.svg_neutro
        res3 = statics.txt_neutro
    elif comp3[0] == '-':
        comp3+="%"
        ico3 = statics.svg_negativo
        res3 = statics.txt_negativo
    else:
        comp3+="%"
        ico3 = statics.svg_positivo
        res3 = statics.txt_positivo


    return render_template('index.html', data=data, hora=hora, dados0=dados0, dados1=dados1, dados2=dados2, dados3=dados3, comp0=comp0, comp1=comp1, comp2=comp2, comp3=comp3, res0=res0, res1=res1, res2=res2, res3=res3, ico0=ico0, ico1=ico1, ico2=ico2, ico3=ico3)

@app.route('/Graficos')
def especific():
    data_inicio = request.args.get('DataInicio')
    data_termino = request.args.get('DataTermino')
    div_html = grafico(statics.db_est_temp, data_inicio, data_termino)
    div_html1 = grafico(statics.db_est_um_solo, data_inicio, data_termino) 
    div_html2 = grafico(statics.db_est_um_amb, data_inicio, data_termino) 
    div_html3 = grafico(statics.db_est_vol_aq, data_inicio, data_termino) 
    return render_template('grafico.html', plotly_div=div_html, plotly_div1=div_html1, plotly_div2=div_html2, plotly_div3=div_html3)

@app.route('/Baixar')
def baixar_relatorio():
    
    opcao = request.args.get('Opcao')
    data_inicio = request.args.get('DataInicio')
    data_termino = request.args.get('DataTermino')
    
    try:
        if opcao == 'periodo':
             # Converte as strings de data para objetos datetime
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_termino = datetime.strptime(data_termino, '%Y-%m-%d')

            # Adiciona um dia ao término
            data_termino += timedelta(days=1)
            gerar_tabela(data_inicio, data_termino, opcao)
            return send_file("./uploads/relatorio.xlsx", as_attachment=True)
        else:
            gerar_tabela('a', 'a', opcao)
            return send_file("./uploads/relatorio.xlsx", as_attachment=True)
        
    except Exception as e:
        return str(e), 500 



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
        criar_banco(filepath)
        return redirect('/')

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json.get('data')
    print(f'Received data: {data}')
    
    try:
        um_solo, um_amb, temperatura, vol_aq = data.split(",")
        # Define o fuso horário local (exemplo para o horário de Brasília)
        local_tz = pytz.timezone('America/Sao_Paulo')
        # Obtém o horário atual com o fuso horário UTC
        utc_now = datetime.now(pytz.utc)
        # Converte para o fuso horário local
        local_now = utc_now.astimezone(local_tz)
        # Formata a data e hora para o formato desejado
        timestamp = local_now.strftime('%Y-%m-%d %H:%M:%S')
        
        banco_arduino(timestamp, float(um_solo), float(um_amb), float(temperatura), float(vol_aq))
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid data format"}), 400
    
    return jsonify({"status": "success"}), 200

