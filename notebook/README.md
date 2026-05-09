# Notebook principal do projeto
# 🎓 Projeto: Sistema Inteligente de Análise de Churn (Telco)
> **Foco em Decision Intelligence e Modelagem Preditiva para Retenção de Clientes**

## 🎯 Objetivo do Projeto
Este notebook foi desenvolvido como um projeto consolidado de Ciência de Dados, simulando uma entrega de consultoria estratégica. O objetivo central é transformar dados brutos em **Decision Intelligence**, desenvolvendo um modelo capaz de prever o risco de cancelamento (*churn*) de clientes de telecomunicações.

A solução foca em:
*   **Prever o comportamento de abandono** antes que ele ocorra.
*   **Quantificar o impacto financeiro** da evasão.
*   **Substituir posturas reativas** por estratégias proativas baseadas em dados.

---

## 🛠️ Etapas do Desenvolvimento

O projeto percorre o ciclo completo de um projeto de dados:

1.  **Ingestão e Auditoria (SQL):** Validação de integridade e extração de KPIs financeiros diretamente de um banco de dados relacional (SQLite).
2.  **Análise Exploratória (EDA):** Identificação de padrões comportamentais e correlações (ex: impacto do tipo de contrato e métodos de pagamento no churn).
3.  **Engenharia de Dados:** Tratamento de nulos, codificação de variáveis categóricas (*One-Hot Encoding*) e normalização de escalas.
4.  **Modelagem Preditiva:** Comparação entre **Regressão Logística**, **Random Forest** e **XGBoost**, com foco na métrica de **Recall** para maximizar a captura de clientes em risco.
5.  **Análise de ROI e Negócio:** Tradução da performance estatística em valores monetários e definição de uma régua de relacionamento baseada em faixas de probabilidade.

---

## 🚀 Destaques Técnicos
*   **Modelo Campeão:** Regressão Logística (AUC 0.84 / Recall 0.76).
*   **Foco em Negócio:** Cálculo de ROI que demonstra uma preservação potencial de faturamento superior a **$220.000,00/ano**.
*   **Visualizações Avançadas:** Curvas ROC, Matrizes de Confusão Comparativas e Mapas de Calor.

---

## 📝 Nota sobre a Estrutura do Arquivo
Este notebook foi mantido em um **arquivo único (monolítico)** por uma escolha deliberada de simplicidade pedagógica e restrições de tempo para a apresentação final. 

**Em um cenário de produção escalável**, a recomendação seria a modularização deste projeto em scripts separados:
*   `ingestion.py`: Para conexão e auditoria de bancos.
*   `preprocessing.py`: Para o pipeline de limpeza e escala.
*   `model_trainer.py`: Para o treinamento e persistência de modelos.
*   `eda_plots.py`: Para a geração de relatórios visuais.

Esta separação facilitaria a manutenção, o versionamento de dados (DVC) e a implementação de rotinas de CI/CD para Machine Learning (MLOps).

---

## 📂 Como utilizar
1. Certifique-se de ter o arquivo `telco-customer-churn.csv` e o banco `.db` nos diretórios indicados.
2. Instale as dependências: `pandas`, `numpy`, `seaborn`, `matplotlib`, `scikit-learn`, `xgboost` e `sqlite3`.
3. Execute as células sequencialmente para observar a evolução da análise desde a ingestão até a recomendação estratégica final.

---
**Desenvolvido por Grupo 7 - Hackathon Elas Tech** 🚀
