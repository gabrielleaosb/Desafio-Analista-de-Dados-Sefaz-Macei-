# Passo 1 — Descompactação dos arquivos ZIP
#
# Os dados do Siconfi vêm compactados em arquivos .zip organizados por ano
# dentro de dados_compactos/. Este script percorre toda a pasta recursivamente,
# encontra cada .zip e extrai o conteúdo para dados_extraidos/<ano>/.
#
# A pasta de destino é criada automaticamente caso não exista.
# O ano é inferido pelo nome da pasta pai de cada arquivo zip.

from pathlib import Path
import zipfile

dados_compactos = Path("dados_compactos")
dados_extraidos = Path("dados_extraidos")

for zip_path in sorted(dados_compactos.rglob("*.zip")):
    ano = zip_path.parent.name
    destino = dados_extraidos / ano
    destino.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(destino)
    print(f"Extraido: {zip_path} -> {destino}/")

print("\nDescompactacao concluida.")
