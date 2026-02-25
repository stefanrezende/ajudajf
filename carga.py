"""
carga.py — Script de carga dos pontos de arrecadação
Execute UMA VEZ com: python carga.py

Requer a variável DATABASE_URL configurada:
  export DATABASE_URL="postgresql://..."
  python carga.py
"""

import psycopg
from psycopg.rows import dict_row
import os, uuid

DATABASE_URL = os.environ.get("DATABASE_URL", "")

PONTOS = [
    {
        "nome": "Prédio Sede da PJF",
        "endereco": "Av. Brasil, 2001 (térreo) - Centro, Juiz de Fora - MG",
        "latitude": -21.7622,
        "longitude": -43.3496,
        "responsavel": "Prefeitura de Juiz de Fora",
        "telefone": "(32) 3690-8000",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Casa da Mulher",
        "endereco": "Av. Garibaldi Campinhos, 169 - Vitorino Braga, Juiz de Fora - MG",
        "latitude": -21.7895,
        "longitude": -43.3710,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Escola Municipal Murilo Mendes",
        "endereco": "Rua Dr. Leonel Jaguaribe, 240 - Alto Grajaú, Juiz de Fora - MG",
        "latitude": -21.7530,
        "longitude": -43.3340,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Escola Municipal Professor Nilo Camilo Ayupe",
        "endereco": "Rua Almirante Barroso, 155 - Paineiras, Juiz de Fora - MG",
        "latitude": -21.7720,
        "longitude": -43.3890,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Shopping Jardim Norte",
        "endereco": "Av. Brasil, 6345 - Mariano Procópio, Juiz de Fora - MG",
        "latitude": -21.7910,
        "longitude": -43.3760,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Unimed Juiz de Fora",
        "endereco": "Av. Rio Branco, 2540 - Juiz de Fora - MG",
        "latitude": -21.7648,
        "longitude": -43.3570,
        "responsavel": "Unimed JF",
        "telefone": "(32) 3257-2000",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Emcasa",
        "endereco": "Av. Sete de Setembro, 975 - Costa Carvalho, Juiz de Fora - MG",
        "latitude": -21.7700,
        "longitude": -43.3620,
        "responsavel": "Emcasa",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "IF Sudeste MG",
        "endereco": "Rua Bernardo Mascarenhas, 1283 - Bairro Fábrica, Juiz de Fora - MG",
        "latitude": -21.7580,
        "longitude": -43.3450,
        "responsavel": "Instituto Federal Sudeste MG",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Escola Municipal Paulo Rogério dos Santos",
        "endereco": "Rua Cel. Quintão, 136 - Monte Castelo, Juiz de Fora - MG",
        "latitude": -21.7810,
        "longitude": -43.3530,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Supermercados Bahamas – Todas as Lojas",
        "endereco": "Diversas unidades - Juiz de Fora - MG",
        "latitude": -21.7640,
        "longitude": -43.3510,
        "responsavel": "Rede Bahamas",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Sindicato dos Bancários",
        "endereco": "Rua Batista de Oliveira, 745 - Juiz de Fora - MG",
        "latitude": -21.7630,
        "longitude": -43.3480,
        "responsavel": "Sindicato dos Bancários",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Igreja Metodista em Bela Aurora",
        "endereco": "Rua Dr. Costa Reis, 380 - Ipiranga, Juiz de Fora - MG",
        "latitude": -21.7750,
        "longitude": -43.3440,
        "responsavel": "Igreja Metodista",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "UniAcademia",
        "endereco": "Rua Halfeld, 1.179 - Centro, Juiz de Fora - MG",
        "latitude": -21.7618,
        "longitude": -43.3468,
        "responsavel": "UniAcademia",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Independência Shopping",
        "endereco": "Av. Presidente Itamar Franco, 3600 - Cascatinha, Juiz de Fora - MG",
        "latitude": -21.7462,
        "longitude": -43.3620,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "AACI",
        "endereco": "Rua Doutor Dias da Cruz, 487 - Nova Era, Juiz de Fora - MG",
        "latitude": -21.7690,
        "longitude": -43.3590,
        "responsavel": "AACI",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Secretaria Especial de Igualdade Racial",
        "endereco": "Av. Rio Branco, 2234 - Centro, Juiz de Fora - MG",
        "latitude": -21.7635,
        "longitude": -43.3555,
        "responsavel": "PJF",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Loja Maçônica",
        "endereco": "Rua Cândido Tostes, 212 - São Mateus, Juiz de Fora - MG",
        "latitude": -21.7555,
        "longitude": -43.3525,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Mister Shopping",
        "endereco": "Rua Mr. Moore, 70 - Centro, Juiz de Fora - MG",
        "latitude": -21.7610,
        "longitude": -43.3490,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Souza Gomes Imóveis",
        "endereco": "Av. Presidente Itamar Franco, 2.800 - São Mateus, Juiz de Fora - MG",
        "latitude": -21.7520,
        "longitude": -43.3600,
        "responsavel": "Souza Gomes Imóveis",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Trade Hotel",
        "endereco": "Av. Presidente Itamar Franco, 3800 - Cascatinha, Juiz de Fora - MG",
        "latitude": -21.7455,
        "longitude": -43.3628,
        "responsavel": "Trade Hotel",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Shopping Alameda",
        "endereco": "R. Morais e Castro, 300 - Passos, Juiz de Fora - MG",
        "latitude": -21.7668,
        "longitude": -43.3715,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Salvaterra Restaurante",
        "endereco": "Av. Deusdedith Salgado, 4735 - Salvaterra, Juiz de Fora - MG",
        "latitude": -21.8120,
        "longitude": -43.3480,
        "responsavel": "Salvaterra Restaurante",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Praça de Pedágio – Simão Pereira (BR-040)",
        "endereco": "BR-040, km 819 - Simão Pereira, MG",
        "latitude": -21.9850,
        "longitude": -43.4120,
        "responsavel": "",
        "telefone": "",
        "horario": "",
        "itens": "",
    },
    {
        "nome": "Sesc Mesa Brasil",
        "endereco": "Rua Carlos Chagas, 100 - São Mateus, Juiz de Fora - MG",
        "latitude": -21.7562,
        "longitude": -43.3512,
        "responsavel": "Sesc JF",
        "telefone": "(32) 3216-9200",
        "horario": "",
        "itens": "",
    },
]


