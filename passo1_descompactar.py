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
