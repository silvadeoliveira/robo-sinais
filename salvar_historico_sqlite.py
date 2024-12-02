import sqlite3
from datetime import datetime

def criar_banco_dados(nome_banco):
    """
    Cria a estrutura do banco de dados SQLite para salvar histórico de operações.
    :param nome_banco: Nome do arquivo do banco de dados SQLite.
    """
    try:
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()

        # Criar tabela de histórico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT,
                operacao TEXT,
                preco REAL,
                stop_loss REAL,
                take_profit REAL
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")

def salvar_operacao_sqlite(nome_banco, data_hora, operacao, preco, stop_loss, take_profit):
    """
    Salva uma operação no banco de dados SQLite.
    :param nome_banco: Nome do banco de dados SQLite.
    :param data_hora: Data e hora da operação.
    :param operacao: Tipo de operação ("COMPRA" ou "VENDA").
    :param preco: Preço da operação.
    :param stop_loss: Valor do stop-loss.
    :param take_profit: Valor do take-profit.
    """
    try:
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO historico_trades (data_hora, operacao, preco, stop_loss, take_profit)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_hora, operacao, preco, stop_loss, take_profit))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar operação no banco de dados: {e}")
