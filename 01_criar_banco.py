"""
01_criar_banco.py
Cria um banco SQLite de exemplo (vendas.db) com uma tabela de vendas.
Rode este script UMA VEZ para gerar a base de dados de teste.
"""
import sqlite3
import random
from datetime import date, timedelta

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS vendas")
cur.execute("""
    CREATE TABLE vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        produto TEXT NOT NULL,
        categoria TEXT NOT NULL,
        valor REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
""")

produtos = [
    ("Notebook", "Eletrônicos"),
    ("Mouse", "Eletrônicos"),
    ("Cadeira", "Móveis"),
    ("Mesa", "Móveis"),
    ("Caderno", "Papelaria"),
    ("Caneta", "Papelaria"),
]

hoje = date.today()
linhas = []
for i in range(200):
    dia = hoje - timedelta(days=random.randint(0, 29))
    produto, categoria = random.choice(produtos)
    valor_unit = round(random.uniform(10, 500), 2)
    qtd = random.randint(1, 5)
    linhas.append((dia.isoformat(), produto, categoria, valor_unit * qtd, qtd))

cur.executemany(
    "INSERT INTO vendas (data, produto, categoria, valor, quantidade) VALUES (?, ?, ?, ?, ?)",
    linhas,
)

conn.commit()
conn.close()
print("Banco 'vendas.db' criado com 200 registros de exemplo.")
