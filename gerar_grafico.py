import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Configuração do banco de dados
username = 'root'
password = 'fatec'
host = 'localhost'
database = 'estufa'

def grafico(dado):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )
        if conn.is_connected():
            print('Conectado ao banco de dados MySQL')

            # Carregar dados diretamente em um DataFrame do pandas
            query = f"SELECT * FROM estufa"
            data = pd.read_sql(query, conn)

            if dado not in data.columns:
                print("Colunas disponíveis no DataFrame:", data.columns.tolist())
                raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
            
            # Conversão de valores, se necessário - Pois não aceita ','
            if dado == 'Temperatura':
                data[dado] = data[dado].str.replace(',', '.').astype(float)
            elif dado == 'Volume Água (L)':
                data[dado] = pd.to_numeric(data[dado].str.replace(',', '.'), errors='coerce')

            # ANTIGO -- JÁ FEITO AO ENVIAR PARA O BANCO
            # data = data.sort_values(by='Data_Hora').set_index('Data_Hora')
            # # Filtrar os dados para ter entradas com pelo menos 10 minutos de diferença
            # data_filtrada = data[~(data.index.to_series().diff() < pd.Timedelta('10min'))]
            
            # Selecionar os dados da coluna desejada
            y = data[dado].to_list()
            x = data.index.tolist()  # Usar o índice Data_Hora como eixo x
            
            nome_y = ""
            if dado == "Temperatura":
                nome_y = "Temperatura °C"
            elif dado == "Umidade solo":
                nome_y = "Umidade solo %"
            elif dado == "Umidade Ambiente":
                nome_y = "Umidade ambiente %"
            else:
                nome_y = "Volume água (ml)"
                
            # Criação do gráfico
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name=dado, line=dict(color='#2e5725')))
            
            fig.update_xaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo X
            fig.update_yaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo Y

            fig.update_layout(
                xaxis_title='Data e Hora',
                yaxis_title=nome_y,
                margin=dict(l=20, r=20, t=20, b=20),  # Margens menores para aumentar a área de plotagem
                autosize=True
            )

            config = {'displayModeBar': False, 'responsive': True}
            div_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)
            return div_html

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    except Exception as ex:
        print(f"Erro ao processar os dados: {ex}")
    finally:
        if conn.is_connected():
            conn.close()
            print('Conexão ao MySQL encerrada')

def obter_ultimos_valores(dado, default_value=0):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )
        if conn.is_connected():
            print('Conectado ao banco de dados MySQL')

            # Preparar a consulta SQL para pegar o último valor da coluna especificada
            query = f"SELECT `{dado}` FROM estufa ORDER BY Data_Hora DESC LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return result[-1]  # Retorna o último valor
            else:
                return default_value  # Retorna o valor padrão se não houver dados
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return default_value
    except Exception as ex:
        print(f"Erro ao processar os dados: {ex}")
        return default_value
    finally:
        if conn and conn.is_connected():
            conn.close()
            print('Conexão ao MySQL encerrada')

def gerar_tabela():
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )
        if conn.is_connected():
            # Carregar dados diretamente em um DataFrame do pandas
            query = f"SELECT * FROM estufa"
            data = pd.read_sql(query, conn)
            print(data)
            # Geração do arquivo Excel sem incluir 'Data_Hora' como índice
            data.to_excel("./static/relatorio.xlsx", index=False)     
            
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    except Exception as ex:
        print(f"Erro ao processar os dados: {ex}")
    finally:
        if conn.is_connected():
            conn.close()
            print('Conexão ao MySQL encerrada')