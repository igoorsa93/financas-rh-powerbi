# Roadmap — Excel → Power BI

Este documento descreve os próximos passos do projeto, partindo dos workbooks Excel já
consolidados até um modelo estruturado no Power BI. Todos os dados citados aqui são fictícios
(veja aviso no [README](README.md)).

## Onde estamos

- [x] `Financas_Pessoais.xlsx` — controle manual (Contas, Categorias, Lançamentos, Orçamento, Resumo)
- [x] `RH_Folha_Consolidado.xlsx` — consolidação de folha de pagamento (Funcionários, Líquidos,
      Horas Extras, Faltas, Atestados, Rescisões, Rubricas de Folha, Resumos por Departamento/Geral)
- [x] Vínculos internos entre abas (INDEX/MATCH por Código, SUMIFS/SUMPRODUCT nos resumos)
- [x] Direção visual dos dois dashboards (RH e Financeiro) validada em mockup

## Próximos passos

### 1. Modelagem de dados (Power BI / Power Query)
- Importar as duas planilhas como fontes independentes (dois modelos separados, não misturar
  dados de empresa com dados pessoais).
- Separar cada aba em tabelas fato/dimensão:
  - **RH**: `Funcionarios` (dimensão) ligada a `Liquidos`, `Horas_Extras`, `Faltas`, `Atestados`,
    `Rescisoes` (fatos) pela chave `Codigo`; `Departamentos` como dimensão derivada de
    `Resumo_Departamento`.
  - **Financeiro**: `Contas` e `Categorias` (dimensões) ligadas a `Lancamentos` (fato) por nome.
- Criar uma tabela `Calendario` (Power Query ou DAX `CALENDAR`) para permitir análise por
  mês/ano em ambos os modelos.
- Definir tipos de dados corretos (moeda, data, percentual) já na importação, evitando conversão
  implícita no relatório.

### 2. Medidas DAX
- **RH**: Total Líquido, Custo por Departamento, Total Horas Extras, % Absenteísmo (Faltas +
  Atestados / Horas Previstas), Rescisões no Período, Ticket Médio de Rescisão.
- **Financeiro**: Receita do Mês, Despesa do Mês, Saldo do Mês, Saldo Acumulado, % Orçamento
  Realizado por Categoria, Variação Planejado x Realizado.

### 3. Páginas do relatório (espelhando os mockups já validados)
- **RH**: Visão Geral, Departamentos, Horas Extras, Faltas & Atestados, Rescisões, Ficha do
  Funcionário (drill-through a partir de qualquer visual).
- **Financeiro**: Visão Geral, Contas, Lançamentos, Orçamento, Investimentos.

### 4. Identidade visual
- Aplicar a paleta e a logo de cada projeto (verde corporativo para RH, paleta própria para
  Financeiro) nos temas do Power BI (`theme.json`), replicando o padrão dos mockups HTML.

### 5. Publicação e atualização
- Definir se os `.xlsx` ficam locais (import) ou em um OneDrive/SharePoint para permitir
  atualização agendada no Power BI Service.
- Configurar atualização (refresh) manual ou agendada, conforme a frequência de lançamento dos
  dados de origem.

## Fora de escopo por enquanto

- Automação de entrada de dados (hoje é manual/lançamento por planilha).
- Integração direta com sistemas de folha ou bancos (Open Finance).
