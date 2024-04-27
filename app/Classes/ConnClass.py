import mysql.connector
import csv

mysql = mysql.connector.connect(
            user= 'root',
        	password= '',
            #aqui em baixo é o nome do container ao invés de ser localhost kkkkkkkk
        	host= 'localhost',
    		database= 'CSVRegister'
        )

def guardar_registro(list_infos):

    cursor = mysql.cursor()

    for item in list_infos:
        query = f'INSERT INTO RegistroIndividual (dia_reg, data_reg, hora_reg, umidade_solo_reg, umidade_ambiente_reg, temperatura_reg, volume_reg) VALUES ("{item[0]}", "{item[1]}", "{item[2]}", {item[3]}, {item[4]}, {item[5]}, {item[6]})'
        cursor.execute(query)
                
    mysql.commit()

# Essa função cria os gráficos trazendo do DB as coisas mas sem filtro por enquanto
def criar_csv():
    
    with open("app\\Files\\Dados.csv", 'w', newline='') as file:
        
        myresult = ''

        try:
            mycursor = mysql.cursor()

            mycursor.execute("SELECT * FROM RegistroIndividual")

            myresult = mycursor.fetchall()

            writer = csv.writer(file, dialect='excel')
            temp1 = 'Dia da semana;Data;Hora;Umidade solo;Umidade Ambiente;Temperatura;Volume Água (L)'
            field = [temp1]
            writer.writerow(field)

            for x in myresult:
                tmp = f'{x[1]}; {x[2]}; {x[3]}; {x[4]}; {x[5]}; {x[6]}; {x[7]}'
                teste = [tmp]
                writer.writerow(teste)
                print(teste)

        except:
            return "Não foi possivel acessar o Banco de Dados, tente novamente mais tarde!"

criar_csv()