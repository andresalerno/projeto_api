import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
#nosso
#globals
import estaticos as statics




def grafico(dado):
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host=statics.host,
            database=statics.database,
            user=statics.username,
            password=statics.password
        )
        if conn.is_connected():
            print('Conectado ao banco de dados MySQL')

            # Carregar dados diretamente em um DataFrame do pandas
            query = f"SELECT * FROM `{statics.table}`"
            data = pd.read_sql(query, conn)

            if dado not in data.columns:
                print("Colunas disponíveis no DataFrame:", data.columns.tolist())
                raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
            

            # ANTIGO -- JÁ MANIPULADO NA ENTRADA DOS DADOS
            # Conversão de valores, se necessário - Pois não aceita ','
            #if dado == 'Temperatura':
            #    data[dado] = data[dado].str.replace(',', '.').astype(float)
            #elif dado == 'Volume Água (L)':
            #    data[dado] = pd.to_numeric(data[dado].str.replace(',', '.'), errors='coerce')

            # ANTIGO -- JÁ FEITO AO ENVIAR PARA O BANCO
            # data = data.sort_values(by=statics.db_est_data_hora).set_index(statics.db_est_data_hora)
            # # Filtrar os dados para ter entradas com pelo menos 10 minutos de diferença
            # data_filtrada = data[~(data.index.to_series().diff() < pd.Timedelta('10min'))]
            
            # Selecionar os dados da coluna desejada
            y = data[dado].to_list()
            x = data[statics.db_est_data_hora].tolist()  # Usar o índice Data_Hora como eixo x
            
            nome_y = ""
            title = ""
            if dado == statics.db_est_temp:
                nome_y = statics.txt_title_temp
                title = statics.txt_title_temp
            elif dado == statics.db_est_um_solo:
                nome_y = statics.txt_title_um_solo
                title = statics.txt_title_um_solo
            elif dado == statics.db_est_um_amb:
                nome_y = statics.txt_title_um_amb
                title = statics.txt_title_um_amb
            else:
                nome_y = statics.txt_title_vol_aq
                title = statics.txt_title_vol_aq
                
            # Criação do gráfico
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name=dado, line=dict(color='#2e5725')))
            
            fig.update_xaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo X
            fig.update_yaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo Y

            fig.update_layout(
                xaxis_title='Data e Hora',
                yaxis_title=nome_y,
                title=title,
                margin=dict(l=20, r=20, t=50, b=20),  # Margens menores para aumentar a área de plotagem
                autosize=True,
                plot_bgcolor='white',
                    font=dict(
                    family='Poppins',  # Definir a família da fonte global do gráfico
                    size=12,        # Definir o tamanho da fonte global do gráfico
                    color='black'   # Definir a cor do texto global do gráfico
                ),
                yaxis=dict(
                    showgrid=True,  # Exibir linhas de grade no eixo Y
                    gridcolor='lightgray',  # Cor das linhas de grade no eixo Y
                    gridwidth=1,  # Largura das linhas de grade no eixo Y
                )
            )

            config = {'displayModeBar': False, 'responsive': True}
            div_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)
            return div_html

    except Error as e:
        print(f"{statics.txt_err_sql_conn}: \n> {e}")
    except Exception as ex:
        print(f"{statics.txt_err_sql_proc}: \n> {ex}")
    finally:
        if conn.is_connected():
            conn.close()
            print(statics.txt_sql_conn_end)



def gerar_tabela():
    try:
        # Conexão com o banco de dados MySQL
        conn = mysql.connector.connect(
            host=statics.host,
            database=statics.database,
            user=statics.username,
            password=statics.password
        )
        if conn.is_connected():
            print(statics.txt_sql_conn_init)
            # Carregar dados diretamente em um DataFrame do pandas
            query = f"SELECT * FROM `{statics.table}`"
            data = pd.read_sql(query, conn)
            print(data)

            data[statics.csv_data] = data[statics.db_est_data_hora].apply(str).str.slice(stop=10)
            data[statics.csv_hora] = data[statics.db_est_data_hora].apply(str).str.slice(start=11, stop=16)
            data = data.drop(columns=[statics.db_est_data_hora])

            data = data.rename(columns={
                    statics.db_est_um_solo : statics.csv_um_solo, 
                    statics.db_est_um_amb : statics.csv_um_amb,
                    statics.db_est_temp : statics.csv_temp,
                    statics.db_est_vol_aq : statics.csv_vol_aq 
                })

            data = data[[
                statics.csv_data,
                statics.csv_hora,
                statics.csv_um_solo, 
                statics.csv_um_amb,
                statics.csv_temp,
                statics.csv_vol_aq 
                ]]

            print(data)
            # Geração do arquivo Excel sem incluir 'Data_Hora' como índice
            data.to_excel("./uploads/relatorio.xlsx", index=False)     
            
    except Error as e:
        print(f"{statics.txt_err_sql_conn}: \n> {e}")
    except Exception as ex:
        print(f"{statics.txt_err_sql_proc}: \n> {ex}")
    finally:
        if conn.is_connected():
            conn.close()
            print(statics.txt_sql_conn_end)