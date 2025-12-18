# Fase 4: Validação e Testes de Classificação - Plano Detalhado

**Criado em:** 2025-12-18
**Versão:** 1.0
**Responsável:** Equipe de Refinamento Temático

---

## Contexto do Projeto

### Status Atual (2025-12-18)
- **Fase 0 (Diagnóstico):** ✅ CONCLUÍDA
- **Fase 1 (Descrições L1):** ✅ CONCLUÍDA - 23 temas
- **Fase 2 (Descrições L3):** ✅ CONCLUÍDA - 459 categorias folha
- **Fase 3 (Descrições L2):** ✅ CONCLUÍDA - 106 subtemas
- **Fase 4 (Validação e Testes):** ⬜ EM PLANEJAMENTO

### Resultado das Fases Anteriores
**Arquivo principal:** `themes_tree_enriched_full.yaml`
- **Estrutura:** 23 temas L1 → 106 subtemas L2 → 459 categorias L3
- **Total:** 588 descrições completas (100% de cobertura)
- **Tamanho:** 10.669 linhas
- **Commit:** 3d182d0 (pushed para GitHub)

### Objetivo da Fase 4
Validar a qualidade e efetividade da árvore temática enriquecida para classificação automática de notícias governamentais brasileiras, garantindo:
1. Consistência estrutural e semântica
2. Qualidade das descrições e keywords
3. Performance de classificação em casos reais
4. Identificação e correção de problemas

---

## Fase 4: Subfases Detalhadas

### **Subfase 4.1: Validação de Consistência Estrutural**

**Objetivo:** Garantir integridade técnica da estrutura YAML e hierarquia da árvore

**Atividades:**

1. **Validação YAML**
   - Validar sintaxe YAML do arquivo principal
   - Verificar encoding UTF-8
   - Testar parsing sem erros

2. **Validação de Unicidade**
   - Verificar que todos os códigos (L1, L2, L3) são únicos
   - Detectar duplicações de labels
   - Identificar inconsistências de numeração

3. **Validação de Hierarquia**
   - Verificar que todos os L2 têm pai L1 válido
   - Verificar que todos os L3 têm pai L2 válido
   - Confirmar que não há órfãos ou referências quebradas

4. **Validação de Campos Obrigatórios**
   - Todos os nós têm `code`, `label`, `description`?
   - Todos têm `keywords` com pelo menos 5 termos?
   - L1 têm `includes` e `excludes`?

5. **Estatísticas de Completude**
   - Gerar relatório com contagens por nível
   - Verificar distribuição (L2 por L1, L3 por L2)
   - Identificar desequilíbrios significativos

**Scripts:**
- `scripts/validacao/01_validate_structure.py`

**Output esperado:**
- `reports/01_estrutura_report.md`
- `reports/01_estrutura_stats.json`

---

### **Subfase 4.2: Validação de Qualidade das Descrições**

**Objetivo:** Avaliar qualidade semântica e consistência das descrições em todos os níveis

**Atividades:**

1. **Análise de Tamanho e Complexidade**
   - Verificar comprimento das descrições (L1 > L2 > L3 esperado)
   - Contar palavras por descrição
   - Identificar descrições muito curtas (<30 palavras) ou longas (>200 palavras)

2. **Análise de Sobreposição Semântica**
   - Usar embeddings (sentence-transformers) para calcular similaridade
   - Identificar irmãos L2 com descrições muito similares (>0.85 similaridade)
   - Identificar irmãos L3 com descrições muito similares
   - Detectar redundâncias conceituais

3. **Análise de Keywords**
   - Verificar quantidade de keywords (mínimo 5, recomendado 8-15)
   - Detectar keywords genéricas demais (ex: "Brasil", "governo")
   - Identificar keywords duplicadas entre irmãos
   - Verificar cobertura de termos técnicos e coloquiais

4. **Análise de Includes/Excludes (L1)**
   - Verificar consistência entre description e includes/excludes
   - Detectar contradições lógicas
   - Validar que excludes referenciam temas existentes

5. **Revisão Ortográfica e Gramatical**
   - Executar corretor ortográfico (languagetool ou similar)
   - Verificar uso consistente de maiúsculas/minúsculas
   - Detectar siglas sem expansão na primeira menção

