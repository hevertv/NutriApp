"""
Classe para fazer a conexão com o banco de dados.
"""

import sqlite3 as connector


class BancoDados:

    connection = None # Armazena a conexão com o DB.

    id_nutricionista:int = -1 # Armazena o id do nutricionista que fez login.
    id_paciente:int = -1 # Armazena o id do paciente selecionado.

    # Método construtor apenas para criar as tabelas (caso não existam).
    def __init__(self)->None:

        # Cria a conexão com o banco de dados.
        self.connection = connector.connect("banco.db")

        # Cria o cursor para ter acesso ao DB.
        cursor = self.connection.cursor()

        # Habilita a restrição de FK (que vem desabilitada no SQLite): para inserir um valor na FK, este valor deve existir na PK de outra tabela.
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Comandos SQL para criar as tabelas.
        cursor.execute( # nutricionista
            """
            CREATE TABLE IF NOT EXISTS nutricionista (
                id_nutricionista INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL CHECK(length(senha) >= 8),
                data_criacao TEXT NOT NULL,
                CHECK (
                    email LIKE '%_@_%._%' AND
                    LENGTH(email) - LENGTH(REPLACE(email, '@', '')) = 1 AND
                    SUBSTR(LOWER(email), 1, INSTR(email, '.') - 1) NOT GLOB '*[^@0-9a-z]*' AND
                    SUBSTR(LOWER(email), INSTR(email, '.') + 1) NOT GLOB '*[^a-z]*'
                )
            );
            """
        )

        cursor.execute( # paciente
            """
            CREATE TABLE IF NOT EXISTS paciente (
                id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
                id_nutricionista INTEGER NOT NULL,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                estado_civil TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                sexo TEXT NOT NULL,
                raca TEXT NOT NULL,
                naturalidade TEXT NOT NULL,
                foto BLOB,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY (id_nutricionista) REFERENCES nutricionista (id_nutricionista),
                CHECK (
                    email LIKE '%_@_%._%' AND
                    LENGTH(email) - LENGTH(REPLACE(email, '@', '')) = 1 AND
                    SUBSTR(LOWER(email), 1, INSTR(email, '.') - 1) NOT GLOB '*[^@0-9a-z]*' AND
                    SUBSTR(LOWER(email), INSTR(email, '.') + 1) NOT GLOB '*[^a-z]*'
                )
            );
            """
        )

        cursor.execute( # anamnese
            """
            CREATE TABLE IF NOT EXISTS anamnese (
                id_paciente INTEGER PRIMARY KEY,
                profissao TEXT NOT NULL,
                etilismo TEXT NOT NULL,
                atividade_fisica TEXT NOT NULL,
                tabagismo TEXT NOT NULL,
                doencas TEXT NOT NULL,
                questoes_familiares TEXT NOT NULL,
                questoes_religiosas TEXT NOT NULL,
                questoes_sociais TEXT NOT NULL,
                tradicoes TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente)
            );
            """
        )

        cursor.execute( # antropometria
            """
            CREATE TABLE IF NOT EXISTS antropometria (
                id_paciente INTEGER PRIMARY KEY,
                peso REAL NOT NULL,
                altura INTEGER NOT NULL,
                circunferencia_cintura INTEGER NOT NULL,
                composicao_corporal TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente)
            );
            """
        )

        cursor.execute( # inquerito_alimentar
            """
            CREATE TABLE IF NOT EXISTS inquerito_alimentar (
                id_paciente INTEGER PRIMARY KEY,
                desjejum TEXT,
                desjejum_horario TEXT,
                lanche_manha TEXT,
                lanche_manha_horario TEXT,
                almoco TEXT,
                almoco_horario TEXT,
                lanche_tarde TEXT,
                lanche_tarde_horario TEXT,
                jantar TEXT,
                jantar_horario TEXT,
                ceia TEXT,
                ceia_horario TEXT,
                outras TEXT,
                outras_horario TEXT,
                data_criacao TEXT NOT NULL,
                FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente)
            );
            """
        )

        # Salva os comandos executados.
        self.connection.commit()

        # Fecha a conexão.
        cursor.close()


    # Método para inserir um novo valor em uma tabela.
    # ├─ table_name: o nome da tabela para inserior o novo valor.
    # └─ column_values: um dicionário com os valores para serem inseridos.
    def create(self, table_name:str, column_values:dict)->bool:

        # Tenta executar o comando para o DB.
        try:
            
            # Obtém o nome das colunas e valores separados por ", ".
            columns = ", ".join(column_values.keys())
            values = ", ".join(
                str(value) if not isinstance(value, str)
                else (
                    "null" if not value
                    else f"'{value}'"
                )
                for value in column_values.values()
            )

            # Cria o comando para enviar ao DB.
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            print(sql)

            # Acessa o DB, executa o comando, salva e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print("Cadastro feito com sucesso!")

            return True
        
        # Caso algo de errado.
        except:
            print("Ocorreu um erro no cadastro!")
            return False


    # Método para ler os valores de uma tabela, com a opção de utilizar um filtro.
    # ├─ table_name: o nome da tabela para buscar os valores.
    # └─ column_filter (opcional): um dicionário com os valores das colunas para filtrar a busca.
    def read(self, table_name:str, column_filter:dict = {})->list:

        # Tenta executar o comando para o DB.
        try:

            # Começa a criar o comando para enviar ao DB.
            sql = f"SELECT * FROM {table_name}"

            # Adiciona o filtro na pesquisa do DB.
            if column_filter:
                conditions = []
                for column_name, value in column_filter.items():
                    if not column_name.startswith("id"):
                        value = f"'%{value}%'"
                    conditions.append(f"{column_name} LIKE {value}")
                sql += " WHERE " + " AND ".join(conditions)
            print(sql)

            # Acessa o DB, executa o comando e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall() # Obtém os valores da consulta.
            cursor.close()
            print("Leitura feita com sucesso!")

            # Retorna os valores da consulta.
            return result 

        # Caso algo de errado.
        except:
            print("Ocorreu um erro na leitura!")
        
        return []


    # Método para ler os valores de um registro de uma tabela buscando pelo ID.
    # ├─ table_name: o nome da tabela para buscar os valores.
    # ├─ id_name: o nome da coluna que representa o ID.
    # └─ id_value: o valor do ID para buscar.
    def ready_by_id(self, table_name:str, id_name:str, id_value:int)->None:

        # Tenta executar o comando para o DB.
        try:

            # Comando para enviar ao DB.
            sql = f"SELECT * FROM {table_name} WHERE {id_name} = {id_value}"
            print(sql)

            # Acessa o DB, executa o comando e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone() # Obtém os valores da consulta.
            cursor.close()
            print("Leitura feita com sucesso!")

            return result # Retorna os valores da consulta.

        # Caso algo de errado.
        except:
            print("Ocorreu um erro na leitura!")
        

    # Método para atualizar valores existentes em uma tabela com base no ID.
    # ├─ table_name: o nome da tabela para atualizar os valores.
    # ├─ id_name: o nome da coluna que representa o ID.
    # ├─ id_value: o valor do ID para atualizar os valores.
    # └─ column_values: um dicionário com os valores para serem atualizados.
    def update(self, table_name:str, id_name:str, id_value:int, column_values:dict)->bool:

        # Tenta executar o comando para o DB.
        try:

            # Obtém as colunas e seus valores para atualizarem.
            set_columns = []
            for column_name, value in column_values.items():
                if isinstance(value, str):
                    value = f"'{value}'"
                set_columns.append(f"{column_name} = {value}")
            
            # Define as cláusulas "SET" e "WHERE".
            set_clause = ", ".join(set_columns)
            where_clause = f"{id_name} = {id_value}"
            
            # Cria o comando para enviar ao DB.
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            # print(sql)

            # Acessa o DB, executa o comando, salva e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print("Dados atualizados com sucesso!")
            return True

        # Caso algo de errado.
        except connector.Error as error:
            print("Ocorreu um erro ao atualizar os dados!", error)
            return False


    # Método para excluir um registro existente com base no ID.
    # ├─ table_name: o nome da tabela para excluir o registro.
    # ├─ id_name: o nome da coluna que representa o ID.
    # └─ id_value: o valor do ID para para excluir o registro.
    def delete(self, table_name:str, id_name:str, id_value:int)->bool:

        # Tenta executar o comando para o DB.
        try:

            # Comando para enviar ao DB.
            sql = f"DELETE FROM {table_name} WHERE {id_name} = {id_value}"
            print(sql)
            
            # Acessa o DB, executa o comando, salva e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print("Dados removidos com sucesso!")
            return True

        # Caso algo de errado.
        except:
            print("Ocorreu um erro ao remover os dados!")
            return False


    # Método para obter autorização ao fazer login.
    def get_user_auth(self, email:str, senha:str)->bool:

        # Tenta executar o comando para o DB.
        try:

            # Cria o comando para o DB.
            sql = f"SELECT * FROM nutricionista WHERE email = '{email}' and senha = '{senha}'"
            print(sql)

            # Acessa o DB, executa o comando e depois fecha a conexão.
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone() # Obtém o valor da consulta.
            cursor.close()
            print("Leitura feita com sucesso!")
            
            if result is not None:
                self.id_nutricionista = result[0]
                return True

            print("Acesso negado!")
            return False

        # Caso algo de errado.
        except:
            print("Ocorreu um erro na leitura!")
