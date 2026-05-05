import pandas as pd

df = pd.read_csv("arquivos_entrada/arquivo.csv")

# remover separadores de milhar
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.replace('.', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)

# exportar com formatação
with pd.ExcelWriter("arquivos_saida/arquivo_tratado.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Dados')

    worksheet = writer.sheets['Dados']

    # ajustar largura das colunas automaticamente
    for col in worksheet.columns:
        max_length = 0
        col_letter = col[0].column_letter  # letra da coluna

        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = max_length + 2  # espaço extra
        worksheet.column_dimensions[col_letter].width = adjusted_width