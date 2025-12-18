# Template para Descrições de Temas

Este documento define o formato e critérios para escrever descrições de temas em cada nível da árvore.

---

## 1. Estrutura por Nível

### Nível 1 (Temas Principais)

```yaml
code: "XX"
label: "Nome do Tema"
description: |
  [2-4 frases] Descrição abrangente do escopo do tema.
  Define claramente o que está INCLUÍDO e o que está EXCLUÍDO.
  Foco em delimitar fronteiras com temas adjacentes.
keywords:
  - [10-20 termos] palavras-chave principais
  - sinônimos e variações
  - siglas relevantes (ex: SUS, IBGE)
  - termos técnicos e coloquiais
includes:
  - [3-5 itens] Tipos de conteúdo explicitamente incluídos
  - Ajuda a resolver ambiguidades
excludes:
  - [3-5 itens] Tipos de conteúdo explicitamente excluídos
  - Referência ao tema correto (ex: "ver Tema X")
```

### Nível 2 (Subtemas)

```yaml
code: "XX.YY"
label: "Nome do Subtema"
description: |
  [1-2 frases] Descrição intermediária que herda contexto do L1.
  Especifica o recorte dentro do tema principal.
keywords:
  - [8-15 termos] mais específicos que L1
  - termos do domínio específico
```

### Nível 3 (Temas Folha)

```yaml
code: "XX.YY.ZZ"
label: "Nome do Tema Específico"
description: |
  [1 frase] Descrição concisa e específica.
keywords:
  - [5-12 termos] altamente específicos
  - nomes de programas/políticas
  - termos técnicos do domínio
examples:
  - "[Título de notícia típica 1]"
  - "[Título de notícia típica 2]"
  - "[Título de notícia típica 3]"
```

---

## 2. Critérios de Qualidade

### Para Keywords

**BOM:**
- Termos que aparecem em títulos/conteúdos de notícias reais
- Sinônimos e variações (singular/plural, formal/informal)
- Siglas E formas expandidas
- Termos em português brasileiro

**EVITAR:**
- Termos muito genéricos (ex: "governo", "Brasil")
- Termos que aparecem em múltiplos temas indiscriminadamente
- Estrangeirismos quando há equivalente em português

### Para Descriptions

**BOM:**
- Linguagem clara e direta
- Foco em DIFERENCIAÇÃO (o que faz este tema diferente dos outros?)
- Menciona tipos de notícias/eventos típicos
- Usa terminologia consistente com o governo federal

**EVITAR:**
- Descrições vagas ou circulares
- Repetir o nome do tema como descrição
- Textos muito longos (máx 4 frases para L1)

### Para Includes/Excludes

**BOM:**
- Casos de borda que geram dúvida
- Referências cruzadas para temas relacionados
- Exemplos concretos de conteúdo

**EVITAR:**
- Listar o óbvio
- Excludes sem indicar o tema correto

### Para Examples (L3)

**BOM:**
- Títulos reais ou realistas de notícias
- Variedade de formatos (anúncio, resultado, evento)
- Representativos do tema

**EVITAR:**
- Exemplos que poderiam estar em outros temas
- Títulos muito genéricos

---

## 3. Checklist de Validação

Antes de finalizar uma descrição, verificar:

- [ ] Description diferencia claramente de temas adjacentes?
- [ ] Keywords incluem sinônimos e variações?
- [ ] Keywords incluem siglas relevantes?
- [ ] Includes/excludes resolvem ambiguidades conhecidas?
- [ ] Linguagem é consistente com outros temas do mesmo nível?
- [ ] Não há sobreposição significativa de keywords com outros temas?

---

## 4. Exemplo Completo

### Nível 1

```yaml
code: "03"
label: "Saúde"
description: |
  Políticas, programas e ações relacionadas à saúde pública e ao
  Sistema Único de Saúde (SUS). Inclui vigilância sanitária, campanhas
  de vacinação, assistência médica, e regulação de produtos e serviços
  de saúde. Não inclui pesquisa científica em saúde (ver Ciência e Tecnologia).
keywords:
  - saúde
  - saúde pública
  - SUS
  - Sistema Único de Saúde
  - hospital
  - UBS
  - Unidade Básica de Saúde
  - vacina
  - vacinação
  - imunização
  - medicamento
  - remédio
  - ANVISA
  - Ministério da Saúde
  - epidemia
  - pandemia
  - doença
  - tratamento
  - atendimento médico
includes:
  - Campanhas de vacinação e imunização
  - Regulação de medicamentos e produtos de saúde
  - Atendimento no SUS e hospitais públicos
  - Vigilância epidemiológica e sanitária
  - Políticas de saúde mental
excludes:
  - Pesquisa científica em saúde (ver 06 - Ciência e Tecnologia)
  - Saúde ocupacional/do trabalhador (ver 14 - Trabalho e Emprego)
  - Esportes e atividade física (ver 09 - Esportes e Lazer)
```

### Nível 2

```yaml
code: "03.02"
label: "Campanhas de Saúde Pública"
description: |
  Ações de comunicação e mobilização para prevenção de doenças e promoção
  da saúde. Inclui campanhas de vacinação, conscientização e educação em saúde.
keywords:
  - campanha
  - vacinação
  - imunização
  - prevenção
  - conscientização
  - dia nacional
  - semana de saúde
  - mobilização
  - combate à doença
```

### Nível 3

```yaml
code: "03.02.01"
label: "Combate à Dengue"
description: |
  Ações específicas de prevenção e combate à dengue, zika e chikungunya.
keywords:
  - dengue
  - Aedes aegypti
  - zika
  - chikungunya
  - arbovirose
  - mosquito
  - criadouro
  - fumacê
  - mutirão de limpeza
  - água parada
examples:
  - "Ministério da Saúde lança campanha nacional contra a dengue"
  - "Governo reforça ações de combate ao Aedes aegypti"
  - "Brasil registra queda nos casos de dengue após mutirões"
```

---

## 5. Processo de Escrita

1. **Pesquisar** - Consultar notícias classificadas no tema para entender padrão
2. **Rascunhar** - Escrever primeira versão da descrição
3. **Diferenciar** - Comparar com temas adjacentes, ajustar fronteiras
4. **Validar** - Aplicar checklist de qualidade
5. **Revisar** - Ajustar baseado em feedback ou testes
