from pathlib import Path

from services.atividade_service import processar_planilhas


PASTA_RAIZ = Path(__file__).resolve().parent.parent
PASTA_ENTRADA = PASTA_RAIZ / "arquivos_entrada"
PASTA_SAIDA = PASTA_RAIZ / "arquivos_saida"


def main():
    processar_planilhas(PASTA_ENTRADA, PASTA_SAIDA)


if __name__ == "__main__":
    main()
