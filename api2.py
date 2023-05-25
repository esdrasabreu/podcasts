import json
import sqlite3

with open('podcasts.json', 'r') as f:
    dados = json.load(f)

conn = sqlite3.connect('podcasts.db')

conn.execute("""
    CREATE TABLE podcast (
        id INTEGER PRIMARY KEY,
        episodio TEXT,
        duracao INTEGER,
        data DATE,
        link TEXT,
        descricao TEXT
    )
""")

for dado in dados:
    conn.execute("""
        INSERT INTO podcast (id, episodio, duracao, data, link, descricao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dado['id'], dado['episodio'], dado['duracao'], dado['data'], dado['link'], dado['descricao']))

conn.commit()
conn.close()
