# Sprint S22 -- Higienização do TerritorialGuard (3/10 -> 10/10)

**Projeto:** TerritorialGuard (ex-validador_cidades)
**Data:** 2026-04-16
**Saúde anterior:** 3/10 (parcial: LICENSE GPLv3 já existia de sprint anterior)
**Saúde final:** 10/10

---

## Escopo

Reorganização em `src/territorialguard/` (layout src), criação de `pyproject.toml`, adição de testes `pytest`, CI GitHub Actions, documentação comunitária.

---

## Entregas

### Estrutura
- [x] `src/territorialguard/` com `__init__.py`
- [x] 7 módulos movidos da raiz (main, validador, executor_bq, metricas, linhagem, relatorio, config)
- [x] Imports convertidos para relativos (`from . import config`, etc)
- [x] Entry point configurado em pyproject (`territorialguard = territorialguard.main:main`)

### Testes
- [x] `tests/test_validador.py` (4 testes: parsear_municipio)
- [x] `tests/test_linhagem.py` (6 testes: classificar_upstream)
- [x] `tests/test_metricas.py` (3 testes: shape de METRICAS e INSTRUCOES_DASHBOARD)
- **Total: 13 testes**

### Documentação
- [x] `README.md` atualizado com nova estrutura e entry point
- [x] `CONTRIBUTING.md`
- [x] `CODE_OF_CONDUCT.md`
- [x] `SECURITY.md` (com alerta sobre keyfile de service account)
- [x] `CHANGELOG.md` com entrada 2.0.0

### Metadata
- [x] `pyproject.toml` com deps pinadas, ruff, pytest, script entrypoint
- [x] `.mailmap`

### CI/CD
- [x] `.github/workflows/ci.yml` (ruff + pytest)

### Packaging
- [x] `install.sh` atualizado para `pip install -e .` (pyproject-driven)

---

## 13/13 completos

---

*"Cada municipio e um universo de dados aguardando para ser ouvido."*
