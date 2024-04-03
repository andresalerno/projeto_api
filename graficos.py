import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico(dado):
    """
    Gera e salva um gráfico do dado especificado ao longo do tempo.

    """
    # Caminho para o arquivo CSV
    file_path = 'Dados.csv'
    
    # Lendo o arquivo CSV, ajustando para a codificação correta e possível separador inconsistente
    data = pd.read_csv(file_path, encoding='ISO-8859-1', sep=None, engine='python')

    if dado not in data.columns:
        raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
    
    # Certifique-se de que o argumento 'dado' corresponde exatamente ao nome da coluna no DataFrame
    if dado not in data.columns:
        raise ValueError(f"O dado '{dado}' não foi encontrado nas colunas do DataFrame.")
    
    if dado == 'Temperatura':
        data[dado] = data[dado].str.replace(',', '.').astype(float)
    elif dado == 'Volume Ã¡gua':
        # Certifique-se de que o nome da coluna corresponde ao seu DataFrame
        data[dado] = pd.to_numeric(data[dado].str.replace(',', '.'), errors='coerce')
    
    # Filtrando possíveis entradas inválidas
    data_filtered = data[~data['Data'].str.contains("0/0/2000")]
    data_filtered = data_filtered[data_filtered['Hora'].apply(lambda x: len(x.split(':')) == 2)]
    data_filtered['Hora'] = data_filtered['Hora'].apply(lambda x: x if len(x.split(':')[0]) == 2 else '0' + x)

    # Combinando as colunas de data e hora e convertendo para datetime
    data_filtered['Data_Hora'] = pd.to_datetime(data_filtered['Data'] + ' ' + data_filtered['Hora'], dayfirst=True, errors='coerce')

    # Removendo quaisquer linhas com 'Data_Hora' nulo após a conversão
    data_clean = data_filtered.dropna(subset=['Data_Hora'])

    # Agrupando os dados por hora e calculando a média do dado escolhido
    data_hourly_clean = data_clean.groupby(data_clean['Data_Hora'].dt.floor('h')).agg({dado:'mean'}).reset_index()

    # Plotando o gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(data_hourly_clean['Data_Hora'], data_hourly_clean[dado], marker='o', linestyle='-', color='blue')
    plt.title(f'{dado} ao Longo do Tempo')
    plt.xlabel('Data e Hora')
    plt.ylabel(dado)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvando o gráfico como um arquivo de imagem
    nome_arquivo = f'{dado.lower().replace(" ", "_")}_ao_longo_do_tempo.png'
    # plt.savefig(f"./api_teste/{nome_arquivo}", bbox_inches='tight')
    plt.show()
    plt.close()  # Fecha a figura para evitar a exibição em ambientes interativos

# Exemplo de uso
# gerar_grafico('Temperatura')
# gerar_grafico('Umidade solo')
# gerar_grafico('Umidade Ambiente')
# gerar_grafico('Volume Ã¡gua')
# Para gerar gráficos para outros dados, basta chamar a função com o dado desejado.