**Scripts:**
- `scripts/validacao/02_validate_quality.py`
- `scripts/validacao/02_analyze_similarity.py`
- `scripts/validacao/02_check_keywords.py`

**Output esperado:**
- `reports/02_qualidade_report.md`
- `reports/02_problemas_qualidade.csv`
- `reports/02_similarity_matrix_L2.png`
- `reports/02_similarity_matrix_L3.png`

---

### **Subfase 4.3: Preparação de Dataset de Teste**

**Objetivo:** Criar conjunto robusto de casos de teste para validar classificação

**⚠️ DECISÃO IMPORTANTE: Estratégia de Entrada**

Testaremos 3 abordagens para classificação:

| Estratégia | Input | Vantagens | Desvantagens |
|------------|-------|-----------|--------------|
| **A. Título apenas** | Título da notícia | Rápido, simula cenário de preview | Menos contexto, pode ser ambíguo |
| **B. Resumo apenas** | Resumo da notícia (se disponível) | Balanço entre velocidade e contexto | Nem todas notícias têm resumo |
| **C. Conteúdo completo** | Texto completo | Máximo contexto, melhor precisão | Mais lento, pode ter ruído |
| **D. Título + Resumo** | Concatenação de título e resumo | Combina keywords e contexto | Dependente de qualidade do resumo |
| **E. Título + Início do conteúdo** | Título + primeiros 500 chars | Não depende de resumo | Pode cortar informação relevante |

**Recomendação inicial:** Testar todas as 5 estratégias e comparar performance.

**Atividades:**

1. **Coleta de Notícias Reais**
   - Extrair amostra de 500-1000 notícias do scraper/Typesense
   - Garantir que temos título, resumo E conteúdo completo
   - Cobrir período de 3-6 meses para diversidade temporal
   - Garantir distribuição por órgãos governamentais diversos

2. **Estratificação por Complexidade**
   - **Casos claros (40%):** Títulos com tema óbvio
   - **Casos moderados (40%):** Notícias que podem se encaixar em 2-3 temas
   - **Casos difíceis (20%):** Notícias ambíguos ou multi-temáticas

3. **Anotação Manual (Ground Truth)**
   - Classificar manualmente cada notícia em L1, L2 e L3
   - Ler título + resumo + início do conteúdo para decisão
   - Permitir classificação múltipla quando aplicável
   - Documentar nível de confiança (alta/média/baixa)
   - Ter pelo menos 2 anotadores para casos ambíguos

4. **Casos de Borda e Negativos**
   - Criar casos sintéticos de temas não cobertos
   - Adicionar títulos de outras áreas (esportes, entretenimento)
   - Testar robustez contra títulos fora do escopo governamental

5. **Documentação de Critérios**
   - Registrar regras de desambiguação usadas
   - Documentar casos limítrofes e como foram resolvidos
   - Criar guia de classificação para referência futura

**Scripts:**
- `scripts/dataset/03_collect_news.py` - Extrai notícias do Typesense
- `scripts/dataset/03_annotation_app.py` - Interface Streamlit para anotação
- `scripts/dataset/03_validate_annotations.py` - Valida consistência

**Output esperado:**
- `data/test_dataset.csv`
  - Colunas: `id`, `titulo`, `resumo`, `conteudo`, `fonte`, `data`, `url`, `L1_true`, `L2_true`, `L3_true`, `confianca`, `anotador`, `multi_label`
- `reports/03_classification_guide.md`
- `reports/03_dataset_stats.md`
- `reports/03_inter_annotator_agreement.md` (se múltiplos anotadores)

---

### **Subfase 4.4: Testes de Classificação Comparativos**

**Objetivo:** Implementar e testar classificador baseado em similaridade semântica com diferentes estratégias de entrada

**Atividades:**

1. **Implementação do Classificador Base**
   - Criar embeddings de todas as descrições (L1, L2, L3)
   - Implementar busca por similaridade cosine
   - Permitir classificação hierárquica (L1 → L2 → L3)
   - Implementar threshold de confiança ajustável

2. **Estratégias de Entrada (5 variações)**
   Para cada notícia do dataset de teste:
   - **A:** Embedding do título
   - **B:** Embedding do resumo
   - **C:** Embedding do conteúdo completo (ou primeiros 2000 tokens)
   - **D:** Embedding da concatenação título + resumo
   - **E:** Embedding da concatenação título + início do conteúdo (500 chars)

