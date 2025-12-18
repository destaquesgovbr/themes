# Guia de Classificação Manual de Notícias GovBR

**Versão:** 1.0
**Fase:** 4.3 - Preparação de Dataset de Teste
**Data:** 2025-12-18

---

## 📋 Objetivo

Este guia fornece instruções para anotação manual de notícias governamentais brasileiras usando a árvore temática DestaquesGovBr (3 níveis hierárquicos).

---

## 🎯 Estrutura da Árvore Temática

### Níveis de Classificação

- **L1 (Tema):** Área temática geral (ex: Economia, Saúde, Educação)
- **L2 (Subtema):** Subdivisão específica dentro do tema
- **L3 (Categoria):** Categoria específica de notícia

### Hierarquia Obrigatória

⚠️ **Importante:** A classificação deve seguir a hierarquia:
1. Sempre classifique **L1 primeiro**
2. Depois escolha **L2 dentro do L1** selecionado
3. Finalmente escolha **L3 dentro do L2** selecionado

---

## 📝 Processo de Anotação

### 1. Leitura

- Leia o **título completo**
- Leia o **resumo** (se disponível)
- Se necessário, leia o **início do conteúdo**

### 2. Identificação do Tema Principal

**Pergunta-chave:** *"Qual é o tema PRINCIPAL desta notícia?"*

- Foque no assunto central, não em menções secundárias
- Ignore nomes de ministros/órgãos (eles não definem o tema)
- Priorize o **impacto** da notícia, não apenas quem a divulgou

**Exemplo:**
```
❌ ERRADO: "Ministro da Saúde anuncia investimento em rodovias"
           → Classificar como Saúde (foco no ministro)

✅ CORRETO: "Ministro da Saúde anuncia investimento em rodovias"
            → Classificar como Infraestrutura (foco no investimento)
```

### 3. Navegação Hierárquica

1. **Escolha L1:** Selecione o tema geral que melhor descreve a notícia
2. **Escolha L2:** Dentro do L1, selecione o subtema mais específico
3. **Escolha L3:** Dentro do L2, selecione a categoria exata

### 4. Nível de Confiança

Avalie sua confiança na classificação:

- **Alta:** Tema óbvio, sem ambiguidade
- **Média:** Tema provável, mas há dúvidas ou alternativas razoáveis
- **Baixa:** Múltiplas interpretações possíveis, difícil decidir

### 5. Observações

Use o campo de observações para:
- Casos ambíguos ou limítrofes
- Quando a notícia poderia se encaixar em múltiplos temas
- Sugestões de melhoria da árvore temática
- Dúvidas sobre classificação

---

## 🧭 Regras e Critérios

### Regra 1: Tema Principal > Tema Secundário

Notícias podem mencionar múltiplos temas. **Classifique pelo tema PRINCIPAL**.

**Exemplo:**
```
Título: "Governo lança programa de educação ambiental em escolas"

Temas mencionados:
- Educação (escolas)
- Meio Ambiente (educação ambiental)

✅ Classificação: Educação > Educação Ambiental
   Razão: O foco é um programa educacional, não uma política ambiental
```

### Regra 2: Impacto > Origem

Classifique pela área de **impacto**, não pelo órgão que divulga.

**Exemplo:**
```
Título: "Ministério da Defesa investe R$ 100 mi em hospitais militares"

✅ Classificação: Saúde (impacto na saúde)
❌ NÃO: Defesa e Segurança (origem da notícia)
```

### Regra 3: Específico > Genérico

Quando houver dúvida entre categorias, escolha a mais **específica**.

**Exemplo:**
```
Título: "Governo amplia Bolsa Família para 20 milhões de famílias"

Opções:
- Desenvolvimento Social > Assistência Social (genérico)
- Desenvolvimento Social > Bolsa Família (específico)

✅ Classificação: Use a categoria específica "Bolsa Família"
```

### Regra 4: Conteúdo > Título

Se o título for ambíguo, use o **resumo ou conteúdo** para decidir.

**Exemplo:**
```
Título: "Presidente assina decreto"
Resumo: "Decreto cria novas regras para concessão de rodovias federais"

✅ Classificação: Infraestrutura > Transportes > Rodovias
```

---

## 🚨 Casos Especiais

### Caso 1: Notícias Multi-Temáticas

Quando a notícia cobre **2 ou mais temas com igual importância**:
- Escolha o tema que aparece **primeiro** no título
- Documente os outros temas nas **observações**

**Exemplo:**
```
Título: "Governo anuncia investimentos em saúde e educação"

✅ Classificação: Saúde (aparece primeiro)
📝 Observação: "Notícia multi-temática: também cobre Educação"
```

### Caso 2: Notícias Administrativas Genéricas

Anúncios de ministros, nomeações, viagens oficiais:
- Classifique pela **área de atuação** do órgão/ministério
- Se não for possível determinar, use **confiança "baixa"**

**Exemplo:**
```
Título: "Ministra da Cultura visita França"

✅ Classificação: Cultura > Relações Internacionais da Cultura
🔴 Confiança: Média (notícia administrativa, impacto indireto)
```

### Caso 3: Eventos e Inaugurações

Eventos, inaugurações, cerimônias:
- Classifique pela **finalidade** do evento, não pelo evento em si

**Exemplo:**
```
Título: "Presidente inaugura hospital em São Paulo"

✅ Classificação: Saúde > Infraestrutura de Saúde
❌ NÃO: Eventos (o foco é o hospital, não a cerimônia)
```

### Caso 4: Programas e Ações Governamentais

