# Data Quality Studio | Estúdio de Qualidade de Dados

Aplicação interativa para análise e validação da qualidade de dados de compras e pedidos, desenvolvida com Python, Apache Spark (PySpark) e Streamlit.

**Acesse o dashboard:** [Data Quality Studio](https://data-quality-studio-bia.streamlit.app/)

## Sobre o projeto

O Data Quality Studio é um projeto de portfólio que demonstra como técnicas de processamento e validação de dados podem ajudar a identificar inconsistências em informações de compras e pedidos de uma loja virtual.

A aplicação permite analisar os dados processados, acompanhar indicadores e visualizar problemas que precisam de investigação, facilitando a compreensão dos resultados.

## Objetivos

- Identificar e remover registros duplicados.
- Comparar os valores registrados nas compras com os valores calculados a partir dos pedidos.
- Identificar compras sem pedidos associados.
- Analisar a distribuição das compras por cliente, método de pagamento e data.
- Visualizar os resultados por meio de indicadores, gráficos e tabelas interativas.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento do projeto.
- **Apache Spark (PySpark):** processamento e transformação dos dados.
- **Pandas:** manipulação e organização de dados tabulares.
- **Streamlit:** desenvolvimento da interface interativa.
- **Plotly:** criação de gráficos para exploração dos resultados.

## Etapas do processamento

1. **Leitura dos dados:** carregamento dos arquivos CSV de compras e pedidos.
2. **Tratamento de duplicidades:** identificação e remoção de registros repetidos.
3. **Cálculo dos valores:** cálculo dos valores das compras com base nos itens dos pedidos.
4. **Validação dos dados:** comparação entre valores registrados e calculados.
5. **Identificação de inconsistências:** sinalização de compras sem pedidos associados ou com divergências.
6. **Visualização:** apresentação dos resultados em um dashboard interativo.

## Resultados da análise

No conjunto de dados ilustrativo utilizado no projeto, o processamento apresentou os seguintes resultados:

- **Compras:** 7 registros antes da remoção de duplicidades e 5 após o tratamento.
- **Pedidos:** 7 registros antes da remoção de duplicidades e 5 após o tratamento.
- **Validação:** identificação de uma compra sem pedidos associados, que precisa de investigação.
- **Análise exploratória:** consolidação de informações sobre compras por cliente, métodos de pagamento, produtos vendidos e receita por data.

Os resultados demonstram como o tratamento e a validação de dados podem contribuir para a identificação de inconsistências e para a geração de informações mais confiáveis.

## Estrutura do projeto

```text
data-quality-studio/
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

## Como executar localmente

1. Clone o repositório:

   ```bash
   git clone https://github.com/BiancaOrdine/data-quality-studio.git
   ```

2. Acesse a pasta do projeto:

   ```bash
   cd data-quality-studio
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash
   streamlit run app.py
   ```

## Observação


## Como executar os testes automatizados

O projeto possui testes automatizados para verificar a validação dos dados de compras, incluindo compras com valores corretos, compras sem pedidos associados e divergências entre o valor registrado e o valor calculado.

### Pré-requisitos

- Python instalado.
- Java compatível com a versão do PySpark utilizada.
- Dependências do projeto instaladas.

### Instalação das dependências de teste

Após instalar as dependências do projeto, execute:

```bash
pip install pyspark pytest
```

### Execução dos testes

Na pasta raiz do projeto, execute:

```bash
python -m pytest tests/ -v
```

O comando executa os testes encontrados na pasta `tests/` e apresenta o resultado de cada teste no terminal.

<br/>
Este é um projeto demonstrativo desenvolvido para fins de aprendizado e portfólio. Os dados são ilustrativos e não representam informações reais de uma empresa.

---

Desenvolvido por **Bianca Ordine** como projeto de portfólio em processamento, qualidade e visualização de dados.