3. **Estratégias de Classificação (4 variações)**
   Para cada estratégia de entrada acima:
   - **Estratégia 1:** Flat (comparar input com todos os L3 diretamente)
   - **Estratégia 2:** Hierárquica (L1 primeiro, depois L2, depois L3)
   - **Estratégia 3:** Ensemble (combinar descrição + keywords pesados)
   - **Estratégia 4:** Multi-label (permitir múltiplos temas)

   **Total:** 5 inputs × 4 estratégias = 20 combinações a testar

4. **Execução dos Testes**
   - Rodar cada combinação no dataset de teste
   - Registrar top-1, top-3, top-5 predictions
   - Calcular tempo de inferência por notícia
   - Gerar embeddings em batch para otimização

5. **Cálculo de Métricas**
   - **Por nível (L1, L2, L3):**
     - Acurácia (top-1, top-3, top-5)
     - Precision, Recall, F1-score
     - Matriz de confusão
   - **Global:**
     - Acurácia hierárquica (L1 correto E L2 correto E L3 correto)
     - Taxa de classificação multi-label
     - Coverage (% de casos com confiança > threshold)
   - **Por estratégia de entrada:**
     - Ranking das 5 estratégias (A-E) por acurácia
     - Tempo médio de inferência
     - Trade-off precisão vs. velocidade

6. **Análise de Erros**
   - Identificar temas com maior taxa de erro
   - Listar pares de temas frequentemente confundidos
   - Analisar casos onde top-1 estava errado mas top-3 continha correto
   - Comparar erros entre estratégias (ex: erros em A mas acertos em C)

**Scripts:**
- `scripts/classificacao/04_classifier.py` - Classe principal do classificador
- `scripts/classificacao/04_run_tests.py` - Executa todas as combinações
- `scripts/classificacao/04_calculate_metrics.py` - Calcula métricas
- `scripts/classificacao/04_analyze_errors.py` - Análise de erros
- `scripts/classificacao/utils.py` - Funções auxiliares

**Output esperado:**
- `reports/04_classification_results.md` - Relatório consolidado
- `reports/04_metrics_summary.json` - Métricas de todas as combinações
- `reports/04_best_strategy_recommendation.md` - Recomendação da melhor combinação
- `reports/04_confusion_matrices/` - Matrizes de confusão por combinação
  - `L1_strategy_A_hierarchical.png`
  - `L2_strategy_C_flat.png`
  - etc.
- `reports/04_classification_errors.csv` - Detalhes dos erros
- `reports/04_confused_pairs.csv` - Pares frequentemente confundidos
- `reports/04_performance_comparison.png` - Gráfico comparativo

---

### **Subfase 4.5: Análise de Resultados e Ajustes Iterativos**

**Objetivo:** Identificar e corrigir problemas baseado nos resultados dos testes

**Atividades:**

1. **Seleção da Melhor Estratégia**
   - Analisar resultados das 20 combinações
   - Escolher estratégia de entrada vencedora (A-E)
   - Escolher estratégia de classificação vencedora (1-4)
   - Justificar escolha (trade-off precisão vs. velocidade vs. disponibilidade de dados)

2. **Priorização de Problemas**
   - Ranquear temas por taxa de erro (piores primeiro)
   - Identificar padrões comuns nos erros
   - Separar problemas de descrição vs. problemas de ambiguidade inerente

3. **Análise de Confusões**
   - Para cada par frequentemente confundido:
     - Comparar descrições lado a lado
     - Identificar keywords sobrepostas
     - Sugerir ajustes para diferenciação

4. **Refinamento de Descrições**
   - **Ação 1:** Adicionar termos distintivos a temas confundidos
   - **Ação 2:** Melhorar keywords com termos mais específicos
   - **Ação 3:** Expandir descrições que são muito curtas
   - **Ação 4:** Adicionar campo `examples` com trechos reais de notícias

5. **Refinamento de Excludes (L1)**
   - Adicionar referências explícitas a temas frequentemente confundidos
   - Esclarecer fronteiras semânticas entre temas adjacentes

