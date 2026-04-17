[![Licença](https://img.shields.io/badge/licença-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![CI](https://github.com/AndreBFarias/TerritorialGuard/actions/workflows/ci.yml/badge.svg)](https://github.com/AndreBFarias/TerritorialGuard/actions/workflows/ci.yml)

# TerritorialGuard

Ferramenta de diagnóstico automático para dashboards territoriais em Looker Studio / BigQuery.

Dado um município, varre todas as tabelas do dashboard no BigQuery, identifica métricas zeradas e diagnostica a causa: dado ausente na fonte ou problema no JOIN/filtro do dbt.

## Requisitos

- Python 3.10+
- Acesso ao projeto BigQuery configurado
- Arquivo de credenciais da service account (keyfile JSON)

## Instalação

```bash
chmod +x install.sh
./install.sh
```

Ou manualmente:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
# Validacao completa de um municipio
.venv/bin/territorialguard --municipio "Andradina - SP"

# Com ano especifico
.venv/bin/territorialguard --municipio "Andradina - SP" --ano 2025

# Com verificacao upstream (identifica onde o dado se perdeu)
.venv/bin/territorialguard --municipio "Andradina - SP" --upstream

# Completo: ano + upstream
.venv/bin/territorialguard --municipio "Andradina - SP" --ano 2025 --upstream

# Estimar custo sem executar
.venv/bin/territorialguard --municipio "Andradina - SP" --dry-run

# Gerar template xlsx sem executar queries
.venv/bin/territorialguard --gerar-template

# Saida em arquivo especifico
.venv/bin/territorialguard --municipio "Andradina - SP" -o resultado.xlsx
```

Modo módulo:

```bash
.venv/bin/python -m territorialguard.main --municipio "Andradina - SP"
```

## Saida

O script gera um arquivo `.xlsx` com abas Input/Output/Guia:

- **Input**: métricas mapeadas (página do dashboard, tabela BQ, expressão SQL)
- **Output**: resultado da validação (valor retornado, status, diagnóstico, upstream)

### Status possíveis

| Status | Significado |
|--------|-------------|
| OK | Dados presentes e com valor > 0 |
| ZERO_LEGITIMO | Zero confirmado na fonte (município não participa do programa) |
| ZERO_SUSPEITO | Dado existe na fonte mas sumiu no painel (possível bug) |
| AUSENTE | Município não encontrado na tabela |
| NULL | Métrica retornou NULL |
| ERRO | Erro na execução da query |

### Colunas upstream (com flag `--upstream`)

| Coluna | Significado |
|--------|-------------|
| fonte_upstream | Tabelas fonte consultadas e contagens |
| registros_upstream | Total de registros nas fontes |
| diagnostico_upstream | ZERO_CONFIRMADO_FONTE / PERDEU_NO_PAINEL / VALOR_ZERADO |
| camada_falha | Onde o dado se perdeu (nenhuma / painel / política) |

## Configuração

Editar `src/territorialguard/config.py`:

- `PROJETO_BQ`: projeto BigQuery
- `KEYFILE`: caminho do arquivo de credenciais
- `ANO_PADRAO`: ano para filtro (padrão: 2025)
- `LIMITE_BYTES_SESSAO`: limite de custo por sessão (padrão: 500 MB)

## Testes

```bash
.venv/bin/pytest tests/ -v
```

## Estrutura

```
TerritorialGuard/
  src/territorialguard/
    main.py               # Ponto de entrada (CLI)
    validador.py          # Core: queries, execucao, classificacao
    executor_bq.py        # Cliente BigQuery
    metricas.py           # Definicao das metricas do dashboard
    linhagem.py           # Mapeamento upstream (fontes de dados)
    relatorio.py          # Geracao de xlsx e output terminal
    config.py             # Configuracao
  tests/                  # Testes pytest
  .github/workflows/      # CI
  pyproject.toml          # Metadados, dependencias, ruff, pytest
  requirements.txt        # Dependencias legadas
  install.sh              # Instalacao do venv
  uninstall.sh            # Remocao do venv
  data/                   # Logs, xlsx e relatorios gerados
  contexto/               # Guias do projeto dbt (referencia)
  sprints/                # Documentacao de sprints
```

## Desinstalação

```bash
./uninstall.sh
```

## Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md) e [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Segurança

Veja [SECURITY.md](SECURITY.md). Nunca commite credenciais (`credentials/*.json`).

## Licença

GPL v3 -- ver [LICENSE](LICENSE).

---

*"Cada município é um universo de dados aguardando para ser ouvido."*
