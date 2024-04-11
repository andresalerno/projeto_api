from Classes.ConnClass import *

class Register:

    '''
        Esse método estático busca transformar a string grande e complexa que contém todos os registros do arquivo .csv em uma lista onde cada
        registro também é uma lista, ou seja, uma matriz. ie. list_infos[numero do registro dentro do csv][informação desejada].
    '''
    @staticmethod
    def setup_list(csv_recebido):

        csv_recebido = csv_recebido.replace('\r', '')
        csv_recebido = csv_recebido.replace('"', '')
        csv_recebido = csv_recebido.split('\n')
        
        list_infos = []
        cont = 0
        for item in csv_recebido:
            cont += 1
            print(cont)
            item = item.split(',')
            item[1] = Register.setup_date_type(item[1])
            list_infos.append(item)
        
        
        guardar_registro(list_infos)

        return list_infos
    

    '''
        Essa método estático transforma a data do registro do formato "DD/MM/AAAA" para o formato "AAAA-MM-DD"
    '''
    @staticmethod
    def setup_date_type(data_string):

        list_date = data_string.split("/")
        return list_date[2] + "-" + list_date[1] + "-" + list_date[0] if Register.is_date_valid(list_date) else "Data não é valida!"

    @staticmethod
    def is_date_valid(list_date):

        if len(list_date[0]) > 2 or len(list_date[1]) > 2 or len(list_date[2]) != 4:
            return False
        return True    


    @staticmethod
    def check_csv(csv):
        return csv[-4:] == '.csv' 