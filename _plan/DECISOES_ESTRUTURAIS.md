# Registro de Decisões Estruturais da Árvore Temática

**Criado em:** 2025-12-17
**Última atualização:** 2025-12-17

Este documento registra todas as decisões tomadas sobre a estrutura da árvore temática durante o processo de revisão.

---

## Formato de Registro

Cada decisão deve seguir o formato:

```
### DEC-XXX: [Título da Decisão]

**Data:** YYYY-MM-DD
**Status:** PROPOSTA | APROVADA | IMPLEMENTADA | REJEITADA

**Contexto:**
[Descrição do problema ou situação que motivou a decisão]

**Decisão:**
[O que foi decidido]

**Justificativa:**
[Por que esta decisão foi tomada]

**Impacto:**
- [Lista de impactos]

**Ações Necessárias:**
- [ ] [Ação 1]
- [ ] [Ação 2]
```

---

## Decisões Pendentes de Aprovação

### DEC-001: Fusão de "Estatísticas e Dados Públicos" com "Políticas Públicas e Governança"

**Data:** 2025-12-17
**Status:** PROPOSTA

**Contexto:**
O tema "23 - Estatísticas e Dados Públicos" possui apenas 6 notícias classificadas (0.04% do total), indicando que é raramente utilizado. O tema "20 - Políticas Públicas e Governança" já possui subtemas relacionados a transparência e dados (20.01 - Transparência e Prestação de Contas).

**Decisão:**
Fundir o tema 23 com o tema 20, movendo os subtemas de Estatísticas para dentro de Políticas Públicas.

**Justificativa:**
- Volume extremamente baixo (6 notícias)
- Sobreposição semântica com transparência e governança
- Simplificação da árvore sem perda de granularidade

**Impacto:**
- Redução de 25 para 24 temas L1
- Necessário reclassificar 6 notícias existentes
- Atualizar prompt de classificação

**Ações Necessárias:**
- [ ] Validar com stakeholders
- [ ] Definir mapeamento de subtemas
- [ ] Reclassificar notícias existentes
- [ ] Atualizar documentação

---

### DEC-002: Fusão/Redistribuição de "Eventos Oficiais e Cerimônias"

**Data:** 2025-12-17
**Status:** PROPOSTA

**Contexto:**
O tema "22 - Eventos Oficiais e Cerimônias" possui apenas 33 notícias (0.2%). Eventos oficiais são inerentemente transversais - um evento pode ser sobre saúde, educação, economia, etc.

**Decisão:**
OPÇÃO A: Remover tema e redistribuir notícias para temas por assunto
OPÇÃO B: Manter como tema secundário (não L1)
OPÇÃO C: Manter mas reduzir subtemas

**Justificativa:**
- Eventos são transversais a todas as áreas do governo
- O foco deve ser no ASSUNTO do evento, não no formato
- Volume muito baixo indica que classificadores já evitam este tema

**Impacto:**
- A definir baseado na opção escolhida

**Ações Necessárias:**
- [ ] Analisar as 33 notícias classificadas para entender padrão
- [ ] Decidir entre opções A, B ou C
- [ ] Implementar conforme decisão

---

### DEC-003: Avaliação de Subdivisão de "Meio Ambiente e Sustentabilidade"

**Data:** 2025-12-17
**Status:** PROPOSTA

**Contexto:**
O tema "05 - Meio Ambiente e Sustentabilidade" concentra 15.5% de todas as notícias classificadas (2.101), muito acima dos demais. Isso pode indicar:
1. Tema muito amplo que absorve outros assuntos
2. Viés do classificador
3. Real predominância de notícias ambientais

**Decisão:**
Analisar distribuição interna (L2 e L3) antes de decidir subdivisão.

**Justificativa:**
- Decisão prematura sem dados de L2/L3
- Pode ser que apenas alguns subtemas estejam sobrecarregados

**Impacto:**
- Possível criação de novo tema L1 (ex: "Sustentabilidade e Desenvolvimento Sustentável")
- Manutenção de "Meio Ambiente" focado em conservação/proteção

**Ações Necessárias:**
- [ ] Coletar distribuição L2 do tema 05
- [ ] Coletar distribuição L3 do tema 05
- [ ] Analisar padrão de classificação
- [ ] Decidir se subdivisão é necessária

---

## Decisões Aprovadas

*(Nenhuma decisão aprovada ainda)*

---

## Decisões Implementadas

*(Nenhuma decisão implementada ainda)*

---

## Decisões Rejeitadas

*(Nenhuma decisão rejeitada ainda)*

---

## Histórico de Alterações deste Documento

| Data | Alteração |
|------|-----------|
| 2025-12-17 | Criação do documento com 3 propostas iniciais |
