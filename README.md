# Controle Financeiro Pessoal + Consolidação de Folha de Pagamento

> **Aviso importante:** este repositório contém **exclusivamente dados fictícios**, gerados
> programaticamente para fins de demonstração e portfólio. Nenhum nome de empresa, funcionário,
> CNPJ, salário ou valor financeiro aqui presente é real. Qualquer semelhança com pessoas ou
> empresas reais é coincidência.

## Sobre o projeto

Este projeto reúne dois módulos de controle financeiro construídos em Excel, com o objetivo de
futuramente evoluir para um modelo estruturado em Power BI:

1. **Finanças Pessoais** (`Financas_Pessoais.xlsx`) — planilha de controle financeiro pessoal com
   abas de Contas, Categorias, Lançamentos, Orçamento (planejado x realizado) e Resumo mensal.

2. **Consolidado de RH / Folha de Pagamento** (`RH_Folha_Consolidado.xlsx`) — workbook que
   consolida diferentes relatórios de folha de pagamento (relação de empregados, líquidos pagos,
   horas extras, faltas, atestados, rescisões, rubricas de folha) em um único arquivo, com abas
   vinculadas por fórmulas (`INDEX`/`MATCH`, `SUMIFS`, `SUMPRODUCT`) para permitir consulta
   individual por funcionário e resumos por departamento/geral.

## Estrutura do repositório

```
financas-rh-powerbi/
├── RH_Folha_Consolidado.xlsx      # Workbook consolidado de RH (dados fictícios)
├── Financas_Pessoais.xlsx              # Template de finanças pessoais (dados de exemplo)
├── Arquivos Fonte RH/             # Versões fictícias dos relatórios de origem
│   ├── relacao_empregados.xlsx
│   ├── relacao_de_faltas.xlsx
│   ├── relacao_de_atestados.xlsx
│   ├── relatorio_de_liquidos_folha_normal_principal.csv
│   ├── relatorio_de_liquidos_folha_normal_quinzena.csv
│   ├── relatorio_de_liquidos_folha_extra.csv
│   ├── relatorios_de_hora_extra_folha_normal.csv
│   ├── relatorios_de_hora_extra_folha_extra.csv
│   ├── relatorios_de_falta_por_funcionario.csv
│   ├── relacao_de_rescisoes_calculadas.csv
│   ├── resumo_mensal_geral_folha_normal.csv
│   └── resumo_mensal_geral_folha_extra.csv
└── scripts/                            # Scripts Python usados para gerar os dados fictícios
    ├── gen_fake_data.py
    ├── build_rh.py
    └── build_source_files.py
```

## RH_Folha_Consolidado.xlsx — abas

| Aba | Descrição |
|---|---|
| Capa | Índice do workbook |
| Ficha_Funcionario | Consulta individual: selecione o código do funcionário e veja todos os dados vinculados |
| Funcionarios | Cadastro completo (fonte de todos os vínculos via `INDEX`/`MATCH`) |
| Liquidos | Valores líquidos pagos por funcionário (Normal Principal / Quinzena / Extra) |
| Horas_Extras | Horas extras trabalhadas e valores calculados |
| Faltas / Atestados | Absenteísmo por funcionário |
| Faltas_Detalhado | Movimentos de falta por rubrica |
| Rescisoes | Rescisões calculadas no período |
| Rubricas_Folha | Proventos/descontos por departamento e rubrica |
| Resumo_Departamento | Totais por departamento (`SUMIFS`) |
| Resumo_Geral | KPIs consolidados (`SUM`, `COUNTA`, `SUMIFS`) |

Todos os funcionários, cargos, departamentos, datas e valores são **gerados aleatoriamente** por
script (`scripts/gen_fake_data.py` + `scripts/build_rh.py`), mantendo apenas rótulos
genéricos de cargo/departamento (ex.: "Operacional", "Assistente Financeiro") que não constituem
dado sensível.

## Como os dados fictícios foram gerados

- `scripts/gen_fake_data.py`: gera ~36 funcionários fictícios (nomes combinando prenomes e
  sobrenomes brasileiros comuns, nunca nomes de pessoas reais), cargos, departamentos, datas de
  admissão/nascimento e salários dentro de faixas plausíveis por cargo.
- `scripts/build_rh.py`: monta o workbook `RH_Folha_Consolidado.xlsx` replicando a
  estrutura de abas e fórmulas do projeto original, recalculado via Excel (COM) para garantir que
  não há erros de fórmula (`#REF!`, `#N/A`, etc.).
- `scripts/build_source_files.py`: gera as versões fictícias simplificadas dos 10 tipos de
  relatório de origem (em `.xlsx`/`.csv`), usando os mesmos funcionários e valores do workbook
  consolidado, para manter consistência interna entre fonte e consolidado.

## Próximos passos (roadmap)

- Modelagem em Power BI a partir dos dados consolidados (fato de folha, dimensão de funcionários,
  dimensão de tempo).
- Automatização da ingestão dos relatórios de origem.
- Dashboard de indicadores de RH (headcount, massa salarial, absenteísmo, turnover).
