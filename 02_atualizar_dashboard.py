"""
02_atualizar_dashboard.py
Conecta no SQLite, roda as queries e escreve tudo em data.json.
Rode este script TODA VEZ que quiser atualizar o dashboard.
"""
import sqlite3
import json

conn = sqlite3.connect("vendas.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# --- KPI: total vendido, número de vendas, ticket médio ---
cur.execute("SELECT SUM(valor) AS total, COUNT(*) AS qtd FROM vendas")
row = cur.fetchone()
total_vendido = round(row["total"] or 0, 2)
num_vendas = row["qtd"]
ticket_medio = round(total_vendido / num_vendas, 2) if num_vendas else 0

# --- Vendas por categoria (para o gráfico) ---
cur.execute("""
    SELECT categoria, SUM(valor) AS total
    FROM vendas
    GROUP BY categoria
    ORDER BY total DESC
""")
por_categoria = [{"categoria": r["categoria"], "total": round(r["total"], 2)} for r in cur.fetchall()]

# --- Vendas por dia (últimos 30 dias, para o gráfico de linha) ---
cur.execute("""
    SELECT data, SUM(valor) AS total
    FROM vendas
    GROUP BY data
    ORDER BY data
""")
por_dia = [{"data": r["data"], "total": round(r["total"], 2)} for r in cur.fetchall()]

# --- Últimas 10 vendas (para compatibilidade) ---
cur.execute("""
    SELECT data, produto, categoria, valor, quantidade
    FROM vendas
    ORDER BY data DESC, id DESC
    LIMIT 10
""")
ultimas = [dict(r) for r in cur.fetchall()]

# --- Todas as vendas (para filtros dinâmicos no dashboard) ---
cur.execute("""
    SELECT id, data, produto, categoria, valor, quantidade
    FROM vendas
    ORDER BY data DESC, id DESC
""")
todas = [dict(r) for r in cur.fetchall()]

conn.close()

dados = {
    "kpis": {
        "total_vendido": total_vendido,
        "num_vendas": num_vendas,
        "ticket_medio": ticket_medio,
    },
    "por_categoria": por_categoria,
    "por_dia": por_dia,
    "ultimas_vendas": ultimas,
    "todas_vendas": todas,
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("data.json atualizado com sucesso!")
