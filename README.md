# Extract CSV

Projeto em Python para tratar arquivos CSV de atividades esportivas, mantendo apenas as colunas importantes e gerando um resumo no terminal.

O sistema le os arquivos da pasta `arquivos_entrada`, cria uma versao tratada na pasta `arquivos_saida` e mostra informacoes como quantidade de atividades, volume total de treino e duracao total.

## Colunas utilizadas

O projeto mantem apenas estas colunas:

- `Activity Type`
- `Date`
- `Distance`
- `Time`
- `Moving Time`
- `Avg HR`
- `Calories`
- `Aerobic TE`
- `Training Stress Score(R)`
- `Avg Pace`
- `Avg Power`
- `Normalized Power(R) (NP(R))`
- `Total Ascent`
- `Steps`

No CSV original, algumas dessas colunas podem aparecer com o simbolo `R` registrado. O codigo normaliza esse nome antes de tratar os dados.

## Informacoes exibidas no terminal

Depois de processar cada planilha, o sistema mostra:

- Nome do arquivo processado
- Atleta, quando existir no CSV
- Mes ou meses de referencia
- Quantidade de atividades realizadas
- Volume total de treino
- Duracao total das atividades
- Tempo total em movimento
- Caminho dos arquivos tratados gerados

## Estrutura do projeto

```text
Extract_csv/
|-- arquivos_entrada/
|   `-- arquivo.csv
|-- arquivos_saida/
|   |-- arquivo_tratado.csv
|   `-- arquivo_tratado.xlsx
|-- src/
|   |-- extract_csv.py
|   |-- reposotories/
|   |   `-- arquivo_repository.py
|   |-- services/
|   |   `-- atividade_service.py
|   `-- utils/
|       `-- tempo_utils.py
|-- requirements.txt
`-- README.md
```

## Como instalar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

## Como usar

1. Coloque os arquivos `.csv` dentro da pasta `arquivos_entrada`.
2. Execute o script principal:

```powershell
python src\extract_csv.py
```

3. Veja o resumo no terminal.
4. Confira os arquivos tratados na pasta `arquivos_saida`.

## Exemplo de saida no terminal

```text
Arquivo processado: arquivo
Atleta: Nao identificado no CSV
Mes de referencia: 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04
Quantidade de atividades: 40
Volume total de treino: 234.10 km
Duracao total das atividades: 22:53:17
Tempo total em movimento: 21:56:07
CSV tratado: C:\Users\Dell\Documents\Extract_csv\arquivos_saida\arquivo_tratado.csv
Excel tratado: C:\Users\Dell\Documents\Extract_csv\arquivos_saida\arquivo_tratado.xlsx
```

## Dependencias

O projeto usa:

- `pandas`
- `openpyxl`

Essas dependencias estao listadas no arquivo `requirements.txt`.

## Observacoes

- O projeto processa todos os arquivos `.csv` encontrados em `arquivos_entrada`.
- O atleta so sera identificado se o CSV tiver uma coluna chamada `Athlete` ou `Atleta`.
- Os arquivos tratados sao gerados em dois formatos: `.csv` e `.xlsx`.
