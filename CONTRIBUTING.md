# Guia de Contribuição -- TerritorialGuard

## Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commits seguindo Conventional Commits em PT-BR
4. Abra um Pull Request

## Padrão de Commits

```
tipo: descricao imperativa em PT-BR

Tipos: feat, fix, refactor, docs, test, perf, chore, style, ci, build
```

### Regras

- Idioma: PT-BR com acentuação correta
- Zero emojis
- Zero menções a ferramentas de IA
- Subject curto (~50 chars), body em 72 chars

## Padrão de Código

- Type hints sempre
- `logging` rotacionado (nunca `print()` em código de produção)
- Paths relativos via `pathlib.Path`
- Error handling explícito
- Limite de 800 linhas por arquivo

## Configuração do Ambiente

```bash
git clone https://github.com/AndreBFarias/TerritorialGuard.git
cd TerritorialGuard
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Testes

```bash
pytest tests/ -v
```

## Lint

```bash
ruff check src tests
```

## Processo de Review

1. Abra PR contra `main`
2. CI precisa estar verde
3. Aguarde revisão do mantenedor
4. Merge após aprovação
