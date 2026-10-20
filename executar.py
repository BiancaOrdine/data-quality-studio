from pathlib import Path
from src.processamento import executar_processamento

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_SAIDA = PASTA_PROJETO / "dados_processados"


def salvar_csv(dataframe, nome_arquivo):
    caminho = PASTA_SAIDA / nome_arquivo

    (
        dataframe
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(str(caminho.parent / f"temporario_{nome_arquivo}"))
    )

    import shutil

    pasta_temporaria = caminho.parent / f"temporario_{nome_arquivo}"
    arquivos_csv = list(pasta_temporaria.glob("part-*.csv"))

    if not arquivos_csv:
        raise RuntimeError(f"Nenhum CSV foi gerado para {nome_arquivo}")

    if caminho.exists():
        caminho.unlink()

    shutil.copy2(arquivos_csv[0], caminho)
    shutil.rmtree(pasta_temporaria)


def main():
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    resultado = executar_processamento()

    try:
        salvar_csv(resultado["compras_limpo"], "compras_limpo.csv")
        salvar_csv(resultado["pedidos_limpo"], "pedidos_limpo.csv")
        salvar_csv(resultado["validacao"], "validacao.csv")

        print("Processamento concluído!")
        print(f"Compras originais: {resultado['compras_originais'].count()}")
        print(f"Compras após limpeza: {resultado['compras_limpo'].count()}")
        print(f"Pedidos originais: {resultado['pedidos_originais'].count()}")
        print(f"Pedidos após limpeza: {resultado['pedidos_limpo'].count()}")
        print("\\nValidação das compras:")
        resultado["validacao"].select(
            "id_compra", "valor_total", "valor_calculado", "situacao"
        ).show(truncate=False)

    finally:
        resultado["spark"].stop()


if __name__ == "__main__":
    main()
