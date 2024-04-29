import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta
import os
from sqlalchemy.types import DateTime

# Configuração do banco de dados
username = 'root'
password = 'fatec'
host = 'localhost'
database = 'estufa'

def criar_banco():
    try:
        # Conexão com o banco de dados MySQL
        engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

        # Caminho do arquivo CSV
        file_path = "./uploads/Dados.csv"

        # Carregar dados do CSV
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

            # Garantir que a coluna de data/hora esteja no formato datetime
            df['Data_Hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'], dayfirst=True, errors='coerce')
            df = df.dropna(subset=['Data_Hora'])
            
            # Ordenar os dados por Data_Hora antes de definir como índice
            df = df.sort_values(by='Data_Hora').set_index('Data_Hora')
            
            # Excluir as colunas desnecessárias
            df = df.drop(columns=['Dia da semana', 'Data', 'Hora'])
            
            # Filtrar os dados para ter entradas com pelo menos 10 minutos de diferença
            data_filtrada = df[~(df.index.to_series().diff() < pd.Timedelta('10min'))]
            
            dtype = {
                'Data_Hora': DateTime,
            }
            
            # Inserir dados no MySQL
            data_filtrada.reset_index(inplace=True)
            data_filtrada.to_sql('estufa', con=engine, if_exists='append', index=False, dtype=dtype)

            # Excluir o arquivo após inserção no banco de dados
            os.remove(file_path)
            print("Arquivo CSV excluído com sucesso.")
        else:
            print("Erro: Arquivo CSV não encontrado.")

    except Exception as e:
        print(f"Erro durante o processo: {e}")