Lançamentos de programas, ações, políticas:
- Classifique pela **área beneficiada**, não pela ação em si

**Exemplo:**
```
Título: "Governo lança Programa Brasil Alfabetizado"

✅ Classificação: Educação > Alfabetização
❌ NÃO: Programas Sociais (foco é educação)
```

---

## ⚠️ Erros Comuns a Evitar

### ❌ Erro 1: Classificar pelo Órgão

```
Título: "Ministério da Economia anuncia concurso público"

❌ ERRADO: Economia (foco no ministério)
✅ CORRETO: Administração Pública > Concursos Públicos
```

### ❌ Erro 2: Ignorar a Hierarquia

```
❌ ERRADO: Selecionar L3 sem passar por L1 e L2 corretos
✅ CORRETO: Seguir L1 → L2 → L3 na ordem
```

### ❌ Erro 3: Classificar por Palavra-Chave Isolada

```
Título: "Banco Central mantém Selic em 13,75% para controlar inflação"

❌ ERRADO: "Controlar" → Controle e Fiscalização
✅ CORRETO: Economia > Política Monetária (contexto completo)
```

### ❌ Erro 4: Usar Conhecimento Externo

```
❌ ERRADO: Classificar com base em conhecimento prévio não presente na notícia
✅ CORRETO: Classificar apenas com base no texto fornecido
```

---

## 💡 Dicas Práticas

### 1. Use o Campo de Observações
Quando tiver dúvida ou encontrar casos limítrofes, documente! Isso ajudará no refinamento da árvore temática.

### 2. Seja Consistente
Se classificar uma notícia sobre "vacinação infantil" como **Saúde > Vacinação**, use o mesmo critério para notícias similares.

### 3. Não Tenha Pressa
Prefira qualidade a velocidade. Uma classificação cuidadosa é mais valiosa.

### 4. Confie na Árvore
A árvore temática foi criada especificamente para notícias gov.br. Se houver uma categoria específica, use-a.

### 5. Marque Confiança Honestamente
Não há problema em marcar "baixa" confiança. Isso indica que a notícia é difícil de classificar, não que você errou.

---

## 📊 Critérios de Qualidade

Uma boa anotação deve:

✅ **Ser Específica:** Usar a categoria mais detalhada possível (L3 sempre que aplicável)
✅ **Ser Consistente:** Seguir os mesmos critérios para notícias similares
✅ **Ser Justificável:** Você consegue explicar por que escolheu aquele tema
✅ **Ter Confiança Apropriada:** Refletir honestamente a dificuldade da classificação
✅ **Documentar Ambiguidades:** Usar observações para casos duvidosos

---

## 🆘 Casos de Dúvida

Se tiver dúvida sobre como classificar uma notícia:

1. **Leia novamente** o título, resumo e início do conteúdo
2. **Pergunte-se:** "Se eu fosse buscar esta notícia, que tema eu procuraria?"
3. **Consulte a árvore temática:** Veja se há uma categoria específica
4. **Use confiança "média" ou "baixa"** se ainda tiver dúvida
5. **Documente nas observações** sua dúvida ou raciocínio

**Lembre-se:** Não há classificação "errada" se você seguiu os critérios e documentou seu raciocínio.

---

## 📚 Exemplos Completos

### Exemplo 1: Classificação Clara

**Título:** "Ministério da Saúde amplia vacinação contra gripe para todo o país"

**Análise:**
- Tema: Saúde (óbvio)
- Subtema: Vacinação (especificado no título)
- Categoria: Campanha de Vacinação

**Classificação:**
- L1: `03` - Saúde
- L2: `03.02` - Vacinação
- L3: `03.02.01` - Campanhas de Vacinação
- Confiança: **Alta**
- Observações: (nenhuma)

---

### Exemplo 2: Classificação Moderada

**Título:** "Governo federal investe R$ 500 milhões em pavimentação de estradas rurais"

**Análise:**
- Tema: Infraestrutura (investimento em estradas)
- Subtema: Transportes (estradas/rodovias)
- Categoria: Rodovias? Ou Infraestrutura Rural?

**Classificação:**
- L1: `06` - Infraestrutura
- L2: `06.01` - Transportes
- L3: `06.01.01` - Rodovias
- Confiança: **Média**
- Observações: "Estradas rurais - poderia também ser Agricultura > Infraestrutura Rural"

---

### Exemplo 3: Classificação Difícil

**Título:** "Presidente participa de evento do Dia Mundial da Água"

**Análise:**
- Evento? Meio Ambiente? Recursos Hídricos?
- Título não indica ação concreta
- Foco parece ser simbólico (evento temático)

**Classificação:**
- L1: `06` - Meio Ambiente
- L2: `06.03` - Recursos Hídricos
- L3: `06.03.01` - Gestão de Recursos Hídricos
- Confiança: **Baixa**
- Observações: "Notícia sobre evento simbólico, sem ação concreta. Difícil determinar tema principal."

---

## ✅ Checklist Final

Antes de salvar cada anotação, verifique:

- [ ] Li o título completo?
- [ ] Li o resumo (se disponível)?
- [ ] Identifiquei o tema PRINCIPAL (não secundário)?
- [ ] Segui a hierarquia L1 → L2 → L3?
- [ ] Usei a categoria mais específica possível?
- [ ] Avaliei minha confiança honestamente?
- [ ] Documentei dúvidas/ambiguidades nas observações?
- [ ] Informei meu nome como anotador?

---

**Dúvidas?** Consulte este guia ou documente suas dúvidas nas observações.

**Boa anotação! 📋✨**
