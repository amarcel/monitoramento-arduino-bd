import serial # instalar biblioteca pyserial
import sqlite3

def criarBD():
  try:
    sqliteConnection = sqlite3.connect('BancoDados.db')
    cursor = sqliteConnection.cursor()
    print("Banco de dados criado com sucesso")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("Versão do SQLite: ", record)
    cursor.close()

  except sqlite3.Error as error:
    print("Erro ao conectar ao SQLite", error)
  finally:
    if sqliteConnection:
      sqliteConnection.close()
      print("Conexão fechada")

def criarTabelasBD():
  try:
    sqliteConnection = sqlite3.connect('BancoDados.db')
    sqlite_create_table_query = '''CREATE TABLE medicao (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                umidade REAL NOT NULL,
                                temperatura REAL NOT NULL,
                                data_hora datetime NOT NULL DEFAULT CURRENT_TIMESTAMP);'''

    cursor = sqliteConnection.cursor()
    print("Conectado ao banco de dados com sucesso")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("Tabela criada com sucesso")

    cursor.close()

  except sqlite3.Error as error:
    print("Erro ao tentar criar a tabela", error)
  finally:
    if sqliteConnection:
      sqliteConnection.close()
      print("Conexão fechada")

def inserirMedicaoBD(umidade, temperatura):
  try:
    sqliteConnection = sqlite3.connect('BancoDados.db')
    cursor = sqliteConnection.cursor()
    print("Conectado ao banco de dados com sucesso")

    sqlite_insert_query = '''INSERT INTO medicao (umidade, temperatura) VALUES (?, ?)'''
    data_tuple = (umidade, temperatura)

    count = cursor.execute(sqlite_insert_query, data_tuple)
    sqliteConnection.commit()
    print("Dado inserido com sucesso ", cursor.rowcount)
    cursor.close()

  except sqlite3.Error as error:
    print("Erro ao inserir dado na tabela medicao", error)
  finally:
    if sqliteConnection:
      sqliteConnection.close()
      print("Conexão fechada")


def realizarMedicoesArduino():
  arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)

  i = 0
  while True:
    data = arduino.readline()[:].decode('utf-8')
    if data:
#      print(type(data))
#      break
      if i > 0:
        data = str(data)
        try:
          data = data.split(';')  # exemplo: 80.7;30.8
          umidade = data[0]
          temperatura = data[1]
          print(umidade,';',temperatura)
          inserirMedicaoBD(umidade, temperatura)
        except IndexError:
          print('erro')
      i = i + 1

# aqui inicia o programa:
criarBD()
criarTabelasBD()
realizarMedicoesArduino()
