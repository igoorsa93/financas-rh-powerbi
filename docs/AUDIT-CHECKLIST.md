# Checklist de Auditoria de Modelo Power BI

Checklist genérico para revisar um modelo semântico Power BI (medidas DAX, relacionamentos,
nomenclatura e performance) antes de considerá-lo pronto para uso. Pensado para ser aplicado aos
futuros modelos deste projeto (RH/Folha e Financeiro Pessoal, ver [ROADMAP.md](../ROADMAP.md)),
mas não depende de nenhuma estrutura específica — pode ser reaproveitado em qualquer modelo.

---

## 1. Como conduzir a auditoria

1. Liste todas as medidas do modelo (nome, tabela onde vive, fórmula atual).
2. Para cada medida, aplique os critérios da seção 2 abaixo e registre um status
   (🟢 certificado / 🟡 alerta / 🔴 bug) com uma nota curta.
3. Depois de revisar cada medida isoladamente, faça as verificações "de conjunto" da seção 3
   (hierarquia de dependências, redundâncias, relacionamentos).
4. Corrija bugs primeiro, depois resolva alertas, documentando a decisão mesmo quando a decisão
   for "manter como está" — isso evita que o mesmo ponto seja reaberto na próxima auditoria.
5. Rode os testes de caso extremo da seção 4 antes de dar a medida por encerrada.
6. Feche com um sumário (quantas medidas, quantos bugs corrigidos, quantos alertas resolvidos,
   score antes/depois se estiver usando pontuação) — ver seção 6.

---

## 2. Critérios por medida

- [ ] **Sintaxe DAX** — a fórmula compila sem erro e sem warnings do motor.
- [ ] **Lógica de negócio** — a fórmula realmente calcula o que o nome da medida promete; peça
      para alguém que não escreveu a fórmula explicar o que ela faz só lendo o nome, e compare
      com a implementação.
- [ ] **Tratamento de BLANK e zero** — a medida se comporta corretamente quando uma das partes do
      cálculo não tem dado (ver `docs/DAX-PATTERNS.md`, itens 1 e 2). Decida conscientemente se
      "sem dado" deve aparecer como `BLANK()`, `0`, ou outro valor — e documente a decisão.
- [ ] **Arredondamento** — arredondamento aplicado uma única vez, no fim do cálculo, não em cada
      parcela.
- [ ] **Referências entre medidas** — toda medida que uma fórmula referencia existe, está
      documentada, e a dependência faz sentido (não é uma referência "por acidente" a uma medida
      de nome parecido).
- [ ] **Relacionamentos usados corretamente** — confirme que a medida está de fato aproveitando
      os relacionamentos ativos do modelo (e não recalculando algo que já deveria vir de um
      relacionamento, ou ignorando um relacionamento que deveria filtrar o resultado).
- [ ] **Casos extremos cobertos** — período sem movimento, filtro sem correspondência, tabela
      vazia, denominador zero, primeira/última linha de uma sequência temporal.
- [ ] **Performance** — a medida evita iterações desnecessárias (`FILTER` sobre tabelas grandes
      quando `TREATAS`/`CALCULATE` resolveriam), não empilha `VAR`s redundantes, e não tem
      complexidade visivelmente maior do que o cálculo exige.
- [ ] **Nomenclatura** — nome claro, consistente com o padrão do restante do modelo (idioma,
      capitalização, uso ou não de unidades/percentual no nome), sem abreviações ambíguas.
- [ ] **Formatação de exibição** — formato de número/moeda/percentual configurado na medida (não
      deixado para o visual individual configurar toda vez).

---

## 3. Verificações de conjunto (modelo como um todo)

- [ ] **Hierarquia de dependências sem ciclos** — desenhe (mesmo que em texto) a árvore de quais
      medidas usam quais outras medidas, e confirme visualmente que não há referência circular
      (ver `docs/DAX-PATTERNS.md`, item 9).
- [ ] **Profundidade razoável** — hierarquias muito profundas (mais de 3-4 níveis de medida
      dependendo de medida) são difíceis de auditar e de dar manutenção; considere achatar.
