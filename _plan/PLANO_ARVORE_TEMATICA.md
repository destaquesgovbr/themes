# Plano de Melhoria da Árvore Temática DestaquesGovBr

**Criado em:** 2025-12-17
**Última atualização:** 2025-12-17
**Status:** Em execução - Fase 0

---

## 1. Contexto e Motivação

### Problema Atual
- Árvore com **25 temas L1**, **~113 L2**, **~400+ L3** (~540 nós totais)
- **Desbalanceamento extremo:** Meio Ambiente (2101 notícias, 15.5%) vs Estatísticas (6 notícias, 0.04%) = razão 350:1
- Temas muito específicos ou faltantes em algumas áreas
- Classificação atual usa **apenas nome do tema** (sem descrições)
- Processo de classificação pode ser enviesado

### Objetivos
1. **Revisar estrutura** da árvore (remover/adicionar/reorganizar temas)
2. **Adicionar descrições** otimizadas para RAG + LLM
3. Criar **processo metódico e faseado** com documentação

### Arquivos Principais
- `themes/themes_tree.yaml` - Árvore temática principal
- `scraper/src/enrichment/themes_tree.yaml` - Cópia usada pelo scraper
- `scraper/src/enrichment/themes_tree.json` - Versão JSON

---

## 2. Estratégia: Abordagem Híbrida (L1 → L3 → L2)

| Fase | Foco | Status | Descrição |
|------|------|--------|-----------|
| **0** | Diagnóstico | EM ANDAMENTO | Coletar dados de distribuição L1/L2/L3 |
| **1** | L1 + Estrutura | PENDENTE | Revisar estrutura + descrições dos 25 temas |
| **2** | L3 | PENDENTE | Descrições dos ~400 temas folha |
| **3** | L2 | PENDENTE | Descrições ponte (~110 temas) |
| **4** | Validação | PENDENTE | Testes e ajustes finais |

---

## 3. Detalhamento das Fases

### Fase 0: Análise e Diagnóstico

**Objetivo:** Coletar dados para informar decisões estruturais

**Tarefas:**
- [ ] Consultar Typesense para distribuição por tema L1
- [ ] Consultar Typesense para distribuição por tema L2
- [ ] Consultar Typesense para distribuição por tema L3
- [ ] Identificar temas com volume zero ou muito baixo (<10 notícias)
- [ ] Identificar temas sobrecarregados (>5% do total)
- [ ] Analisar sobreposições semânticas entre temas
- [ ] Gerar relatório de diagnóstico

**Entregáveis:**
- `DIAGNOSTICO_DISTRIBUICAO.md` - Relatório com estatísticas
- `DECISOES_ESTRUTURAIS.md` - Registro de decisões

---

### Fase 1: Revisão Estrutural + Descrições L1

**Objetivo:** Ajustar estrutura e definir fronteiras claras dos temas principais

#### Parte A: Revisão Estrutural

**Critérios para remoção/fusão:**
- Temas com <1% das notícias que podem ser absorvidos
- Temas com sobreposição semântica significativa

**Candidatos identificados (dados preliminares):**
| Tema | Notícias | % | Ação Sugerida |
|------|----------|---|---------------|
| Estatísticas e Dados Públicos | 6 | 0.04% | Avaliar fusão |
| Eventos Oficiais e Cerimônias | 33 | 0.2% | Avaliar fusão |
| Defesa e Forças Armadas | 38 | 0.3% | Manter, revisar subtemas |

**Critérios para divisão:**
- Temas com >15% que são heterogêneos

| Tema | Notícias | % | Ação Sugerida |
|------|----------|---|---------------|
| Meio Ambiente e Sustentabilidade | 2101 | 15.5% | Avaliar subdivisão |

#### Parte B: Descrições L1

**Tarefas por tema L1:**
- [ ] 01 - Economia e Finanças
- [ ] 02 - Educação
- [ ] 03 - Saúde
- [ ] 04 - Segurança Pública
- [ ] 05 - Meio Ambiente e Sustentabilidade
- [ ] 06 - Ciência, Tecnologia e Inovação
- [ ] 07 - Infraestrutura e Transportes
- [ ] 08 - Cultura, Artes e Patrimônio
- [ ] 09 - Esportes e Lazer
- [ ] 10 - Agricultura, Pecuária e Abastecimento
- [ ] 11 - Indústria e Comércio
- [ ] 12 - Relações Internacionais e Diplomacia
- [ ] 13 - Justiça e Direitos Humanos
- [ ] 14 - Trabalho e Emprego
- [ ] 15 - Desenvolvimento Social
- [ ] 16 - Turismo
- [ ] 17 - Energia e Recursos Minerais
- [ ] 18 - Comunicações e Mídia
- [ ] 19 - Defesa e Forças Armadas
- [ ] 20 - Políticas Públicas e Governança
- [ ] 21 - Legislação e Regulamentação
- [ ] 22 - Eventos Oficiais e Cerimônias
- [ ] 23 - Estatísticas e Dados Públicos
- [ ] 24 - Minorias e Grupos Especiais
- [ ] 25 - Habitação e Urbanismo

---

### Fase 2: Descrições L3 (Temas Folha)

**Objetivo:** Máxima especificidade para classificação precisa

**Estratégia:** Um subagente por tema L1 para evitar bias e manter qualidade constante.

**Contagem de L3 por tema L1:**

