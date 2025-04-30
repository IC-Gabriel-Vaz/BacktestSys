import sqlite3

class Admin:

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        try:
            self.connection= sqlite3.connect(self.db_path)
            print("Conexão com a Base de Dados estabelecida! \n")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    def disconnect(self):
        if self.connection == True:
            self.connection.close()
            print("Conexão encerrada")
