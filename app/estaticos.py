#
#   Arquivo para definições estáticas usados em múltiplos arquivos
#
#   Em outras palavras, nunca mudarão!
#

# Banco de dados:
username = 'root'
password = 'root'
host = 'db'
table = 'Estufa'
database = 'CSVRegister'
#
db_est_data_hora = "est_dh"
db_est_um_amb = "est_um_amb"
db_est_um_solo = "est_um_solo"
db_est_temp = "est_temp"
db_est_vol_aq = "est_vol_aq"


# CSV:
csv_dia = 'Dia da semana'
csv_data = 'Data'
csv_hora = 'Hora'
csv_um_amb = 'Umidade Ambiente'
csv_um_solo = 'Umidade solo'
csv_temp = 'Temperatura'
csv_vol_aq = 'Volume Água (L)'


# Data manipulation:
zero = "0,000"
zero_len = len(zero)
zero_rlen = 0 - zero_len
data_aprox = "{0:.03f}"


# Arquivos:
csv_local_up = './uploads/'
csv_nome = 'Dados.csv'
#
xlsx_loc = './static/'
xlsx_nome = 'relatorio.xlsx'
#
svg_positivo = "../static/img/positivo.svg"
svg_negativo = "../static/img/negativo.svg"
svg_neutro = ""


# Strings
txt_title_temp = "Temperatura (°C)"
txt_title_um_solo = "Umidade Solo %"
txt_title_um_amb = "Umidade Ambiente %"
txt_title_vol_aq = "Volume Água (mL)"
#
txt_positivo = 'acima desde a última atualização'
txt_negativo = 'abaixo desde a última atualização'
txt_neutro = "Sem alteração desde a última atualização"
#
txt_sql_conn_init = "Conectado ao banco de dados MySQL"
txt_sql_conn_end = "Conexão ao MySQL encerrada"
#
txt_err_sql_conn = "Erro ao conectar ao MySQL"
txt_err_sql_proc = "Erro ao processar os dados"