| Tema | L3 | Complexidade |
|------|-----|--------------|
| 01 - Economia | 22 | Média |
| 02 - Educação | 14 | Baixa |
| 03 - Saúde | 18 | Média |
| 04 - Segurança | 20 | Média |
| 05 - Meio Ambiente | 14 | Baixa |
| 06 - C&T&I | 15 | Baixa |
| 07 - Infraestrutura | 25 | Alta |
| 08 - Cultura | 27 | Alta |
| 09 - Esportes | 25 | Alta |
| 10 - Agricultura | 15 | Baixa |
| 11 - Indústria | 25 | Alta |
| 12 - Rel. Internacionais | 22 | Média |
| 13 - Justiça | 9 | Baixa |
| 14 - Trabalho | 25 | Alta |
| 15 - Desenv. Social | 12 | Baixa |
| 16 - Turismo | 20 | Média |
| 17 - Energia | 25 | Alta |
| 18 - Comunicações | 15 | Baixa |
| 19 - Defesa | 25 | Alta |
| 20 - Políticas Públicas | 14 | Baixa |
| 21 - Legislação | 20 | Média |
| 22 - Minorias | 19 | Média |
| 23 - Habitação | 24 | Alta |
| **Total** | **~450** | |

**Execução em Lotes Paralelos:**
- Lote 1: Temas 01, 02, 03, 04, 05, 06 (6 paralelos)
- Lote 2: Temas 07, 08, 09, 10, 11, 12 (6 paralelos)
- Lote 3: Temas 13, 14, 15, 16, 17, 18 (6 paralelos)
- Lote 4: Temas 19, 20, 21, 22, 23 (5 paralelos)

**Progresso por Tema:**

| Código | Tema | Status | Notas |
|--------|------|--------|-------|
| 01 | Economia e Finanças | ⬜ Pendente | |
| 02 | Educação | ⬜ Pendente | |
| 03 | Saúde | ⬜ Pendente | |
| 04 | Segurança Pública | ⬜ Pendente | |
| 05 | Meio Ambiente | ⬜ Pendente | |
| 06 | C&T&I | ⬜ Pendente | |
| 07 | Infraestrutura | ⬜ Pendente | |
| 08 | Cultura | ⬜ Pendente | |
| 09 | Esportes | ⬜ Pendente | |
| 10 | Agricultura | ⬜ Pendente | |
| 11 | Indústria | ⬜ Pendente | |
| 12 | Rel. Internacionais | ⬜ Pendente | |
| 13 | Justiça | ⬜ Pendente | |
| 14 | Trabalho | ⬜ Pendente | |
| 15 | Desenv. Social | ⬜ Pendente | |
| 16 | Turismo | ⬜ Pendente | |
| 17 | Energia | ⬜ Pendente | |
| 18 | Comunicações | ⬜ Pendente | |
| 19 | Defesa | ⬜ Pendente | |
| 20 | Políticas Públicas | ⬜ Pendente | |
| 21 | Legislação | ⬜ Pendente | |
| 22 | Minorias | ⬜ Pendente | |
| 23 | Habitação | ⬜ Pendente | |

**Arquivo de Progresso:** `PROGRESSO_DESCRICOES.md`

---

### Fase 3: Descrições L2 (Ponte)

**Objetivo:** Criar ponte semântica entre L1 e L3

**Abordagem:**
- Derivar de L1 (herda escopo) + resumir L3 (agrega especificidades)

**Progresso:** Ver arquivo `PROGRESSO_L2.md`

---

### Fase 4: Validação e Ajustes

**Tarefas:**
- [ ] Validar YAML (sintaxe, estrutura)
- [ ] Verificar cobertura de keywords
- [ ] Testar classificação com amostra de notícias
- [ ] Ajustar descrições baseado em erros
- [ ] Sincronizar entre repositórios

---

## 4. Formato Final do YAML

```yaml
themes:
  - code: "01"
    label: "Economia e Finanças"
    description: |
      Políticas econômicas, fiscais e monetárias do governo federal.
      Inclui gestão de recursos públicos, investimentos, comércio exterior
      e regulação do sistema financeiro.
    keywords:
      - economia
      - finanças
      - fiscal
      - tributário
      - investimento
    includes:
      - Políticas de incentivo econômico
      - Regulação bancária e financeira
    excludes:
      - Programas sociais (ver Desenvolvimento Social)
      - Turismo econômico (ver Turismo)
    children:
      - code: "01.01"
        label: "Política Econômica"
        description: "..."
        keywords: [...]
        children:
          - code: "01.01.01"
            label: "Política Fiscal"
            description: "..."
            keywords: [...]
            examples:
              - "Governo anuncia novo arcabouço fiscal"
              - "Congresso aprova LOA 2025"
```

---

## 5. Conexão Typesense (para consultas)

```json
{
  "host": "34.39.186.38",
  "port": 8108,
  "protocol": "http",
  "collection": "news",
  "searchOnlyApiKey": "060758cdd81ae52c92067f2083b79783d7eb6ad195d3638130247b77aca21232"
}
```

---

## 6. Histórico de Execução

| Data | Fase | Ação | Resultado |
|------|------|------|-----------|
| 2025-12-17 | 0 | Criação do plano | Documentos criados |
| 2025-12-17 | 0 | Consulta distribuição L1 | Ver DIAGNOSTICO |

---

## 7. Referências

- [Documentação do projeto](../docs/)
- [Scraper - classificação](../scraper/src/enrichment/)
- [Portal - temas](../portal/src/lib/)
