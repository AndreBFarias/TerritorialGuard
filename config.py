"""Configuracao do validador de cidades."""

from pathlib import Path

PROJETO_BQ = "br-mec-segape-dev"
KEYFILE = Path(__file__).parent / "credentials" / "service_account.json"
TIMEOUT_SEGUNDOS = 60
LIMITE_BYTES_SESSAO = 500 * 1024 * 1024  # 500 MB

DIRETORIO_PROJETO = Path(__file__).parent
ARQUIVO_XLSX = DIRETORIO_PROJETO / "data" / "Projeto_Validador_Visão_Municipal.xlsx"
DIRETORIO_DATA = DIRETORIO_PROJETO / "data"

ANO_PADRAO = 2025

# "A ordem natural das coisas nao e determinada pela desordem do acaso, mas pelo rigor da razao." - Baruch Spinoza
