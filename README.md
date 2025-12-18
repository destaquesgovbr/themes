# Árvore Temática DestaquesGovBr

Este diretório contém a árvore temática (vocabulário controlado) utilizada para classificar notícias do governo federal brasileiro no projeto DestaquesGovBr.

---

## Arquivos

### Árvore Temática
- **`themes_tree.yaml`** - Árvore temática atual (apenas códigos e nomes)
- **`themes_tree_enriched.yaml`** - *(Em construção)* Árvore com descrições, keywords e exemplos

### Documentação do Projeto de Melhoria
- **`PLANO_ARVORE_TEMATICA.md`** - Plano mestre com fases e tarefas
- **`DIAGNOSTICO_DISTRIBUICAO.md`** - Análise de distribuição de notícias por tema
- **`DECISOES_ESTRUTURAIS.md`** - Registro de decisões sobre estrutura da árvore
- **`TEMPLATE_DESCRICOES.md`** - Template e critérios para escrever descrições

---

## Estrutura da Árvore

A árvore possui **3 níveis hierárquicos**:

```
Nível 1 (25 temas)     → Nível 2 (~113 subtemas)    → Nível 3 (~400 tópicos)
01 - Economia          → 01.01 - Pol. Econômica    → 01.01.01 - Pol. Fiscal
                       → 01.02 - Fiscalização      → 01.02.01 - Fisc. Econômica
02 - Educação          → 02.01 - Ensino Básico     → 02.01.01 - Ed. Infantil
```

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
curl -s "http://34.39.186.38:8108/collections/news/documents/search?q=*&query_by=title&facet_by=theme_1_level_1_label&per_page=0&max_facet_values=30" \
  -H "X-TYPESENSE-API-KEY: 060758cdd81ae52c92067f2083b79783d7eb6ad195d3638130247b77aca21232"
```

---

## Sincronização com Outros Repositórios

A árvore temática precisa estar sincronizada em:

| Local | Arquivo | Uso |
|-------|---------|-----|
| themes/ | `themes_tree.yaml` | Fonte de verdade |
| scraper/src/enrichment/ | `themes_tree.yaml` | Classificação LLM |
| scraper/src/enrichment/ | `themes_tree.json` | Estrutura programática |
| portal/src/lib/ | `themes.yaml` | Navegação no portal |

Após alterações na árvore, sincronizar manualmente para todos os locais.