6. **Testes Incrementais**
   - Após cada rodada de ajustes, re-testar apenas temas modificados
   - Validar que ajustes melhoram performance sem regredir outros temas
   - Documentar impacto de cada mudança

7. **Critério de Parada**
   - Acurácia L1 > 85%
   - Acurácia L2 > 70%
   - Acurácia L3 > 60%
   - OU máximo de 3 iterações de ajuste

**Scripts:**
- `scripts/refinamento/05_analyze_confusions.py` - Analisa confusões
- `scripts/refinamento/05_suggest_fixes.py` - Sugere melhorias automáticas
- `scripts/refinamento/05_apply_fixes.py` - Aplica mudanças ao YAML
- `scripts/refinamento/05_retest_themes.py` - Re-testa temas ajustados

**Output esperado:**
- `reports/05_ajustes_realizados.md` - Log de todas as mudanças
- `themes_tree_enriched_full.yaml` (versão 3.2+) - Arquivo atualizado
- `reports/05_improvements.md` - Comparação antes/depois por tema
- `reports/05_iteration_log.md` - Histórico de iterações
- `reports/05_final_metrics.json` - Métricas finais pós-ajustes

---

### **Subfase 4.6: Documentação Final e Entrega**

**Objetivo:** Consolidar resultados e preparar documentação para uso em produção

**Atividades:**

1. **Relatório de Validação Final**
   - Sumário executivo com principais métricas
   - Descrição do processo de validação
   - Principais problemas encontrados e resolvidos
   - Limitações conhecidas da árvore temática
   - Recomendações para uso em produção

2. **Guia de Uso da Árvore Temática**
   - Como interpretar a hierarquia
   - Como usar descrições, keywords e examples
   - Quando usar classificação hierárquica vs. flat
   - Como lidar com multi-label
   - Thresholds recomendados de confiança
   - **Estratégia de entrada recomendada** (título/resumo/conteúdo)

3. **Exemplos de Classificação**
   - Criar notebook Jupyter com exemplos práticos
   - Incluir código de classificação pronto para uso
   - Demonstrar casos claros, ambíguos e limítrofes
   - Mostrar interpretação de scores de confiança
   - Comparar diferentes estratégias de entrada

4. **Benchmark de Performance**
   - Documentar tempo de inferência por estratégia
   - Requisitos de hardware/memória
   - Comparação de modelos de embedding testados
   - Recomendações de otimização

5. **Entrega de Artefatos**
   - Arquivos finais organizados em `_plan_refinamento/`
   - README.md explicando estrutura de pastas
   - Script de exemplo para classificação
   - Dados de teste (anonimizados se necessário)

**Documentação:**
- `reports/06_RELATORIO_VALIDACAO_FINAL.md`
- `reports/06_GUIA_USO_ARVORE_TEMATICA.md`
- `notebooks/06_classification_examples.ipynb`
- `reports/06_performance_benchmark.md`
- `README.md`

---

## Estrutura de Diretórios

