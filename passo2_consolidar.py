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
