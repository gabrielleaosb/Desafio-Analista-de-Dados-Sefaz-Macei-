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
