import sys
from pathlib import Path

from pyspark.sql import SparkSession

PROJETO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJETO / "src"))

from processamento import validar_compras


def test_compra_com_valor_correto():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("TesteDataQuality")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    try:
        compras = spark.createDataFrame(
            [(1, 101, "2026-01-01", 20.0, "Pix")],
            [
                "id_compra",
                "cliente_id",
                "data_compra",
                "valor_total",
                "metodo_pagamento",
            ],
        )

        pedidos = spark.createDataFrame(
            [(1, 1, "A001", 2, 10.0)],
            [
                "id_pedido",
                "id_compra",
                "produto_id",
                "quantidade",
                "preco_unitario",
            ],
        )

        resultado = validar_compras(compras, pedidos)
        situacao = resultado.collect()[0]["situacao"]

        assert situacao == "OK"

    finally:
        spark.stop()


def test_compra_sem_pedidos_associados():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("TesteCompraSemPedidos")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    try:
        compras = spark.createDataFrame(
            [(5, 104, "2026-01-05", 500.0, "Pix")],
            [
                "id_compra",
                "cliente_id",
                "data_compra",
                "valor_total",
                "metodo_pagamento",
            ],
        )

        from pyspark.sql.types import (
            StructType, StructField, IntegerType, StringType, DoubleType
        )

        esquema_pedidos = StructType([
            StructField("id_pedido", IntegerType(), True),
            StructField("id_compra", IntegerType(), True),
            StructField("produto_id", StringType(), True),
            StructField("quantidade", IntegerType(), True),
            StructField("preco_unitario", DoubleType(), True),
        ])

        pedidos = spark.createDataFrame([], esquema_pedidos)

        resultado = validar_compras(compras, pedidos)
        situacao = resultado.collect()[0]["situacao"]

        assert situacao == "SEM PEDIDOS ASSOCIADOS"

    finally:
        spark.stop()


def test_compra_com_valor_divergente():
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("TesteValorDivergente")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    try:
        compras = spark.createDataFrame(
            [(3, 103, "2026-01-03", 100.0, "Cartão")],
            [
                "id_compra",
                "cliente_id",
                "data_compra",
                "valor_total",
                "metodo_pagamento",
            ],
        )

        pedidos = spark.createDataFrame(
            [(1, 3, "A001", 2, 40.0)],
            [
                "id_pedido",
                "id_compra",
                "produto_id",
                "quantidade",
                "preco_unitario",
            ],
        )

        resultado = validar_compras(compras, pedidos)
        situacao = resultado.collect()[0]["situacao"]

        assert situacao == "VALOR DIVERGENTE"

    finally:
        spark.stop()