def main():
    if not DATABASE_URL:
        print("ERRO: variável DATABASE_URL não definida.")
        return

    print(f"Conectando ao banco...")
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        # garante tabela
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pontos (
                id          TEXT PRIMARY KEY,
                nome        TEXT NOT NULL,
                endereco    TEXT NOT NULL,
                latitude    DOUBLE PRECISION NOT NULL,
                longitude   DOUBLE PRECISION NOT NULL,
                responsavel TEXT DEFAULT '',
                telefone    TEXT DEFAULT '',
                horario     TEXT DEFAULT '',
                itens       TEXT DEFAULT '',
                ativo       BOOLEAN DEFAULT TRUE,
                criado_em   TIMESTAMP DEFAULT NOW()
            )
        """)

        inseridos = 0
        pulados   = 0
        for p in PONTOS:
            existe = conn.execute(
                "SELECT 1 FROM pontos WHERE nome = %s", (p["nome"],)
            ).fetchone()
            if existe:
                print(f"  [PULADO] {p['nome']} (já existe)")
                pulados += 1
                continue

            conn.execute("""
                INSERT INTO pontos
                  (id, nome, endereco, latitude, longitude,
                   responsavel, telefone, horario, itens)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                str(uuid.uuid4()),
                p["nome"], p["endereco"],
                p["latitude"], p["longitude"],
                p["responsavel"], p["telefone"],
                p["horario"], p["itens"],
            ))
            print(f"  [OK] {p['nome']}")
            inseridos += 1

    print(f"\n✅ Concluído: {inseridos} inseridos, {pulados} pulados.")
    print("⚠️  Confira as coordenadas no mapa e ajuste as que estiverem imprecisas.")


if __name__ == "__main__":
    main()
