import pandas as pd

from reposotories.arquivo_repository import (
    buscar_arquivos_csv,
    ler_arquivo_csv,
    salvar_arquivo_csv,
    salvar_arquivo_excel,
)
from utils.tempo_utils import somar_tempos, transformar_tempo_em_texto


COLUNAS_NECESSARIAS = [
    "Activity Type",
    "Date",
    "Distance",
    "Time",
    "Moving Time",
    "Avg HR",
    "Calories",
    "Aerobic TE",
    "Training Stress Score®",
    "Avg Pace",
    "Avg Power",
    "Normalized Power® (NP®)",
    "Total Ascent",
    "Steps",
]

COLUNAS_NUMERICAS = [
    "Distance",
    "Avg HR",
    "Calories",
    "Aerobic TE",
    "Training Stress Score®",
    "Avg Power",
    "Normalized Power® (NP®)",
    "Total Ascent",
    "Steps",
]


def processar_planilhas(pasta_entrada, pasta_saida):
    pasta_saida.mkdir(exist_ok=True)

    arquivos_csv = buscar_arquivos_csv(pasta_entrada)

    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado na pasta arquivos_entrada.")
        return

    for arquivo_csv in arquivos_csv:
        dataframe_original = ler_arquivo_csv(arquivo_csv)
        dataframe_tratado = tratar_dataframe(dataframe_original)
        resumo_planilha = montar_resumo_planilha(dataframe_tratado, dataframe_original, arquivo_csv.stem)

        caminho_csv_saida = pasta_saida / f"{arquivo_csv.stem}_tratado.csv"
        caminho_excel_saida = pasta_saida / f"{arquivo_csv.stem}_tratado.xlsx"

        salvar_arquivo_csv(dataframe_tratado, caminho_csv_saida)
        salvar_arquivo_excel(dataframe_tratado, caminho_excel_saida)

        mostrar_resumo_no_terminal(resumo_planilha, caminho_csv_saida, caminho_excel_saida)


def tratar_dataframe(dataframe):
    dataframe = dataframe.copy()
    dataframe.columns = normalizar_nomes_das_colunas(dataframe.columns)

    for nome_coluna in COLUNAS_NECESSARIAS:
        if nome_coluna not in dataframe.columns:
            dataframe[nome_coluna] = None

    dataframe_tratado = dataframe[COLUNAS_NECESSARIAS].copy()
    dataframe_tratado["Date"] = pd.to_datetime(dataframe_tratado["Date"], errors="coerce")

    for nome_coluna in COLUNAS_NUMERICAS:
        dataframe_tratado[nome_coluna] = converter_coluna_para_numero(dataframe_tratado[nome_coluna])

    return dataframe_tratado


def normalizar_nomes_das_colunas(colunas):
    colunas_normalizadas = []

    for nome_coluna in colunas:
        nome_coluna = nome_coluna.strip()
        nome_coluna = nome_coluna.replace("Â®", "®")
        colunas_normalizadas.append(nome_coluna)

    return colunas_normalizadas


def converter_coluna_para_numero(coluna):
    coluna = coluna.astype(str)
    coluna = coluna.str.replace(",", "", regex=False)
    coluna = coluna.str.replace("--", "", regex=False)

    return pd.to_numeric(coluna, errors="coerce")


def montar_resumo_planilha(dataframe_tratado, dataframe_original, nome_arquivo):
    atleta = identificar_atleta(dataframe_original)
    meses_referencia = identificar_meses_referencia(dataframe_tratado)
    quantidade_atividades = len(dataframe_tratado)
    volume_total_treino = dataframe_tratado["Distance"].sum()
    duracao_total_atividades = somar_tempos(dataframe_tratado["Time"])
    duracao_total_movimento = somar_tempos(dataframe_tratado["Moving Time"])

    return {
        "nome_arquivo": nome_arquivo,
        "atleta": atleta,
        "meses_referencia": meses_referencia,
        "quantidade_atividades": quantidade_atividades,
        "volume_total_treino": volume_total_treino,
        "duracao_total_atividades": duracao_total_atividades,
        "duracao_total_movimento": duracao_total_movimento,
    }


def identificar_atleta(dataframe_original):
    dataframe_original = dataframe_original.copy()
    dataframe_original.columns = normalizar_nomes_das_colunas(dataframe_original.columns)

    if "Athlete" in dataframe_original.columns:
        return dataframe_original["Athlete"].dropna().astype(str).iloc[0]

    if "Atleta" in dataframe_original.columns:
        return dataframe_original["Atleta"].dropna().astype(str).iloc[0]

    return "Nao identificado no CSV"


def identificar_meses_referencia(dataframe_tratado):
    datas_validas = dataframe_tratado["Date"].dropna()

    if datas_validas.empty:
        return "Nao identificado"

    meses = datas_validas.dt.strftime("%Y-%m").unique()
    meses = sorted(meses)

    return ", ".join(meses)


def mostrar_resumo_no_terminal(resumo_planilha, caminho_csv_saida, caminho_excel_saida):
    print("")
    print(f"Arquivo processado: {resumo_planilha['nome_arquivo']}")
    print(f"Atleta: {resumo_planilha['atleta']}")
    print(f"Mes de referencia: {resumo_planilha['meses_referencia']}")
    print(f"Quantidade de atividades: {resumo_planilha['quantidade_atividades']}")
    print(f"Volume total de treino: {resumo_planilha['volume_total_treino']:.2f} km")
    print(f"Duracao total das atividades: {transformar_tempo_em_texto(resumo_planilha['duracao_total_atividades'])}")
    print(f"Tempo total em movimento: {transformar_tempo_em_texto(resumo_planilha['duracao_total_movimento'])}")
    print(f"CSV tratado: {caminho_csv_saida}")
    print(f"Excel tratado: {caminho_excel_saida}")
