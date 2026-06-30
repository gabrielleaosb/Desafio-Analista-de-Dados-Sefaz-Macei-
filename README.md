## 💡 Solução Desenvolvida

### Estrutura dos arquivos

```
passo1_descompactar.py   → extrai os ZIPs para dados_extraidos/<ano>/
passo2_consolidar.py     → consolida os CSVs em um DataFrame e salva em Parquet
passo3_otimizado.py      → carrega o Parquet no DuckDB para consultas SQL rápidas
passo4_analise.ipynb     → notebook com as análises e visualizações
saidas/                  → gráficos gerados pelo notebook
requirements.txt         → dependências Python
```

### Como executar

```bash
pip install -r requirements.txt

python passo1_descompactar.py
python passo2_consolidar.py
python passo3_otimizado.py

jupyter notebook passo4_analise.ipynb
```

### Escolhas técnicas

**Por que Parquet + DuckDB?**
O Parquet é um formato colunar e comprimido: em consultas que filtram por poucas colunas (ex.: só "Despesas Pagas"), ele lê apenas o necessário, sem carregar o CSV inteiro. O DuckDB é um banco analítico embutido — roda direto no Python, sem servidor, e consulta arquivos Parquet com SQL completo e desempenho muito superior ao pandas puro em agregações. A combinação torna o projeto reproduzível em qualquer máquina sem configuração de infraestrutura.

**Por que excluir 2025 das comparações entre capitais?**
Em 2025, apenas 11 das 26 capitais entregaram dados ao Siconfi até o momento da análise. Comparar esse ano com os demais em valores totais ou médias levaria a conclusões erradas — a queda nos números refletiria ausência de dados, não redução real de gastos.

**Por que usar gasto per capita?**
São Paulo tem população cerca de 20 vezes maior que Boa Vista. Comparar os dois em valores absolutos é injusto e não revela nada sobre a prioridade orçamentária de cada prefeitura. O gasto por habitante nivela o campo e permite uma comparação real de esforço fiscal.

**Como a coluna `tipo_conta` foi construída?**
A coluna `Conta` mistura três tipos de registro: funções (`10 - Saúde`), subfunções (`10.301 - Atenção Básica`) e totais (`Despesas Exceto Intraorçamentárias`). Somar todos juntos contaria os mesmos valores duas vezes. A classificação por regex separa os três tipos, permitindo filtrar apenas funções para análises comparáveis entre capitais.

### Principais achados

- **Maceió (AL)** ocupa o **8º lugar** em taxa de execução financeira entre 26 capitais no período 2020–2024 (94,3%), acima da média nacional de 92%.
- Em **Saúde**, Maceió investiu R$ 1.315/habitante em 2024 — 13º entre as capitais. O crescimento foi expressivo: saiu de R$ 767/hab em 2020.
- Em **Educação**, o gasto per capita de R$ 716/hab em 2024 coloca Maceió no 22º lugar, abaixo da média das capitais. É a área com maior espaço para avanço.
- As funções com menor taxa de execução no geral são **Habitação** e **Saneamento**, onde as capitais tendem a acumular mais restos a pagar.