```
/Users/nitai/Dropbox/dev-mgi/destaquesgovbr/themes/_plan_refinamento/
├── FASE_4_DETALHAMENTO.md                 # Este arquivo
├── README.md                               # Visão geral e instruções
├── requirements.txt                        # Dependências Python
├── .python-version                         # Python 3.13
│
├── scripts/                                # Scripts Python organizados
│   ├── __init__.py
│   ├── config.py                          # Configurações globais
│   ├── utils/                             # Utilitários compartilhados
│   │   ├── __init__.py
│   │   ├── yaml_utils.py
│   │   ├── embedding_utils.py
│   │   └── metrics_utils.py
│   │
│   ├── validacao/                         # Subfase 4.1 e 4.2
│   │   ├── __init__.py
│   │   ├── 01_validate_structure.py
│   │   ├── 02_validate_quality.py
│   │   ├── 02_analyze_similarity.py
│   │   └── 02_check_keywords.py
│   │
│   ├── dataset/                           # Subfase 4.3
│   │   ├── __init__.py
│   │   ├── 03_collect_news.py
│   │   ├── 03_annotation_app.py
│   │   └── 03_validate_annotations.py
│   │
│   ├── classificacao/                     # Subfase 4.4
│   │   ├── __init__.py
│   │   ├── 04_classifier.py
│   │   ├── 04_run_tests.py
│   │   ├── 04_calculate_metrics.py
│   │   └── 04_analyze_errors.py
│   │
│   └── refinamento/                       # Subfase 4.5
│       ├── __init__.py
│       ├── 05_analyze_confusions.py
│       ├── 05_suggest_fixes.py
│       ├── 05_apply_fixes.py
│       └── 05_retest_themes.py
│
├── data/                                   # Dados gerados
│   ├── test_dataset.csv
│   ├── embeddings_cache/                  # Cache de embeddings
│   └── annotations/                       # Anotações manuais
│
├── reports/                                # Relatórios gerados
│   ├── 01_estrutura_report.md
│   ├── 01_estrutura_stats.json
│   ├── 02_qualidade_report.md
│   ├── 02_problemas_qualidade.csv
│   ├── 02_similarity_matrix_L2.png
│   ├── 02_similarity_matrix_L3.png
│   ├── 03_classification_guide.md
│   ├── 03_dataset_stats.md
│   ├── 04_classification_results.md
│   ├── 04_metrics_summary.json
│   ├── 04_best_strategy_recommendation.md
│   ├── 04_confusion_matrices/
│   ├── 04_classification_errors.csv
│   ├── 04_confused_pairs.csv
│   ├── 04_performance_comparison.png
│   ├── 05_ajustes_realizados.md
│   ├── 05_improvements.md
│   ├── 05_iteration_log.md
│   ├── 05_final_metrics.json
│   ├── 06_RELATORIO_VALIDACAO_FINAL.md
│   ├── 06_GUIA_USO_ARVORE_TEMATICA.md
│   └── 06_performance_benchmark.md
│
└── notebooks/                              # Jupyter notebooks
    └── 06_classification_examples.ipynb
```

---

## Ambiente de Desenvolvimento

### Virtual Environment

**Importante:** Usar o ambiente Poetry já configurado:

```bash
# Ativar virtual env
source /Users/nitai/Library/Caches/pypoetry/virtualenvs/govbr-news-ai-_H0Lmpg7-py3.13/bin/activate

# Verificar Python
python --version  # Deve ser 3.13.x

# Instalar dependências
cd /Users/nitai/Dropbox/dev-mgi/destaquesgovbr/themes/_plan_refinamento
pip install -r requirements.txt
```

### Dependências Python

```txt
# Core
pyyaml>=6.0
python-dotenv>=1.0.0

# Machine Learning
sentence-transformers>=2.2.0
torch>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.0.0

# Visualização
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0

# NLP e Validação
language-tool-python>=2.8.0
spacy>=3.7.0

# Interface e Notebooks
streamlit>=1.28.0
jupyter>=1.0.0
ipywidgets>=8.1.0

# Typesense (para coleta de notícias)
typesense>=0.16.0

# Utilidades
tqdm>=4.66.0
click>=8.1.0
colorama>=0.4.6
```

### Requisitos de Hardware
- **CPU:** Mínimo 4 cores (para embeddings)
- **RAM:** Mínimo 8GB (modelo de embeddings + dados)
- **Disco:** ~2GB para modelos e outputs
- **GPU:** Opcional, mas acelera geração de embeddings (10-50x mais rápido)

---

## Decisões de Design

### 1. Modelo de Embeddings
**Escolha:** `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`

**Razões:**
- Multilingual (suporta português)
- Bom equilíbrio entre performance e velocidade
- 768 dimensões (não muito grande)
- Amplamente usado e validado

**Alternativas a testar se necessário:**
- `neuralmind/bert-base-portuguese-cased` (BERTimbau)
- `sentence-transformers/distiluse-base-multilingual-cased-v2` (mais rápido)

### 2. Estratégia de Classificação Padrão
**Escolha:** Hierárquica (após testes comparativos)

**Justificativa:**
- Classifica L1 primeiro (mais confiável)
- Depois L2 dentro do L1 escolhido
- Finalmente L3 dentro do L2 escolhido
- Reduz espaço de busca e melhora precisão

### 3. Estratégia de Entrada
**Escolha:** A ser determinada na Subfase 4.4

**Hipótese inicial:** Estratégia D (título + resumo) deve ter melhor trade-off

**Razões:**
- Título contém keywords principais
- Resumo adiciona contexto sem excesso de ruído
- Mais rápido que conteúdo completo
- Mais informativo que apenas título

