# Data Quality Studio

Projeto demonstrativo de qualidade de dados para análise de compras e pedidos.

## Objetivo

Identificar duplicidades, conferir os valores registrados nas compras
com os valores calculados a partir dos pedidos e sinalizar registros
que precisam de investigação.

## Tecnologias

- Python
- Apache Spark (PySpark)
- Pandas
- Streamlit
- Plotly

## Estrutura do projeto

```text
data-quality-dashboard/
├── dados/
│   ├── compras.csv
│   └── pedidos.csv
├── dados_processados/
│   ├── compras_limpo.csv
│   ├── pedidos_limpo.csv
│   └── validacao.csv
├── src/
│   └── processamento.py
├── tests/
├── app.py
└── README.md
```

## Etapas do processamento

1. Leitura dos arquivos CSV.
2. Remoção de linhas duplicadas.
3. Cálculo dos valores dos pedidos.
4. Comparação dos valores calculados com os valores registrados.
5. Sinalização de compras sem pedidos associados ou com valores divergentes.
6. Visualização dos resultados em um dashboard.

## Observação

Este é um projeto demonstrativo com dados ilustrativos.
Os resultados não representam dados reais de uma empresa.
