# Padrões DAX Recomendados

Boas práticas genéricas de escrita de medidas DAX, pensadas para o modelo deste projeto
(RH/Folha e Financeiro Pessoal — ver [ROADMAP.md](../ROADMAP.md)). Os exemplos usam nomes de
medidas planejadas no roadmap (Total Líquido, Custo por Departamento, % Absenteísmo, Saldo do
Mês, % Orçamento Realizado), mas as fórmulas são didáticas — servem para ilustrar a técnica, não
são a implementação final.

---

## 1. Proteção contra BLANK em operações aritméticas

### ❌ Evitar
```dax
[Receita do Mês] - [Despesa do Mês]
-- Se qualquer medida retornar BLANK, o resultado inteiro vira BLANK
```

### ✅ Preferir
```dax
COALESCE([Receita do Mês], 0) - COALESCE([Despesa do Mês], 0)
-- BLANK é tratado como 0; o resultado só fica BLANK se não houver base nenhuma
```

### Variante com validação de base
```dax
Saldo do Mês =
VAR _receita = [Receita do Mês]
RETURN
    IF(
        ISBLANK(_receita),
        BLANK(),  -- sem receita no período = sem saldo a mostrar
        COALESCE(_receita, 0) - COALESCE([Despesa do Mês], 0)
    )
```

Use esse padrão sempre que uma medida combinar duas ou mais medidas que podem individualmente
retornar BLANK (período sem lançamentos, filtro sem correspondência etc.).

---

## 2. DIVIDE() em vez de divisão direta

### ❌ Evitar
```dax
% Absenteísmo = SUM(Faltas[Horas]) / SUM(Calendario[Horas_Previstas])
-- Erro de divisão por zero se o denominador for 0 ou BLANK
```

### ✅ Preferir
```dax
% Absenteísmo = DIVIDE(SUM(Faltas[Horas]), SUM(Calendario[Horas_Previstas]), 0)
```

### Quando o "valor alternativo" também deveria ser BLANK (não 0)
Às vezes retornar `0` esconde a diferença entre "não houve absenteísmo" e "não há dados para
calcular". Nesse caso, proteja explicitamente:
```dax
% Absenteísmo =
VAR _ausencias = SUM(Faltas[Horas])
VAR _previstas = SUM(Calendario[Horas_Previstas])
RETURN
    IF(
        _previstas = 0,
        BLANK(),          -- não há base para calcular o percentual
        DIVIDE(_ausencias, _previstas)
    )
```

---

## 3. Alias em vez de duplicar lógica

### ❌ Evitar (duplicação gera divergência quando uma cópia é atualizada e a outra não)
```dax
-- Custo Total da Folha
VAR Total = SUM(Rubricas_Folha[Valor_Calculado])
RETURN Total

-- Custo Total (usada em outro relatório) — cópia da fórmula acima
VAR Total = SUM(Rubricas_Folha[Valor_Calculado])
RETURN Total
```

### ✅ Preferir (referência única)
```dax
-- Custo Total da Folha (implementação)
SUM(Rubricas_Folha[Valor_Calculado])

-- Custo Total (alias, usado por compatibilidade em outro relatório)
[Custo Total da Folha]
```

Sempre que duas medidas precisarem existir com nomes diferentes (por exemplo, uma para uso em
cálculos e outra para segmentação/filtro em outra tabela), prefira que uma referencie a outra em
vez de repetir a expressão.

---

## 4. Contagem: cuidado com COUNTROWS vs COUNTA vs DISTINCTCOUNT

- `COUNTROWS(tabela)` conta **todas as linhas**, inclusive linhas "vazias" geradas por
  relacionamentos ou por linhas técnicas sem valor útil.
- `COUNTA(tabela[coluna])` conta apenas células não vazias de uma coluna específica — mais preciso
  quando a tabela pode ter linhas sem preenchimento completo.
