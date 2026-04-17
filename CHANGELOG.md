# Changelog

## [2.0.0] - 2026-04-16

### Mudado
- Projeto renomeado de `validador_cidades` para `TerritorialGuard` (sprint S20 do portfólio)
- Código reorganizado em `src/territorialguard/` (pacote Python com layout src)
- Imports convertidos para relativos dentro do pacote
- Entry point via `territorialguard` (configurado em pyproject.toml)

### Adicionado
- `pyproject.toml` com metadados, dependências pinadas, ruff e pytest
- `tests/` com 13 testes (parsear_municipio, classificar_upstream, METRICAS)
- `.github/workflows/ci.yml` com ruff + pytest
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- `.mailmap` para unificação de identidade

## [1.0.0] - 2026-04-06

### Adicionado
- Validador de métricas territoriais em BigQuery
- Modo direto (CLI) e interativo
- Diagnóstico upstream (identifica onde o dado se perdeu)
- Geração de relatórios XLSX com abas Input/Output/Guia
- Suporte a filtros por ano e município
