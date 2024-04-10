import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def grafico(dado):
    file = 'Dados.csv'
    # Ajuste para garantir que o separador é corretamente identificado
    data = pd.read_csv(file, encoding='ISO-8859-1', sep=';', engine='python')
    
    if dado not in data.columns:
        print("Colunas disponíveis no DataFrame:", data.columns.tolist())
        raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
    
    # Conversão de valores, se necessário - Pois não aceita ','
    if dado == 'Temperatura':
        data[dado] = data[dado].str.replace(',', '.').astype(float)
    elif dado == 'Volume Água (L)':
        data[dado] = pd.to_numeric(data[dado].str.replace(',', '.'), errors='coerce')
    
    # Criação de uma coluna datetime a partir da Data e da Hora
    data['Data_Hora'] = pd.to_datetime(data['Data'] + ' ' + data['Hora'], dayfirst=True, errors='coerce')
    data = data.dropna(subset=['Data_Hora'])
    
    # Ordenar os dados por Data_Hora antes de definir como índice
    data = data.sort_values(by='Data_Hora').set_index('Data_Hora')
    
    # Filtrar os dados para ter entradas com pelo menos 10 minutos de diferença
    data_filtrada = data[~(data.index.to_series().diff() < pd.Timedelta('10min'))]
    
    # Selecionar os dados da coluna desejada
    y = data_filtrada[dado].to_list()
    x = data_filtrada.index.tolist()  # Usar o índice Data_Hora como eixo x
    
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

def obter_ultimos_valores(dado):
    # Lendo o arquivo CSV com a codificação e delimitador corretos
    df = pd.read_csv("Dados.csv", encoding='ISO-8859-1', sep=';')
    # Capturando o último valor do dado desejado
    ultimos_valores = df[dado].iloc[-1]
    return ultimos_valores

def gerar_tabela():
    file = 'Dados.csv'
    # Carregamento dos dados com o encoding e separador especificado
    data = pd.read_csv(file, encoding='ISO-8859-1', sep=';', engine='python')
    
    # Remoção da coluna "dia da semana" (assumindo que é a primeira coluna)
    data = data.drop(data.columns[0], axis=1)

    # Combinação das colunas 'Data' e 'Hora' em 'Data_Hora' e conversão para datetime
    data['Data_Hora'] = pd.to_datetime(data['Data'] + ' ' + data['Hora'], dayfirst=True, errors='coerce')
    
    # Remoção de linhas com 'Data_Hora' nulo e ordenação
    data = data.dropna(subset=['Data_Hora']).sort_values(by='Data_Hora')
    
    # Remoção das colunas originais 'Data' e 'Hora' após a combinação, se desejado
    data = data.drop(['Data', 'Hora'], axis=1)
    
    # Geração do arquivo Excel sem incluir 'Data_Hora' como índice
    data.to_excel("./static/relatorio.xlsx", index=False)