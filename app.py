
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# --------------------------------------------------
# 1. Configuração
# --------------------------------------------------

PASTA_PROJETO = Path(__file__).parent
PASTA_DADOS = PASTA_PROJETO / "dados_processados"

st.set_page_config(
    page_title="Data Quality Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# 2. Identidade visual adaptável ao tema
# --------------------------------------------------

st.markdown("""
<style>
    :root {
        --dq-accent: #B84F73;
        --dq-accent-soft: #E7B8C8;
        --dq-line: var(--secondary-background-color);
    }

    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label, span {
        color: inherit;
    }

    h1 {
        font-size: clamp(2rem, 4vw, 3rem) !important;
        font-weight: 650 !important;
        letter-spacing: -0.055em;
        line-height: 1.1 !important;
    }

    h2 {
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.035em;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    .dq-eyebrow {
        color: var(--dq-accent);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .dq-intro {
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.75;
        opacity: 0.78;
    }

    .dq-section-note {
        font-size: 0.86rem;
        opacity: 0.7;
        line-height: 1.6;
        margin-top: -0.5rem;
        margin-bottom: 1.1rem;
    }

    .dq-rule {
        border: 0;
        border-top: 1px solid var(--dq-line);
        margin: 1.8rem 0;
    }

    .dq-kpi-label {
        font-size: 0.78rem;
        opacity: 0.72;
        margin-bottom: 0.55rem;
    }

    .dq-kpi-value {
        font-size: clamp(1.45rem, 2.5vw, 2rem);
        font-weight: 650;
        letter-spacing: -0.045em;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }

    .dq-kpi {
        padding: 0.65rem 0 0.8rem 1rem;
        border-left: 2px solid var(--dq-accent-soft);
        min-height: 88px;
    }

    .dq-status {
        padding: 0.95rem 1.1rem;
        border-left: 3px solid var(--dq-accent);
        background: var(--secondary-background-color);
        border-radius: 0 5px 5px 0;
        line-height: 1.65;
        margin: 0.8rem 0 1rem 0;
    }

    .dq-footer {
        font-size: 0.78rem;
        opacity: 0.65;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--dq-line);
        padding: 1rem 1.1rem;
        border-radius: 5px;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricDelta"] {
        color: var(--text-color);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.82rem;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 650;
        letter-spacing: -0.035em;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label {
        font-size: 0.82rem;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--dq-line);
        border-radius: 5px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 5px;
    }

    button[kind="secondary"] {
        border-radius: 5px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.3rem;
        }

        h1 {
            font-size: 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. Carregar os dados processados
# --------------------------------------------------

@st.cache_data
def carregar_dados():
    compras = pd.read_csv(
        PASTA_DADOS / "compras_limpo.csv"
    )

    pedidos = pd.read_csv(
        PASTA_DADOS / "pedidos_limpo.csv"
    )

    validacao = pd.read_csv(
        PASTA_DADOS / "validacao.csv"
    )

    return compras, pedidos, validacao


compras, pedidos, validacao = carregar_dados()


# --------------------------------------------------
# 4. Preparar os tipos
# --------------------------------------------------

compras["data_compra"] = pd.to_datetime(
    compras["data_compra"],
    errors="coerce"
)

compras["valor_total"] = pd.to_numeric(
    compras["valor_total"],
    errors="coerce"
)

compras["cliente_id"] = pd.to_numeric(
    compras["cliente_id"],
    errors="coerce"
).astype("Int64")

pedidos["quantidade"] = pd.to_numeric(
    pedidos["quantidade"],
    errors="coerce"
)

validacao["valor_total"] = pd.to_numeric(
    validacao["valor_total"],
    errors="coerce"
)

validacao["valor_calculado"] = pd.to_numeric(
    validacao["valor_calculado"],
    errors="coerce"
)

# Evita que valores ausentes na situação sejam tratados
# silenciosamente como registros válidos.
validacao["situacao"] = (
    validacao["situacao"]
    .fillna("SITUAÇÃO NÃO INFORMADA")
)


# --------------------------------------------------
# 5. Cabeçalho
# --------------------------------------------------

st.markdown(
    '<div class="dq-eyebrow">Dados · Análise · Confiabilidade</div>',
    unsafe_allow_html=True
)

st.title("Data Quality Studio")

st.markdown(
    """
    <p class="dq-intro">
        Uma leitura da qualidade dos dados de compras e pedidos:
        o que foi registrado, o que confere e o que precisa ser
        investigado antes de virar informação para o negócio.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<hr class="dq-rule">',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 6. Indicadores gerais
# --------------------------------------------------

total_compras = len(compras)

valor_registrado = compras["valor_total"].sum()

total_clientes = compras["cliente_id"].nunique()

total_problemas = int(
    (validacao["situacao"] != "OK").sum()
)

col1, col2, col3, col4 = st.columns(4)

indicadores = [
    (col1, "Compras analisadas", f"{total_compras:,}"),
    (
        col2,
        "Valor registrado",
        f"R$ {valor_registrado:,.2f}".replace(",", "X")
        .replace(".", ",").replace("X", ".")
    ),
    (col3, "Clientes identificados", f"{total_clientes:,}"),
    (col4, "Registros para revisar", f"{total_problemas:,}")
]

for coluna, rotulo, valor in indicadores:
    with coluna:
        st.markdown(
            f"""
            <div class="dq-kpi">
                <div class="dq-kpi-label">{rotulo}</div>
                <div class="dq-kpi-value">{valor}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption(
    "O valor registrado corresponde à soma das compras. "
    "Não representa necessariamente receita confirmada."
)


# --------------------------------------------------
# 7. Filtros
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.subheader("Explorar compras")

st.markdown(
    '<p class="dq-section-note">'
    'Combine os filtros para analisar um recorte dos registros.'
    '</p>',
    unsafe_allow_html=True
)

col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

with col_filtro1:
    clientes = sorted(
        compras["cliente_id"].dropna().unique().tolist()
    )

    cliente_selecionado = st.selectbox(
        "Cliente",
        options=["Todos"] + clientes,
        format_func=lambda x: "Todos os clientes" if x == "Todos"
        else str(x)
    )

with col_filtro2:
    metodos = sorted(
        compras["metodo_pagamento"]
        .dropna()
        .unique()
        .tolist()
    )

    metodo_selecionado = st.selectbox(
        "Pagamento",
        options=["Todos"] + metodos,
        format_func=lambda x: "Todos os métodos" if x == "Todos"
        else str(x)
    )

with col_filtro3:
    maior_valor = float(
        compras["valor_total"].max()
    ) if not compras.empty else 0.0

    valor_minimo = st.number_input(
        "Valor mínimo (R$)",
        min_value=0.0,
        max_value=max(maior_valor, 0.0),
        value=0.0,
        step=50.0
    )

compras_filtradas = compras.copy()

if cliente_selecionado != "Todos":
    compras_filtradas = compras_filtradas[
        compras_filtradas["cliente_id"] == cliente_selecionado
    ]

if metodo_selecionado != "Todos":
    compras_filtradas = compras_filtradas[
        compras_filtradas["metodo_pagamento"] == metodo_selecionado
    ]

compras_filtradas = compras_filtradas[
    compras_filtradas["valor_total"] >= valor_minimo
]

st.caption(
    f"{len(compras_filtradas)} de {len(compras)} compras "
    "correspondem aos filtros selecionados."
)


# --------------------------------------------------
# 8. Visualizações
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.subheader("Movimento das compras")

grafico1, grafico2 = st.columns(2)

with grafico1:
    resumo_pagamentos = (
        compras_filtradas
        .groupby("metodo_pagamento")
        .size()
        .reset_index(name="quantidade")
        .sort_values("quantidade", ascending=True)
    )

    if resumo_pagamentos.empty:
        st.info("Não há compras para os filtros selecionados.")
    else:
        fig_pagamentos = px.bar(
            resumo_pagamentos,
            x="quantidade",
            y="metodo_pagamento",
            orientation="h",
            text="quantidade",
            color_discrete_sequence=["#B84F73",
                                     "#D59AAF",
                                     "#8F6677"],
            title="Compras por forma de pagamento",
            labels={
                "quantidade": "Número de compras",
                "metodo_pagamento": "Forma de pagamento"
            }
        )

        fig_pagamentos.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_pagamentos.update_layout(
            showlegend=False,
            margin=dict(l=5, r=25, t=55, b=10),
            yaxis_title=None,
            xaxis_title=None,
            bargap=0.48
        )

        st.plotly_chart(
            fig_pagamentos,
            use_container_width=True,
            theme="streamlit"
        )

with grafico2:
    resumo_datas = (
        compras_filtradas
        .dropna(subset=["data_compra"])
        .groupby("data_compra", as_index=False)["valor_total"]
        .sum()
        .sort_values("data_compra")
    )

    if resumo_datas.empty:
        st.info("Não há datas disponíveis para esse recorte.")
    else:
        fig_receita = px.line(
            resumo_datas,
            x="data_compra",
            y="valor_total",
            markers=True,
            title="Valor registrado ao longo do tempo",
            labels={
                "data_compra": "Data",
                "valor_total": "Valor registrado (R$)"
            }
        )

        fig_receita.update_traces(
            line=dict(color="#B84F73", width=2.5),
            marker=dict(size=7, color="#B84F73")
        )

        fig_receita.update_layout(
            margin=dict(l=5, r=15, t=55, b=10),
            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(
            fig_receita,
            use_container_width=True,
            theme="streamlit"
        )


# --------------------------------------------------
# 9. Produtos
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.subheader("Produtos")

st.markdown(
    '<p class="dq-section-note">'
    'Quantidade total registrada por produto nos pedidos processados.'
    '</p>',
    unsafe_allow_html=True
)

resumo_produtos = (
    pedidos
    .groupby("produto_id", as_index=False)["quantidade"]
    .sum()
    .sort_values("quantidade", ascending=True)
)

if resumo_produtos.empty:
    st.info("Não há produtos disponíveis para análise.")
else:
    fig_produtos = px.bar(
        resumo_produtos,
        x="quantidade",
        y="produto_id",
        orientation="h",
        text="quantidade",
        color_discrete_sequence=["#C9859D"],
        labels={
            "produto_id": "Produto",
            "quantidade": "Unidades"
        }
    )

    fig_produtos.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig_produtos.update_layout(
        showlegend=False,
        margin=dict(l=5, r=25, t=15, b=10),
        xaxis_title=None,
        yaxis_title=None,
        bargap=0.4
    )

    st.plotly_chart(
        fig_produtos,
        use_container_width=True,
        theme="streamlit"
    )


# --------------------------------------------------
# 10. Detalhamento
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.subheader("Registros de compras")

tabela_compras = compras_filtradas.copy()

tabela_compras["data_compra"] = (
    tabela_compras["data_compra"].dt.strftime("%d/%m/%Y")
)

tabela_compras["valor_total"] = tabela_compras[
    "valor_total"
].map(
    lambda x: (
        f"R$ {x:,.2f}".replace(",", "X")
        .replace(".", ",").replace("X", ".")
        if pd.notna(x) else "Não informado"
    )
)

st.dataframe(
    tabela_compras,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 11. Qualidade e alertas
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.subheader("Pontos para investigar")

problemas = validacao[
    validacao["situacao"] != "OK"
].copy()

if problemas.empty:
    st.markdown(
        """
        <div class="dq-status">
            Não foram identificados registros sinalizados pela
            validação atual. Isso não significa, por si só, que
            todos os dados estejam livres de problemas.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class="dq-status">
            <strong>{len(problemas)} registro(s)</strong> precisam
            de revisão. Confira as informações abaixo antes de
            considerar os valores como confirmados.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        problemas,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 12. Rodapé
# --------------------------------------------------

st.markdown('<hr class="dq-rule">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="dq-footer">
        Projeto demonstrativo de qualidade de dados.
        Processamento com PySpark; visualização com Python,
        Pandas, Streamlit e Plotly.<br>
        Os dados são ilustrativos. Registros sem pedidos associados
        exigem investigação antes de qualquer conclusão financeira.
    </div>
    """,
    unsafe_allow_html=True
)