- [ ] **Redundâncias identificadas e documentadas** — se duas medidas calculam essencialmente a
      mesma coisa (em tabelas diferentes, por exemplo, para servir a páginas de relatório
      distintas), documente que a duplicação é intencional, ou consolide.
- [ ] **Relacionamentos ativos revisados** — direção do filtro (single/both), cardinalidade
      (1:muitos, muitos:muitos) e se algum relacionamento inativo deveria estar ativo (ou
      vice-versa).
- [ ] **Colunas calculadas vs medidas** — confirme que cálculos que deveriam ser medidas (porque
      dependem do contexto de filtro) não foram implementados como colunas calculadas por engano,
      e vice-versa.
- [ ] **Parâmetros hardcoded** — valores fixos dentro de uma fórmula (metas, limites, taxas) que
      deveriam vir de uma tabela de parâmetros editável devem ser sinalizados com um TODO
      explícito, mesmo que a migração fique para depois.
- [ ] **Medidas não utilizadas** — identifique medidas que não aparecem em nenhum visual nem são
      referenciadas por outra medida; decida remover ou documentar por que permanecem.

---

## 4. Testes de caso extremo (rodar por medida crítica)

Para cada medida que alimenta um KPI principal, teste manualmente (ou com um cenário simulado):

- [ ] Período/filtro sem nenhum dado → resultado é o esperado (BLANK, 0, ou outro, conforme
      decidido na seção 2)?
- [ ] Denominador possivelmente zero → não gera erro de divisão?
- [ ] Apenas uma das partes do cálculo tem dado, a outra está vazia → resultado ainda é exibido
      corretamente (não vira BLANK por causa da parte vazia)?
- [ ] Resultado que teoricamente não deveria ser negativo → confirma que nunca fica negativo?
- [ ] Múltiplos filtros combinados (ex.: duas segmentações ao mesmo tempo) → resultado continua
      coerente?
- [ ] Comparação com um cálculo manual (fora do Power BI, ex. em planilha) para pelo menos um
      cenário conhecido, como validação cruzada.

---

## 5. Nomenclatura e organização do modelo

- [ ] Nomes de tabelas fato e dimensão seguem um padrão consistente (ex.: prefixo `d` para
      dimensões, ou nome no plural para fatos — escolha um padrão e siga em todo o modelo).
- [ ] Medidas organizadas em pastas de exibição (display folders) por assunto/página de relatório.
- [ ] Colunas técnicas (chaves, códigos internos) ocultas do usuário final do relatório.
- [ ] Descrições preenchidas nas medidas mais usadas, explicando em uma frase o que calculam e
      qualquer particularidade de comportamento com filtros.

---

## 6. Registro da auditoria (changelog)

Ao final de uma rodada de auditoria, registre em um changelog:

1. **Data e escopo** — quantas medidas/tabelas foram revisadas.
2. **Bugs corrigidos** — para cada um: nome da medida, o que estava errado, o "antes" e o
   "depois" da fórmula, e por que o "depois" resolve o problema.
3. **Alertas identificados** — itens que não são bugs, mas merecem atenção (ex.: redundância
   documentada, TODO de parametrização), com a decisão tomada.
4. **Validação** — confirmação de que as medidas corrigidas foram testadas (visualmente no
   relatório e/ou com os testes de caso extremo da seção 4).
5. **Pendências** — o que ficou para uma próxima rodada (ex.: consolidar medidas redundantes,
   parametrizar valores hardcoded, criar testes automatizados).

Um changelog registrado dessa forma facilita auditorias futuras, porque decisões já tomadas
("essa duplicação é intencional", "esse operador é `||` de propósito") não precisam ser
reinvestigadas do zero a cada revisão.

---

## Referências

- Documentação oficial DAX (Microsoft Learn)
- Tabular Editor — Best Practice Analyzer
- Ver também [`docs/DAX-PATTERNS.md`](./DAX-PATTERNS.md) para os padrões de escrita de fórmula
  usados como base desta checklist.
