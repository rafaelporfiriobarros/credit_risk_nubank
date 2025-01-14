# Previsão de Risco de Crédito - NuBank

![cartao_nubank](images/cartao-nubank.jpg)

## 1. Descrição 

- A avaliação de risco de crédito é um processo crucial para instituições financeiras como o Nubank, uma fintech que revolucionou o setor bancário com foco em simplicidade, tecnologia e personalização. Esse processo visa identificar a capacidade e a probabilidade de um cliente cumprir suas obrigações financeiras, garantindo que o crédito seja concedido de forma responsável e sustentável.
Cada vez mais, soluções vêm sendo desenvolvidas e aprimoradas visando minimizar o risco de default.

- Default é o termo utilizado para indicar o não cumprimento das obrigações e/ou condições de um empréstimo (como financiamentos ou dívidas de cartão de crédito). Normalmente, o principal motivo para o descumprimento das condições de pagamento é a incapacidade financeira do cliente.

## 2. Como Funciona a Avaliação de Risco de Crédito

### Análise de Dados Alternativos

- Os bancos utilizam fontes de dados alternativos para analisar o perfil de seus clientes. Além de dados convencionais como histórico de crédito (score do Serasa ou SPC), a empresa analisa informações comportamentais coletadas de maneira ética e transparente.

### Modelos de Machine Learning

- A avaliação de crédito dos bancos hoje em dia é altamente tecnológica. A empresa usa algoritmos de machine learning para processar grandes volumes de dados e identificar padrões. Esses modelos são ajustados continuamente, aprendendo com o comportamento real dos clientes para oferecer uma análise mais precisa e personalizada.

### Customização de Limites

- Com base nos dados analisados, os bancos oferecem limites personalizados para seus clientes. Isso permite que a empresa conceda crédito de forma gradativa, aumentando o limite conforme o cliente demonstra bom comportamento financeiro, como o pagamento pontual de faturas.

### Transparência no Processo

- Os bancos precisam de transparência com os clientes. Por exemplo, se um pedido de aumento de limite for negado, os bancos explicam os motivos e oferecem dicas práticas para melhorar a análise de crédito futura.

# Contextualização do Problema

Neste problema, o objetivo é prever qual a probabilidade de um cliente da Startup Nubank não cumprir com suas obrigações financeiras e deixar de pagar a sua fatura do Cartão de Crédito.

Vale ressaltar que essa avaliação deve ser realizada no momento em que o cliente solicita o cartão (normalmente no primeiro contato com a instituição).

**OBJETIVO: Criar um modelo que forneça a probabilidade de um cliente virar inadimplente.**

# Relatório Análise Univariada

- Entre os **Scores**, o Score 3 é o mais diversificado para uma análise bi e multivariada, onde o score **340.0** é o valor mais frequente.

- Em **Risk Rate** o valor de **0.29** é o valor mais frequente, onde o valor máximo registrado é de **0.9**.

- Em **Last Amount Borrowed** o valor de **12024.02** é o mais frequente, e praticamente isolado, pois em segundo lugar vem o valor de 10022.75 com apenas 3 registros.

- Em **Last Borrowed in Months** **36.0** meses é o intervalo com mais frequência.

- Em **Credit Limit** o valor de **31510.0** é o valor mais frequente, e praticamente isolado, pois em segundo lugar vem o valor de **10000.0** com apenas **78** registros.

- Em **Income** o valor de **61291.01** é o mais frequente, e praticamente isolado, pois em segundo lugar vem o valor de **75017.74** com apenas 5 registros.

- Em **Ok Since** temos o valor de **32.0** com mais frequência e praticamente isolado, com **20079** registros.

- Em **N Bankruptcies** não há muitas declarações de falência, **31259** são a quantidade de registros sem declaração de falência.

- Em **N Defaulted Loans** grande parte dos empréstimos não estão como inadimplentes.

- Em **N Accounts** podemos ver que grande parte dos clientes possuem mais de **5** a **10** contas ou créditos em seus nomes.

- Em **N Issues** podemos ver que **10** problemas ou ocorrências, irregularidades associadas as contas dos clientes são mais frequentes, seguidas de 9, 8 e 11 ocorrências.

- Em **External Data Provider Credit Checks Last 2 Years** possuem **0** quantidade de consultas.

- **External Data Provider Credit Checks Last Month** já é um pouco diferente. **2** é o números mais frequente de vezes que provedores externos consultaram o histórico de crédito no mês anterior.

- Em **External Data Provider Credit Checks Last Year** **1** que siginica True é o numero com mais frequência em consultas dos dados históricos de crédito.

- Em **Reported Income** temos valores bem altos, na casa de milhões com mais frequência, em seguida vem valores mais aceitáveis, precisamos checar possiveis outliers.

- Em **Shipping State** é basicamente o registro dos estados onde se localizam cada cliente. **SP** é o estado com mais frequência.

- E em **Target Default** podemos ver que há mais registros **positivos** com relação aos créditos.

- Verificamos que  há valores discrepantes nas variáveis **credit_limit**, **income** e **reporte_income**, mas precisamos ter cuidado ao excluir pois podemos compromoter a qualidade dos dados.
