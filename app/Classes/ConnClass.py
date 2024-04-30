import mysql.connector

mysql = mysql.connector.connect(
            user= 'root',
        	password= 'root',
            #aqui em baixo é o nome do container ao invés de ser localhost kkkkkkkk
        	host= 'db',
    		database= 'CSVRegister'
        )

def guardar_registro(list_infos):

    cursor = mysql.cursor()

    for item in list_infos:
        query = f'INSERT INTO RegistroIndividual (dia_reg, data_reg, hora_reg, umidade_solo_reg, umidade_ambiente_reg, temperatura_reg, volume_reg) VALUES ("{item[0]}", "{item[1]}", "{item[2]}", {item[3]}, {item[4]}, {item[5]}, {item[6]})'
        cursor.execute(query)
                
    mysql.commit()
