from sqlalchemy import create_engine, MetaData, Table
import datetime 
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from sqlalchemy.types import DateTime
#nosso
#globals
import estaticos as statics

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=statics.host,
            database=statics.database,
            user=statics.username,
            password=statics.password
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def criar_banco(file_path):
    try:
        # Conexão com o banco de dados MySQL
        engine = create_engine(f'mysql+pymysql://{statics.username}:{statics.password}@{statics.host}/{statics.database}')

        # Caminho do arquivo CSV
        #file_path = "./uploads/Dados.csv"

        # Carregar dados do CSV
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

            #datahora = 'Data_Hora'
            datahora = statics.db_est_data_hora

            # Garantir que a coluna de data/hora esteja no formato datetime
            df[datahora] = pd.to_datetime(df[statics.csv_data] + ' ' + df[statics.csv_hora], dayfirst=True, errors='coerce')
            df = df.dropna(subset=[datahora])
            
            # Ordenar os dados por Data_Hora antes de definir como índice
            df = df.sort_values(by=datahora).set_index(datahora)
            
            # Excluir as colunas desnecessárias
            df = df.drop(columns=[statics.csv_dia, statics.csv_data, statics.csv_hora])


            print(df)
            # Manipula dados de Temperatura: String -> 
            df[statics.csv_temp] = df[statics.csv_temp].astype(str)
            df[statics.csv_temp] = df[statics.csv_temp].str.replace(',','.').apply(float)

            # Manipula dados de Volume de Água: : String -> Float
            df[statics.csv_vol_aq] = df[statics.csv_vol_aq].astype(str)
            df[statics.csv_vol_aq] = df[statics.csv_vol_aq].str.replace(',','.').apply(float)



            # Renomear as colunas para um padrão de boas práticas em SQL
            df = df.rename(columns={
                    statics.csv_um_solo : statics.db_est_um_solo,
                    statics.csv_um_amb : statics.db_est_um_amb,
                    statics.csv_temp : statics.db_est_temp,
                    statics.csv_vol_aq : statics.db_est_vol_aq
                })

            print(df)
            # Filtrar os dados para ter entradas com pelo menos 10 minutos de diferença
            data_filtrada = df[~(df.index.to_series().diff() < pd.Timedelta('10min'))]
            
            dtype = {
                datahora: DateTime,
            }

            # Inserir dados no MySQL
            data_filtrada.reset_index(inplace=True)
            data_filtrada.to_sql(statics.table, con=engine, if_exists='append', index=False, dtype=dtype)

            #meta = MetaData(bind=engine)
            #alter_estufa = Table(statics.table, meta, autoload=True)
            #alter_estufa.c.


            

            # Excluir o arquivo após inserção no banco de dados
            os.remove(file_path)
            print("Arquivo CSV excluído com sucesso.")
        else:
            print("Erro: Arquivo CSV não encontrado.")

    except Exception as e:
        print(f"Erro durante o processo: \n> {e}")
 
def banco_arduino(timestamp, um_solo, um_amb, temperatura, vol_aq):
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Estufa VALUES (%s, %s, %s, %s, %s)",
                   (timestamp, um_solo, um_amb, temperatura, vol_aq))
    
    conn.commit()
    cursor.close()
    conn.close()

def obter_valores(dado, pos, default_value=0):
    try:
        # Conexão com o banco de dados MySQL
        conn = create_connection()
        if conn.is_connected():
            
            # Preparar a consulta SQL para pegar o último valor da coluna especificada
            query = f"SELECT `{dado}` FROM `{statics.table}` ORDER BY `{statics.db_est_data_hora}` DESC LIMIT {pos},1"
            print(f"Query:\n> " + query)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return result[-1]  # Retorna o último valor
            else:
                return default_value  # Retorna o valor padrão se não houver dados
    except Error as e:
        print(f"{statics.txt_err_sql_conn}: {e}")
        return default_value
    except Exception as ex:
        print(f"{statics.txt_err_sql_proc}: \n> {ex}")
        return default_value
    finally:
        if conn and conn.is_connected():
            conn.close()
            print(statics.txt_sql_conn_end)