### 4. Threshold de Confiança
**Padrão:** 0.5 (ajustável por nível)

- L1: threshold 0.4 (mais permissivo, menos risco)
- L2: threshold 0.5 (padrão)
- L3: threshold 0.6 (mais conservador, pode retornar "indefinido")

### 5. Multi-label
**Permitir até 3 temas simultâneos**
- Útil para notícias que cruzam áreas
- Requer score > 0.4 para labels secundários
- Score primário deve ser > 0.5

---

## Cronograma Estimado

| Subfase | Descrição | Tempo Estimado | Complexidade |
|---------|-----------|----------------|--------------|
| 4.1 | Validação Estrutural | 2-3h | Baixa |
| 4.2 | Validação Qualidade | 4-6h | Média |
| 4.3 | Dataset de Teste | 6-8h | Alta (anotação manual) |
| 4.4 | Testes Classificação | 6-8h | Média-Alta (20 combinações) |
| 4.5 | Análise e Ajustes | 6-10h | Alta (iterativo) |
| 4.6 | Documentação Final | 3-4h | Baixa |
| **Total** | | **27-39h** | |

**Nota:** Tempo aumentado de 25-37h para 27-39h devido aos testes comparativos de entrada.

---

## Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Baixa acurácia de classificação (<60% L1) | Alto | Média | Adicionar mais keywords, revisar descrições problemáticas |
| Ambiguidade inerente em muitos casos | Médio | Alta | Documentar casos ambíguos, permitir multi-label |
| Tempo de anotação manual muito longo | Médio | Média | Reduzir dataset de 1000 para 500 casos |
| Modelo de embeddings inadequado | Alto | Baixa | Testar modelos alternativos (BERTimbau, mDeBERTa) |
| Temas muito desbalanceados no teste | Médio | Média | Estratificar amostragem por temas L1 |
| Conteúdo completo muito lento | Médio | Média | Usar apenas título + resumo, ou truncar conteúdo |
| Resumo não disponível em todas as notícias | Médio | Alta | Gerar resumos automáticos ou usar estratégia E (título + início) |

---

## Critérios de Sucesso

A Fase 4 será considerada concluída com sucesso se:

### ✅ Qualidade Técnica
- 0 erros estruturais no YAML
- 100% dos nós com campos obrigatórios
- < 5% de descrições com problemas ortográficos

### ✅ Qualidade Semântica
- < 10% de pares de irmãos com similaridade > 0.85
- Todas as keywords relevantes e específicas
- Descrições com comprimento adequado

### ✅ Performance de Classificação (na melhor estratégia)
- Acurácia L1 ≥ 85% (top-1)
- Acurácia L2 ≥ 70% (top-1)
- Acurácia L3 ≥ 60% (top-1)
- Acurácia hierárquica completa ≥ 55%

### ✅ Documentação
- Relatório final completo e claro
- Guia de uso prático e acessível
- Exemplos funcionais de código
- Todos os artefatos organizados

### ✅ Decisão sobre Estratégia de Entrada
- Análise comparativa clara das 5 estratégias
- Recomendação justificada da melhor abordagem
- Trade-offs documentados (precisão vs. velocidade vs. disponibilidade)

---

## Próximos Passos

Após aprovação deste plano:

1. ✅ Criar estrutura de pastas `_plan_refinamento/`
2. ⬜ Criar README.md e requirements.txt
3. ⬜ Implementar scripts da Subfase 4.1 (validação estrutural)
4. ⬜ Executar validação estrutural e gerar primeiro relatório
5. ⬜ Prosseguir sequencialmente pelas subfases 4.2 → 4.6
6. ⬜ Realizar checkpoint após subfases 4.4 (decisão de estratégia) e 4.5

---

## Observações Finais

Este plano é **iterativo e adaptável**. Após cada subfase, deve-se:
- Revisar resultados obtidos
- Ajustar próximas subfases se necessário
- Documentar decisões e mudanças de direção
- Manter comunicação com stakeholders sobre progresso e descobertas

**Ênfase especial:** A Subfase 4.4 é crítica pois definirá qual estratégia de entrada usar (título/resumo/conteúdo). Essa decisão impactará diretamente a arquitetura do sistema de classificação em produção.
