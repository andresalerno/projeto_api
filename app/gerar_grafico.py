import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from datetime import datetime, timedelta
#nosso
#globals
import estaticos as statics




def grafico(dado, data_inicio=None, data_termino=None):
    try:
        if not data_inicio or not data_termino:
            data_termino = datetime.now()
            data_inicio = data_termino - timedelta(days=7)
            data_inicio = data_inicio.strftime('%Y-%m-%d')
            data_termino = data_termino.strftime('%Y-%m-%d')
        
        conn = mysql.connector.connect(
            host=statics.host,
            database=statics.database,
            user=statics.username,
            password=statics.password
        )
        if conn.is_connected():
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_termino_obj = datetime.strptime(data_termino, '%Y-%m-%d')
            data_termino_obj += timedelta(days=1)
            data_inicio = data_inicio_obj.strftime('%Y-%m-%d')
            data_termino = data_termino_obj.strftime('%Y-%m-%d')
            
            query = f"SELECT * FROM `{statics.table}` WHERE `{statics.db_est_data_hora}` BETWEEN %s AND %s"
            data = pd.read_sql(query, conn, params=[data_inicio, data_termino])
            data.sort_values(by=statics.db_est_data_hora, inplace=True)  # Sorting data
            
            # Tratamento de valores nulos
            data[dado].fillna(method='ffill', inplace=True)  # Preenche os valores nulos com o último valor válido

            if dado not in data.columns:
                raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
            
            y = data[dado].to_list()
            x = data[statics.db_est_data_hora].tolist()
            
            nome_y = ""
            title = ""
            if dado == statics.db_est_temp:
                nome_y = statics.uni_temp
                title = statics.txt_title_temp
            elif dado == statics.db_est_um_solo:
                nome_y = statics.uni_um_solo
                title = statics.txt_title_um_solo
            elif dado == statics.db_est_um_amb:
                nome_y = statics.uni_um_amb
                title = statics.txt_title_um_amb
            else:
                nome_y = statics.uni_vol_aq
                title = statics.txt_title_vol_aq
                
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name=dado, line=dict(color='#2e5725')))
            
            fig.update_layout(
                xaxis_title='Data e Hora',
                yaxis_title=nome_y,
                title=title,
                margin=dict(l=20, r=20, t=50, b=20),
                autosize=True,
                plot_bgcolor='white',
                font=dict(
                    family='Poppins',
                    size=12,
                    color='black'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgray',
                    gridwidth=1,
                )
            )

            config = {'responsive': True, 'modeBarButtonsToRemove': ['resetScale2d'], 'displaylogo': False}
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



def gerar_tabela(data_inicio, data_termino, opcao):
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
            if opcao == 'periodo':
                # Carregar dados diretamente em um DataFrame do pandas
                query = f"SELECT * FROM `{statics.table}` WHERE `{statics.db_est_data_hora}` BETWEEN %s AND %s"
                data = pd.read_sql(query, conn, params=[data_inicio, data_termino])
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
            else:
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