- `DISTINCTCOUNT(tabela[coluna])` conta valores únicos — essencial quando a tabela de origem tem
  múltiplas linhas por entidade (ex.: várias linhas de pagamento por funcionário) e a métrica
  precisa ser "por entidade", não "por linha".

### Exemplo
```dax
-- ❌ Ambíguo: pode contar funcionários inativos ou linhas duplicadas
Qtd Funcionários = COUNTROWS(Funcionarios)

-- ✅ Preciso: conta só quem de fato tem um registro de pagamento no período
Qtd Funcionários Pagos = DISTINCTCOUNT(Liquidos[Codigo])
```

Ao escolher o denominador de uma medida de "média por entidade" (ex.: Custo Médio por
Funcionário), confirme que a contagem usa a tabela/coluna com granularidade correta — não
necessariamente a tabela dimensão completa, que pode incluir registros fora do escopo do cálculo.

---

## 5. Proteção contra valores negativos com MAX

### ❌ Evitar
```dax
Saldo Disponível = [Orçamento] - [Realizado]
-- Se Realizado > Orçamento por causa de arredondamento ou lançamento tardio, o resultado fica
-- negativo mesmo quando isso não faz sentido de negócio
```

### ✅ Preferir (quando a regra de negócio proíbe negativos)
```dax
Saldo Disponível = MAX(0, [Orçamento] - [Realizado])
```

