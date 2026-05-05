import pandas as pd


def somar_tempos(coluna_tempo):
    tempos_convertidos = pd.to_timedelta(coluna_tempo, errors="coerce")
    return tempos_convertidos.sum()


def transformar_tempo_em_texto(tempo):
    total_segundos = int(tempo.total_seconds())

    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
