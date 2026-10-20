
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# 1. Localizar a pasta dos dados
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "dados"


# 2. Criar a sessão do Spark
def criar_spark():
    spark = (
        SparkSession.builder
        .appName("DataQualityDashboard")
        .getOrCreate()
    )
    return spark


# 3. Ler os arquivos CSV
def carregar_dados(spark):
    compras = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(PASTA_DADOS / "compras.csv"))
    )

    pedidos = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(PASTA_DADOS / "pedidos.csv"))
    )

    return compras, pedidos


# 4. Remover linhas duplicadas
def limpar_dados(compras, pedidos):
    compras_limpo = compras.dropDuplicates()
    pedidos_limpo = pedidos.dropDuplicates()

    return compras_limpo, pedidos_limpo


# 5. Conferir os valores das compras
def validar_compras(compras_limpo, pedidos_limpo):

    # Calcular o valor dos itens de cada compra
    valores_pedidos = (
        pedidos_limpo
        .withColumn(
            "subtotal",
            F.col("quantidade") * F.col("preco_unitario")
        )
        .groupBy("id_compra")
        .agg(
            F.round(F.sum("subtotal"), 2)
            .alias("valor_calculado")
        )
    )

    # Comparar o valor calculado com o valor registrado
    validacao = (
        compras_limpo
        .join(valores_pedidos, on="id_compra", how="left")
        .withColumn(
            "situacao",
            F.when(
                F.col("valor_calculado").isNull(),
                "SEM PEDIDOS ASSOCIADOS"
            )
            .when(
                F.abs(
                    F.col("valor_total") - F.col("valor_calculado")
                ) > 0.01,
                "VALOR DIVERGENTE"
            )
            .otherwise("OK")
        )
    )

    return validacao


# 6. Executar o processamento completo
def executar_processamento():
    spark = criar_spark()

    compras, pedidos = carregar_dados(spark)

    compras_limpo, pedidos_limpo = limpar_dados(
        compras, pedidos
    )

    validacao = validar_compras(
        compras_limpo, pedidos_limpo
    )

    return {
        "spark": spark,
        "compras_originais": compras,
        "pedidos_originais": pedidos,
        "compras_limpo": compras_limpo,
        "pedidos_limpo": pedidos_limpo,
        "validacao": validacao
    }
