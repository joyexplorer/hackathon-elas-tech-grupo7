# 📊 Hackathon Elas Tech - Previsão de Churn em Telecom

## 👥 Equipe Grupo 7

Projeto desenvolvido para o Hackathon Elas Tech com foco em análise estratégica, predição de churn e visualização executiva para apoiar decisões de retenção de clientes em uma empresa de telecomunicações.

---

# 🎯 Objetivo do Projeto

Desenvolver uma solução completa de análise de cancelamento de clientes (**churn**) capaz de:

* Identificar padrões de evasão
* Mensurar impacto financeiro
* Realizar limpeza e tratamento profissional dos dados
* Construir modelos preditivos de Machine Learning
* Disponibilizar dashboard interativo para stakeholders

---

# 🧠 Problema de Negócio

O churn representa perda direta de receita e aumento no custo de aquisição de novos clientes.

### Principais metas:

* Reduzir cancelamentos
* Identificar clientes de alto risco
* Melhorar retenção
* Aumentar previsibilidade financeira

---

# 🔎 Etapas do Projeto

## 1️⃣ SQL - EDA de Negócio

### Objetivo:

Expor o cenário inicial da empresa e quantificar a gravidade do churn.

### Análises realizadas:

* Total de clientes
* Total de cancelamentos
* Taxa de churn
* Receita mensal total
* Receita perdida por churn
* Churn por contrato
* Churn por método de pagamento
* Churn por perfil de cliente

### Benefícios:

* Visão executiva inicial
* Storytelling financeiro
* Base para hipóteses estratégicas

---

## 2️⃣ Pandas - Limpeza e Tratamento

### Processos realizados:

* Renomeação de colunas para português
* Tratamento de valores nulos
* Conversão de tipos numéricos
* Normalização de campos categóricos
* Criação de faixas analíticas
* QA e validação de consistência

### Resultado:

Base final pronta para:

* EDA preditiva
* Dashboard
* Machine Learning

---

## 3️⃣ QA - Quality Assurance

### Verificações:

* Contagem de registros
* Validação de ranges
* Consistência pós-limpeza
* Integridade de colunas
* Conferência entre SQL e Pandas

---

## 4️⃣ EDA Preditiva

### Análises principais:

* Correlação entre variáveis
* Tempo de permanência vs churn
* Valor mensal vs churn
* Contrato vs churn
* Serviços adicionais vs churn
* Perfil demográfico

### Principais insights:

* Contratos mensais possuem maior risco
* Clientes novos cancelam mais
* Electronic check apresenta churn elevado
* Clientes com maior valor mensal podem representar maior impacto financeiro
* Serviços adicionais ajudam retenção

---

## 5️⃣ Machine Learning 

#Modelos testados:

* Regressão Logística
* Melhor Recall para churn
* Alta interpretabilidade
* Modelo estratégico principal
* Random Forest
* XGBoost

### Objetivo:

Prever probabilidade de churn

---

## 6️⃣ Dashboard Interativo (Streamlit)

### Funcionalidades:

* KPIs estratégicos
* Receita total
* Receita em risco
* Taxa de churn
* Filtros interativos
* Visualizações por perfil
* Recomendações estratégicas
* Estrutura pronta para integração ML

---

# 📈 Principais Resultados

### Base:

* 7043 clientes

### Taxa de churn:

* ~26.5%

### Receita mensal em risco:

* ~R$139 mil/mês

### Impacto anual estimado:

* ~R$1.6 milhão

---

# 💡 Estratégias Recomendadas

## Curto prazo:

* Migração de contratos mensais
* Incentivo a débito automático
* Campanhas de retenção para novos clientes

## Médio prazo:

* Cross-sell de serviços adicionais
* Programa de fidelidade
* Segmentação de risco

## Longo prazo:

* Modelo preditivo em produção
* Score contínuo de churn
* Automação de retenção

---

# 🚀 Tecnologias Utilizadas

* Python
* Pandas
* SQLite
* SQL
* Matplotlib / Seaborn / Plotly
* Streamlit
* Scikit-learn
* GitHub
* Google Colab

---

# 📷 Dashboard

O dashboard foi desenvolvido em Streamlit para fornecer uma experiência visual interativa e executiva.

### Inclui:

* Visão geral
* Financeiro
* Perfil do cliente
* Análise de churn
* Recomendações
* Base futura para ML

---


# 🏆 Conclusão
Este projeto representa o esforço máximo e a dedicação da equipe em aplicar de forma integrada todas as ferramentas e metodologias ensinadas ao longo do curso. Nossa prioridade foi garantir que cada etapa — desde a extração de dados via SQL até a construção dos modelos de Machine Learning — fosse acompanhada de um cuidado analítico rigoroso e de uma preocupação constante com a integridade dos dados.

Buscamos elevar o nível da entrega simulando uma situação real de consultoria estratégica. Por isso, investimos em um storytelling financeiro e executivo, capaz de traduzir métricas complexas em insights acionáveis e resultados tangíveis para o negócio, como a mensuração da receita em risco e a proposta de ações preventivas.

Acreditamos que a combinação de uma base técnica sólida (Python, SQL e Scikit-learn) com uma apresentação visual interativa e clara é o que transforma dados em decisões inteligentes. Finalizamos este ciclo com a confiança de que entregamos uma solução estratégica completa voltada para o crescimento sustentável da organização.
