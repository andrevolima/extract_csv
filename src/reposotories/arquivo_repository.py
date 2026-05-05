import pandas as pd


def buscar_arquivos_csv(pasta_entrada):
    return sorted(pasta_entrada.glob("*.csv"))


def ler_arquivo_csv(caminho_arquivo):
    return pd.read_csv(caminho_arquivo)


def salvar_arquivo_csv(dataframe, caminho_arquivo):
    dataframe.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")


def salvar_arquivo_excel(dataframe, caminho_arquivo):
    with pd.ExcelWriter(caminho_arquivo, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Dados")

        worksheet = writer.sheets["Dados"]

        for coluna in worksheet.columns:
            tamanho_maximo = 0
            letra_coluna = coluna[0].column_letter

            for celula in coluna:
                if celula.value:
                    tamanho_maximo = max(tamanho_maximo, len(str(celula.value)))

            worksheet.column_dimensions[letra_coluna].width = tamanho_maximo + 2
