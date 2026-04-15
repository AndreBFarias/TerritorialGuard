# Auditoria de Producao - Validador de Cidades
# Data: 2026-04-06
# Escopo: codigo, organizacao, acentuacao, logica, devops

---

## 1. Problemas Criticos

### 1.1 Arquivo validador.py com 1.193 linhas (limite: 800)
- **Regra violada**: CLAUDE.md define 800 linhas por arquivo
- **Correcao**: extrair METRICAS para `metricas.py`, instrucoes para `instrucoes.py`, xlsx para `relatorio.py`

### 1.2 Instrucoes do dashboard desatualizadas
- Chaves "FUNDEB Repasse" e "Salario Educacao Repasse" no dict `_gerar_instrucoes_dashboard`
  nao correspondem aos nomes atuais "FUNDEB Repasse (Realizado)" e "Salario Educacao Repasse (Realizado)"
- Instrucoes de Selecoes ainda mencionam "triplicado por duplicacao" ja corrigido
- **Impacto**: coluna `o_que_preciso_do_dashboard` fica vazia para essas metricas

### 1.3 Bug no classificador upstream (linhagem.py)
- Quando `registros_painel > 0` e `valor = 0` e `total_upstream = 0`:
  retorna INCONCLUSIVO mas deveria ser ZERO_CONFIRMADO_FONTE
- Afeta: Pronatec, Mulheres Mil, FIES

### 1.4 Variavel nao utilizada em _resolver_id_municipio
- `cidade, uf = _parsear_municipio(municipio)` — `cidade` e `uf` nunca usados

---

## 2. Problemas de Organizacao

### 2.1 Falta .gitignore
- .venv/, __pycache__/, data/*.log, *.xlsx nao estao ignorados
- Risco: commitar venv ou credenciais acidentalmente

### 2.2 inventario.csv obsoleto na raiz
- Arquivo da Sprint 1, substituido pelo xlsx em data/
- Deve ser removido

### 2.3 queries_originais/ e schemas_originais/ vazios
- Sprint 1 nunca concluiu essas copias
- Remover pastas vazias ou popular

### 2.4 install.sh referencia validador.py (deve ser main.py apos refatoracao)

---

## 3. Acentuacao PT-BR

### Regra: CLAUDE.md exige acentuacao correta em TODOS os arquivos

**Arquivos sem acentuacao (precisa corrigir):**
- config.py: docstring "Configuracao" -> "Configuracao" (ok, e nome de modulo, nao descricao)
- executor_bq.py: "validacao", "execucao" -> com acento nos comentarios
- linhagem.py: "Mapeamento", "linhagem", "Inscricoes" -> com acento
- validador.py: todas as docstrings e comentarios
- README.md: "Instalacao", "Configuracao", "diagnostico" -> com acento
- Todos os sprints/*.md: sem acentos

**Nota**: nomes de variaveis e funcoes em Python ficam sem acento (padrao tecnico).
Somente strings visiveis ao usuario, docstrings, comentarios e documentacao precisam de acento.

---

## 4. Logica do Codigo

### 4.1 SQL Injection (risco baixo)
- `_construir_where` usa f-strings com input do usuario
- Para ferramenta interna e aceitavel, mas adicionar nota

### 4.2 Tratamento de erro generico no executor
- `except Exception` em `tabela_existe()` engole todos os erros
- Deveria logar o erro antes de retornar False

### 4.3 Import circular potencial
- `executar_validacao` faz `from linhagem import ...` dentro da funcao
- Funciona mas e um code smell. Apos refatoracao, o import fica no topo

---

## 5. DevOps

### 5.1 Falta .gitignore (critico)
### 5.2 Falta .env.example com variaveis necessarias
### 5.3 requirements.txt sem versoes pinadas
- `>=3.14.0` permite updates que podem quebrar
- Para producao, pinar versoes exatas

### 5.4 Sem testes automatizados
- Aceitavel para v1 de ferramenta interna

---

## 6. Plano de Correcao

| # | Acao | Prioridade |
|---|------|-----------|
| 1 | Criar .gitignore | CRITICA |
| 2 | Refatorar validador.py em modulos (<800 linhas cada) | CRITICA |
| 3 | Corrigir chaves do dict de instrucoes | ALTA |
| 4 | Corrigir bug INCONCLUSIVO no classificador upstream | ALTA |
| 5 | Remover variavel nao utilizada | MEDIA |
| 6 | Corrigir acentuacao em todos os .md e docstrings | MEDIA |
| 7 | Remover inventario.csv obsoleto | BAIXA |
| 8 | Remover pastas vazias (queries_originais, schemas_originais) | BAIXA |
| 9 | Pinar versoes no requirements.txt | BAIXA |
| 10 | Atualizar README com estrutura final | MEDIA |
