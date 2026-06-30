# Passo 3 — Geração de formato otimizado e base de consulta performática
#
# Escolha da abordagem: Parquet + DuckDB
#
# O Parquet (gerado no Passo 2) é um formato colunar e comprimido que lê
# muito mais rápido do que CSV — especialmente em consultas que filtram
# por colunas específicas (ex.: só "Despesas Pagas"), pois não precisa
# carregar colunas irrelevantes.
#
# O DuckDB complementa o Parquet como motor de consulta SQL analítico
# embutido: não exige instalação de servidor, roda no próprio computador
# e consulta arquivos Parquet diretamente com SQL completo. Para análises
# de dados públicos de escala média (dezenas de milhares de linhas),
# DuckDB oferece desempenho muito superior ao pandas puro e é reproduzível
# sem qualquer configuração de infraestrutura.
#
# Este script cria a base finbra.duckdb a partir do Parquet consolidado
# e imprime um diagnóstico dos dados para validação.

import duckdb

con = duckdb.connect("finbra.duckdb")

con.execute("CREATE OR REPLACE TABLE finbra AS SELECT * FROM 'finbra_consolidado.parquet'")

completude = con.execute("""
    SELECT
        ano,
        COUNT(DISTINCT "Cod.IBGE") AS num_capitais,
        COUNT(*) AS total_linhas
    FROM finbra
    WHERE tipo_conta = 'funcao'
    GROUP BY ano
    ORDER BY ano
""").df()

print("Completude dos dados por ano:")
print(completude.to_string(index=False))

estagios = con.execute("""
    SELECT DISTINCT "Coluna"
    FROM finbra
    ORDER BY "Coluna"
""").df()

print("\nEstagios da despesa presentes:")
print(estagios.to_string(index=False))

con.close()
print("\nBase DuckDB salva em finbra.duckdb")
print("Parquet salvo em finbra_consolidado.parquet")
