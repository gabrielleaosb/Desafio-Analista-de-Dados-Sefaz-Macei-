# Passo 2 — Leitura e consolidação dos CSVs em um único DataFrame
#
# Cada arquivo finbra.csv segue o padrão brasileiro do Siconfi, com algumas
# particularidades que precisam ser tratadas explicitamente:
#
#   - encoding="latin-1": o arquivo usa ISO-8859-1; abrir como UTF-8
#     transforma acentos em caracteres inválidos (ex.: "Saúde" → "Sa?de").
#   - sep=";": o separador de colunas é ponto e vírgula, não vírgula.
#   - decimal=",": valores monetários usam vírgula decimal (padrão BR).
#   - thousands=".": ponto como separador de milhar em alguns campos.
#   - skiprows=3: as 3 primeiras linhas são metadados do Siconfi
#     (Exercício, Escopo, Tabela) e precisam ser ignoradas na leitura.
#
# Após a leitura, o ano é adicionado como coluna — informação derivada da
# pasta de origem, não presente no CSV em si.
#
# A coluna tipo_conta classifica cada linha da coluna Conta em:
#   - "funcao"   → formato "XX - Nome" (2 dígitos + traço), ex.: "10 - Saúde"
#   - "subfuncao"→ formato "XX.YYY",                        ex.: "10.301 - ..."
#   - "total"    → linhas agregadas como "Despesas Exceto Intraorçamentárias"
#
# Essa classificação é essencial para evitar dupla contagem nas análises:
# somar funções e subfunções juntas contaria o mesmo valor duas vezes.

from pathlib import Path
import re
import pandas as pd

dados_extraidos = Path("dados_extraidos")
dfs = []

for csv_path in sorted(dados_extraidos.rglob("*.csv")):
    ano = int(csv_path.parent.name)
    df = pd.read_csv(
        csv_path,
        sep=";",
        skiprows=3,
        encoding="latin-1",
        decimal=",",
        thousands=".",
    )
    df["ano"] = ano
    dfs.append(df)

finbra = pd.concat(dfs, ignore_index=True)

finbra.columns = finbra.columns.str.strip()
finbra["Valor"] = pd.to_numeric(finbra["Valor"], errors="coerce")

def classificar_conta(conta):
    conta = str(conta)
    if re.match(r"^\d{2} - ", conta):
        return "funcao"
    if re.match(r"^\d{2}\.\d{3}", conta):
        return "subfuncao"
    return "total"

finbra["tipo_conta"] = finbra["Conta"].apply(classificar_conta)

finbra.to_parquet("finbra_consolidado.parquet", index=False)

print(f"Linhas totais: {len(finbra):,}")
print("\nCapitais por ano:")
print(
    finbra[finbra["tipo_conta"] == "funcao"]
    .groupby("ano")["Cod.IBGE"]
    .nunique()
    .rename("num_capitais")
)
print("\nDistribuicao de tipo_conta:")
print(finbra["tipo_conta"].value_counts())
print("\nSalvo em finbra_consolidado.parquet")