Use esse padrão apenas quando negativo for de fato impossível pela regra de negócio (ex.: "saldo
restante de orçamento"). Se o negativo for uma informação válida (ex.: "variação
planejado x realizado", que pode ser positiva ou negativa de propósito), não force o MAX(0,...).

---

## 6. Operador OR (||) vs AND (&&) em validações compostas

```dax
-- "conte como ativo se A OU B existir"
VAR EstaAtivo = NOT ISBLANK([MedidaA]) || NOT ISBLANK([MedidaB])

-- "conte como ativo só se A E B existirem"
VAR EstaAtivo = NOT ISBLANK([MedidaA]) && NOT ISBLANK([MedidaB])
```

Escolher o operador errado é um bug sutil e comum: usar `&&` quando a regra pede `||` esconde
registros válidos (ex.: um lançamento que só tem uma das duas informações); usar `||` quando a
regra pede `&&` mostra registros "fantasma" sem base suficiente. Sempre escreva por extenso, em
comentário, qual é a regra de negócio antes de escolher o operador.

---

## 7. Filtragem entre tabelas com TREATAS

Útil quando você precisa aplicar, a uma tabela de fatos, os valores visíveis de uma coluna vinda
de outra tabela (dimensão ou outra tabela de fatos), sem depender de um relacionamento físico
direto.

```dax
CALCULATE(
    SUM(Lancamentos[Valor]),
    TREATAS(
        VALUES(Categorias[Categoria]),   -- valores visíveis no contexto de filtro atual
        Lancamentos[Categoria]           -- coluna correspondente na tabela de fatos
    )
)
```

`TREATAS` tende a ter melhor performance que `FILTER` sobre tabelas grandes porque opera por
índice de coluna em vez de iterar linha a linha — prefira-o quando a lógica for "aplicar estes
valores visíveis como filtro em outra tabela".

---

## 8. Arredondamento: uma vez só, no final

### ❌ Evitar (arredondamento duplicado pode gerar diferenças de centavos)
```dax
ROUND(SUM(Receitas[Valor]), 2) - ROUND(SUM(Despesas[Valor]), 2)
```

### ✅ Preferir
```dax
VAR Resultado = SUM(Receitas[Valor]) - SUM(Despesas[Valor])
RETURN ROUND(Resultado, 2)
```

Arredonde depois de todas as operações aritméticas, não em cada parcela individual — evita que
pequenas diferenças de arredondamento se acumulem entre as partes de um cálculo.

---

## 9. Hierarquia de medidas sem referências circulares

Ao construir medidas que dependem de outras medidas (medidas "compostas"), documente a hierarquia
e confirme que cada nível só depende de níveis "mais baixos":

```
Nível 2: [Saldo do Mês]       = [Receita do Mês] - [Despesa do Mês]
Nível 1: [Receita do Mês]     = SUM(Lancamentos[Valor]) filtrado por tipo = Receita
Nível 1: [Despesa do Mês]     = SUM(Lancamentos[Valor]) filtrado por tipo = Despesa
```

### ❌ Nunca faça isso
```
[Medida A] = [Medida B]
[Medida B] = [Medida A]
-- referência circular: o motor DAX não consegue resolver
```

Antes de publicar um conjunto de medidas encadeadas, desenhe (ainda que num comentário ou num
diagrama simples) a árvore de dependências e confirme visualmente que não há ciclos.

---

## 10. Coerência de base em cálculos que se cruzam

Quando várias medidas derivam de uma mesma métrica base (ex.: `Custo Total da Folha` alimentando
`Custo Médio por Funcionário`, `% da Meta` e `Diferença da Meta`), garanta que todas usem a mesma
fonte, e não cópias equivalentes vindas de tabelas diferentes:

```dax
✅ PADRÃO — uma base, várias derivadas
[Custo Total da Folha]        -- base única: SUM(Rubricas_Folha[Valor_Calculado])
├─ [Custo Médio por Funcionário]  -- DIVIDE([Custo Total da Folha], DISTINCTCOUNT(...))
├─ [% da Meta]                    -- DIVIDE([Custo Total da Folha], [Meta Custo Folha])
└─ [Diferença da Meta]            -- [Custo Total da Folha] - [Meta Custo Folha]
```

```dax
❌ EVITAR — duas bases "equivalentes" vindas de tabelas diferentes
[Custo Total Método A]   -- SUM(TabelaX[Valor])
[Custo Total Método B]   -- SUM(TabelaY[Valor])
-- se TabelaX e TabelaY não estiverem sempre sincronizadas, os relatórios divergem
```

---

## Exemplo completo: medida "segura" combinando os padrões acima

```dax
Saldo do Mês (Seguro) =
    VAR _receita   = [Receita do Mês]
    VAR _despesa   = COALESCE([Despesa do Mês], 0)
    VAR _resultado = ROUND(COALESCE(_receita, 0) - _despesa, 2)
    RETURN
        IF(
            ISBLANK(_receita),
            BLANK(),   -- sem lançamento de receita no período = nada a mostrar
            _resultado
        )
```

Por que é uma medida "segura":
- ✅ Protege contra BLANK nas parcelas (item 1)
- ✅ Arredonda uma única vez, no final (item 8)
- ✅ Valida a existência de uma base antes de calcular (item 1)
- ✅ Legível — cada `VAR` tem um nome que explica sua função

---

## Resumo rápido

| Padrão | Use quando | Evite |
|---|---|---|
| `COALESCE` | combinar medidas que podem ser BLANK | operar direto em possíveis BLANK |
| `DIVIDE(...)` | qualquer divisão | `/` direto sem proteção |
| Alias (`[MedidaBase]`) | reaproveitar lógica | duplicar a mesma fórmula |
| `DISTINCTCOUNT` | contar "por entidade" | `COUNTROWS` numa tabela com duplicatas |
| `MAX(0, ...)` | negativo é logicamente impossível | negativo é uma informação válida |
| OR (`\|\|`) vs AND (`&&`) | definir a regra de negócio primeiro | escolher no automático |
| `TREATAS` | aplicar filtro entre tabelas sem relação direta | `FILTER` em tabelas grandes |
| `ROUND` no final | após todas as operações | `ROUND` em cada parcela |
| Hierarquia documentada | medidas compostas | referências circulares |

---

## Referências

- Documentação oficial DAX (Microsoft Learn)
- Tabular Editor — boas práticas de modelagem
- Marco Russo / Alberto Ferrari — *Analyzing Data with Power BI and Power Pivot for Excel* / SQLBI
