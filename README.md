# Árvore Temática DestaquesGovBr

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Este diretório contém a árvore temática (vocabulário controlado) utilizada para classificar notícias do governo federal brasileiro no projeto DestaquesGovBr.

---

## Arquivos

### Árvore Temática (versão 3.2)
- **`themes_tree_enriched_full.yaml`** - Fonte de verdade: L1, L2 e L3 com descrições, keywords, includes/excludes e exemplos. É a origem da tabela `themes` do banco.
- **`themes_tree.yaml`** - A mesma árvore, só com códigos e nomes (lida pelo `activitypub-server`).
- **`themes_tree_enriched.yaml`** - Só os L1, com os mesmos textos do arquivo completo.

Os três arquivos têm os mesmos códigos e labels; `tests/test_themes_tree.py` garante isso no CI.

### Documentação do Projeto de Melhoria (`_plan/`)
- **`PLANO_ARVORE_TEMATICA.md`** - Plano mestre com fases e tarefas
- **`DIAGNOSTICO_DISTRIBUICAO.md`** - Análise de distribuição de notícias por tema
- **`DECISOES_ESTRUTURAIS.md`** - Registro de decisões sobre estrutura da árvore (DEC-001 a DEC-006)
- **`TEMPLATE_DESCRICOES.md`** - Template e critérios para escrever descrições

---

## Estrutura da Árvore

A árvore possui **3 níveis hierárquicos** (589 códigos na versão 3.2):

```
Nível 1 (24 temas)     → Nível 2 (106 subtemas)     → Nível 3 (459 tópicos)
01 - Economia          → 01.01 - Pol. Econômica    → 01.01.01 - Pol. Fiscal
                       → 01.02 - Fiscalização      → 01.02.01 - Fisc. Econômica
02 - Educação          → 02.01 - Ensino Básico     → 02.01.01 - Ed. Infantil
```

Os códigos L1 são 01–21, 24, 25 e 26. Os códigos 22 e 23 foram retirados (DEC-001/DEC-002) e não são reutilizados, porque cópias antigas da árvore ainda os usam com outro significado.

Nos YAML estruturados, os códigos L1 e L2 ficam sempre entre aspas (`'08'`, `'26.01'`), para nenhum parser lê-los como número.

---

## Histórico de versões

| Versão | Data | Mudança |
|--------|------|---------|
| 3.2 | 2026-10-21 | Novo L1 **26 - Defesa Civil e Gestão de Desastres** (DEC-006): 19.03 → 26.01 e 19.04 → 26.02, com os L3 renumerados e os mesmos labels. O 19 fica só com defesa militar. Termos de Defesa Civil saem de 05.02.01 e 15.02.03. `themes_tree.yaml` perde os 22 e 23 legados, e `themes_tree_enriched.yaml` passa a usar 24 e 25 (como o banco). |
| 3.1 | 2025-12-18 | Árvore completa com descrições L1, L2 e L3; temas 22 e 23 removidos (DEC-001/DEC-002). |
| 2.0 | 2025-12-18 | Descrições L1 (`themes_tree_enriched.yaml`). |

---

## Validação

```bash
python3 -m venv .venv
.venv/bin/pip install -r tests/requirements.txt
.venv/bin/pytest -q tests
```

Os testes conferem: carga com PyYAML, contagens por nível, códigos únicos, pais coerentes, alinhamento entre os três arquivos e o contrato do tema 26.

---

## Status do Projeto de Melhoria

| Fase | Descrição | Status |
|------|-----------|--------|
| 0 | Diagnóstico e análise de dados | EM ANDAMENTO |
| 1 | Revisão estrutural + Descrições L1 | PENDENTE |
| 2 | Descrições L3 (temas folha) | PENDENTE |
| 3 | Descrições L2 (ponte) | PENDENTE |
| 4 | Validação e ajustes | PENDENTE |

---

## Como Consultar Distribuição de Notícias

```bash
# Typesense - consulta facets por tema L1
# IMPORTANTE: Use variável de ambiente, NUNCA hardcode a chave API
curl -s "http://34.39.186.38:8108/collections/news/documents/search?q=*&query_by=title&facet_by=theme_1_level_1_label&per_page=0&max_facet_values=30" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}"
```

---

## Sincronização com Outros Repositórios

A árvore precisa estar sincronizada em:

| Local | Arquivo | Uso |
|-------|---------|-----|
| themes/ | `themes_tree_enriched_full.yaml` | Fonte de verdade |
| data-platform | tabela `themes` (Postgres) | Lida pelo classificador (`data-science/src/news_enrichment/taxonomy.py`) e pela API |
| data-platform | `test-data/themes_tree_enriched_full.yaml` | Cópia byte a byte do full, usada nos testes (sha256 fixado) |
| activitypub-server | `scripts/seed-actors.ts` | Lê os L1 de `themes_tree.yaml` |
| clipping | `data/themes.yaml` | Prompt do agente do clipping (cópia) |
| portal | `src/config/themes.yaml`, `src/data/themes.ts` | Navegação, ícones e descrições |
| telegram-bot | `src/telegram_bot/data.py` | Lista de temas |

Após alterações na árvore, sincronizar manualmente para todos os locais.

**test-data do data-platform:** é cópia byte a byte do `themes_tree_enriched_full.yaml` daqui; o conteúdo não se edita lá. O `tests/unit/test_themes_test_data.py` do data-platform fixa o sha256 do arquivo (`SHA256_THEMES_FULL`). Ao mudar o full, copie o arquivo sem reformatar (`cp themes_tree_enriched_full.yaml ../data-platform/test-data/`) e troque o hash, aqui e no data-platform, pelo de `shasum -a 256 themes_tree_enriched_full.yaml` (o `tests/test_themes_tree.py` falha enquanto o README tiver o hash antigo). Na 3.2, o hash é `32a2fa43149ecd6bb1e8f5b26a341b3ee1b539750eb0c5d35120b2e2a32c92b0`.

**Banco:** mudanças de estrutura entram por migração no data-platform (o tema 26 entra pela `034`, com remap auditado das notícias). **Nunca** rode `scripts/populate_themes.py` em produção: ele faz `DELETE FROM themes` e reinsere tudo com ids novos.
