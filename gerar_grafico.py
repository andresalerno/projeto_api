import pandas as pd
import plotly.graph_objects as go

def grafico(dado="Temperatura"):
    file = 'Dados.csv'
    # Ajuste para garantir que o separador é corretamente identificado
    data = pd.read_csv(file, encoding='ISO-8859-1', sep=';', engine='python')
    
    if dado not in data.columns:
        print("Colunas disponíveis no DataFrame:", data.columns.tolist())
        raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
    
    # Conversão de valores, se necessário
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

    # Criação do gráfico
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    
    fig.update_xaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo X
    fig.update_yaxes(showline=False, linewidth=0) # Removendo a linha do contorno do eixo Y

    fig.update_layout(
        xaxis_title='Data e Hora',
        title=dado,
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

    config = {'responsive': True, 'modeBarButtonsToRemove': ['resetScale2d'], 'displaylogo': False}
    div_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)
    return div_html