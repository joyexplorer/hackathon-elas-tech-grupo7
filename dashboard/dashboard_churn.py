# dashboard_churn_completo.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Analytics Churn - Telecom",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    /* Cards personalizados */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .metric-card h2 {
        margin: 0.5rem 0;
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-card p {
        margin: 0;
        font-size: 0.8rem;
        opacity: 0.8;
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .info-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    .dark-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    /* Sidebar personalizada */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    # Caminho do arquivo CSV tratado
    file_path = r"dados\tratados\telco_customer_churn_tratado.csv"
    
    try:
        df = pd.read_csv(file_path)
        st.success(f"✅ Dados carregados com sucesso! {len(df)} registros encontrados.")
        return df
    except FileNotFoundError:
        st.error(f"❌ Arquivo não encontrado em: {file_path}")
        st.info("Verifique se o arquivo 'telco_customer_churn_tratado.csv' está na pasta correta")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df = load_data()

if df is not None:
    
    # Verificar se as colunas estão em português (do seu notebook)
    # Se ainda estiver em inglês, converter
    if 'Churn' in df.columns:
        df.rename(columns={
            'customerID': 'id_cliente', 'gender': 'genero', 'SeniorCitizen': 'idoso',
            'Partner': 'possui_parceiro', 'Dependents': 'possui_dependentes',
            'tenure': 'tempo_contrato_meses', 'PhoneService': 'servico_telefone',
            'MultipleLines': 'multiplas_linhas', 'InternetService': 'servico_internet',
            'OnlineSecurity': 'seguranca_online', 'OnlineBackup': 'backup_online',
            'DeviceProtection': 'protecao_dispositivo', 'TechSupport': 'suporte_tecnico',
            'StreamingTV': 'streaming_tv', 'StreamingMovies': 'streaming_filmes',
            'Contract': 'tipo_contrato', 'PaperlessBilling': 'fatura_digital',
            'PaymentMethod': 'metodo_pagamento', 'MonthlyCharges': 'valor_mensal',
            'TotalCharges': 'valor_total', 'Churn': 'cancelamento'
        }, inplace=True)
    
    # Converter TotalCharges para numérico se necessário
    if df['valor_total'].dtype == 'object':
        df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
        df['valor_total'] = df['valor_total'].fillna(0)
    
    # Criar faixas para análises
    df['faixa_valor_mensal'] = pd.cut(df['valor_mensal'], 
                                       bins=[0, 30, 50, 70, 90, 120, 200],
                                       labels=['< R$30', 'R$30-50', 'R$50-70', 'R$70-90', 'R$90-120', 'R$120+'])
    
    df['faixa_tempo'] = pd.cut(df['tempo_contrato_meses'], 
                                bins=[0, 12, 24, 48, 72, 100],
                                labels=['< 1 ano', '1-2 anos', '2-4 anos', '4-6 anos', '> 6 anos'])
    
    # Sidebar - Filtros Interativos
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/data-configuration.png", width=80)
        st.title("🎛️ Filtros")
        st.markdown("---")
        
        # Filtros principais
        tipo_contrato_filter = st.multiselect(
            "📋 Tipo de Contrato",
            options=df['tipo_contrato'].unique(),
            default=df['tipo_contrato'].unique()
        )
        
        servico_internet_filter = st.multiselect(
            "🌐 Serviço de Internet",
            options=df['servico_internet'].unique(),
            default=df['servico_internet'].unique()
        )
        
        metodo_pagamento_filter = st.multiselect(
            "💳 Método de Pagamento",
            options=df['metodo_pagamento'].unique(),
            default=df['metodo_pagamento'].unique()
        )
        
        st.markdown("---")
        
        # Range sliders
        valor_mensal_range = st.slider(
            "💰 Valor Mensal (R$)",
            min_value=float(df['valor_mensal'].min()),
            max_value=float(df['valor_mensal'].max()),
            value=(float(df['valor_mensal'].min()), float(df['valor_mensal'].max()))
        )
        
        tempo_range = st.slider(
            "⏱️ Tempo de Contrato (meses)",
            min_value=int(df['tempo_contrato_meses'].min()),
            max_value=int(df['tempo_contrato_meses'].max()),
            value=(0, 72)
        )
        
        st.markdown("---")
        
        # Status do filtro
        st.info(f"📊 Mostrando {len(df[(df['tipo_contrato'].isin(tipo_contrato_filter)) & (df['servico_internet'].isin(servico_internet_filter)) & (df['metodo_pagamento'].isin(metodo_pagamento_filter))])} registros")
        
        if st.button("🔄 Resetar Filtros", use_container_width=True):
            st.rerun()
    
    # Aplicar filtros
    df_filtered = df[
        (df['tipo_contrato'].isin(tipo_contrato_filter)) &
        (df['servico_internet'].isin(servico_internet_filter)) &
        (df['metodo_pagamento'].isin(metodo_pagamento_filter)) &
        (df['valor_mensal'].between(valor_mensal_range[0], valor_mensal_range[1])) &
        (df['tempo_contrato_meses'].between(tempo_range[0], tempo_range[1]))
    ]
    
    # Header
    st.title("📊 Telecom Churn Analytics")
    st.caption("Dashboard de Análise de Cancelamento de Clientes - Dados Tratados")
    st.markdown("---")
    
    # KPIs em cards
    st.subheader("📈 KPIs Estratégicos")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_clientes = len(df_filtered)
    total_churn = df_filtered['cancelamento'].value_counts().get('Yes', 0)
    taxa_churn = (total_churn / total_clientes) * 100 if total_clientes > 0 else 0
    receita_total = df_filtered['valor_mensal'].sum()
    receita_risco = df_filtered[df_filtered['cancelamento'] == 'Yes']['valor_mensal'].sum()
    ticket_medio_ativo = df_filtered[df_filtered['cancelamento'] == 'No']['valor_mensal'].mean() if len(df_filtered[df_filtered['cancelamento'] == 'No']) > 0 else 0
    ticket_medio_churn = df_filtered[df_filtered['cancelamento'] == 'Yes']['valor_mensal'].mean() if len(df_filtered[df_filtered['cancelamento'] == 'Yes']) > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Clientes</h3>
            <h2>{total_clientes:,}</h2>
            <p>Base total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card warning-card">
            <h3>⚠️ Taxa de Churn</h3>
            <h2>{taxa_churn:.1f}%</h2>
            <p>{total_churn} clientes cancelaram</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card success-card">
            <h3>💰 Receita Mensal</h3>
            <h2>R$ {receita_total:,.0f}</h2>
            <p>Faturamento total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pct_risco = (receita_risco / receita_total) * 100 if receita_total > 0 else 0
        st.markdown(f"""
        <div class="metric-card warning-card">
            <h3>⚠️ Receita em Risco</h3>
            <h2>R$ {receita_risco:,.0f}</h2>
            <p>{pct_risco:.1f}% do total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        diferenca = ((ticket_medio_churn / ticket_medio_ativo) - 1) * 100 if ticket_medio_ativo > 0 else 0
        st.markdown(f"""
        <div class="metric-card info-card">
            <h3>📊 Ticket Médio</h3>
            <h2>R$ {ticket_medio_churn:.0f}</h2>
            <p>{diferenca:+.1f}% vs ativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Abas principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", "📈 Análise de Churn", "👤 Perfil do Cliente", 
        "💰 Análise Financeira", "🎯 Recomendações"
    ])
    
    # TAB 1 - Visão Geral
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Distribuição de Churn")
            churn_counts = df_filtered['cancelamento'].value_counts().reset_index()
            churn_counts.columns = ['Status', 'Quantidade']
            churn_counts['Status'] = churn_counts['Status'].map({'Yes': 'Cancelou', 'No': 'Ativo'})
            
            fig = px.pie(churn_counts, values='Quantidade', names='Status',
                         title='Proporção de Cancelamento',
                         color='Status',
                         color_discrete_map={'Cancelou': '#ff6b6b', 'Ativo': '#51cf66'},
                         hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Churn por Tipo de Contrato")
            contrato_churn = pd.crosstab(df_filtered['tipo_contrato'], df_filtered['cancelamento'])
            contrato_churn['taxa_churn'] = (contrato_churn['Yes'] / contrato_churn.sum(axis=1)) * 100
            contrato_churn = contrato_churn.sort_values('taxa_churn', ascending=False)
            
            fig = px.bar(contrato_churn.reset_index(), x='tipo_contrato', y='taxa_churn',
                         title='Taxa de Churn por Tipo de Contrato (%)',
                         labels={'tipo_contrato': 'Tipo de Contrato', 'taxa_churn': 'Taxa de Churn (%)'},
                         color='taxa_churn', color_continuous_scale='Reds')
            fig.add_hline(y=20, line_dash="dash", line_color="red", 
                          annotation_text="⚠️ Meta Ideal (20%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de tempo de contrato
        st.subheader("⏱️ Tempo de Permanência vs Churn")
        
        fig = make_subplots(rows=1, cols=2, 
                            subplot_titles=('Clientes Ativos', 'Clientes que Cancelaram'),
                            specs=[[{'type': 'box'}, {'type': 'box'}]])
        
        fig.add_trace(go.Box(y=df_filtered[df_filtered['cancelamento'] == 'No']['tempo_contrato_meses'],
                             name='Ativos', marker_color='#51cf66', 
                             boxmean='sd'), row=1, col=1)
        fig.add_trace(go.Box(y=df_filtered[df_filtered['cancelamento'] == 'Yes']['tempo_contrato_meses'],
                             name='Cancelados', marker_color='#ff6b6b',
                             boxmean='sd'), row=1, col=2)
        
        fig.update_layout(height=450, title_text="Distribuição do Tempo de Contrato (meses)")
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2 - Análise de Churn
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💳 Churn por Método de Pagamento")
            pagamento_churn = pd.crosstab(df_filtered['metodo_pagamento'], df_filtered['cancelamento'])
            pagamento_churn['taxa_churn'] = (pagamento_churn['Yes'] / pagamento_churn.sum(axis=1)) * 100
            pagamento_churn = pagamento_churn.sort_values('taxa_churn', ascending=False)
            
            fig = px.bar(pagamento_churn.reset_index(), x='metodo_pagamento', y='taxa_churn',
                         title='Taxa de Churn por Método de Pagamento',
                         labels={'metodo_pagamento': 'Método de Pagamento', 'taxa_churn': 'Taxa de Churn (%)'},
                         color='taxa_churn', color_continuous_scale='Reds')
            fig.update_layout(xaxis_tickangle=-15)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🌐 Churn por Serviço de Internet")
            internet_churn = pd.crosstab(df_filtered['servico_internet'], df_filtered['cancelamento'])
            internet_churn['taxa_churn'] = (internet_churn['Yes'] / internet_churn.sum(axis=1)) * 100
            
            fig = px.bar(internet_churn.reset_index(), x='servico_internet', y='taxa_churn',
                         title='Taxa de Churn por Tipo de Internet',
                         labels={'servico_internet': 'Serviço de Internet', 'taxa_churn': 'Taxa de Churn (%)'},
                         color='taxa_churn', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        # Serviços adicionais
        st.subheader("🔒 Impacto dos Serviços Adicionais no Churn")
        servicos = ['seguranca_online', 'backup_online', 'protecao_dispositivo', 'suporte_tecnico']
        servicos_labels = {'seguranca_online': 'Segurança Online', 'backup_online': 'Backup Online',
                          'protecao_dispositivo': 'Proteção de Dispositivo', 'suporte_tecnico': 'Suporte Técnico'}
        
        servicos_data = []
        for servico in servicos:
            if servico in df_filtered.columns:
                for valor in df_filtered[servico].unique():
                    df_serv = df_filtered[df_filtered[servico] == valor]
                    if len(df_serv) > 0:
                        taxa = (df_serv['cancelamento'] == 'Yes').mean() * 100
                        servicos_data.append({
                            'Serviço': servicos_labels.get(servico, servico),
                            'Status': valor,
                            'Taxa de Churn (%)': taxa,
                            'Clientes': len(df_serv)
                        })
        
        if servicos_data:
            df_servicos = pd.DataFrame(servicos_data)
            fig = px.bar(df_servicos, x='Serviço', y='Taxa de Churn (%)', color='Status',
                         title='Taxa de Churn por Serviço Adicional',
                         barmode='group', color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3 - Perfil do Cliente
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Churn por Gênero")
            genero_churn = pd.crosstab(df_filtered['genero'], df_filtered['cancelamento'])
            genero_churn['taxa_churn'] = (genero_churn['Yes'] / genero_churn.sum(axis=1)) * 100
            
            fig = px.bar(genero_churn.reset_index(), x='genero', y='taxa_churn',
                         title='Taxa de Churn por Gênero',
                         labels={'genero': 'Gênero', 'taxa_churn': 'Taxa de Churn (%)'},
                         color='taxa_churn', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("👴 Churn por Idade")
            if 'idoso' in df_filtered.columns:
                idoso_churn = pd.crosstab(df_filtered['idoso'], df_filtered['cancelamento'])
                idoso_churn['taxa_churn'] = (idoso_churn['Yes'] / idoso_churn.sum(axis=1)) * 100
                idoso_churn.index = idoso_churn.index.map({0: 'Não Idoso', 1: 'Idoso (65+)'})
                
                fig = px.bar(idoso_churn.reset_index(), x='idoso', y='taxa_churn',
                             title='Taxa de Churn por Idade',
                             labels={'idoso': 'Categoria', 'taxa_churn': 'Taxa de Churn (%)'},
                             color='taxa_churn', color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Dados de idade não disponíveis")
        
        st.subheader("📊 Churn por Faixa de Valor Mensal")
        faixa_churn = pd.crosstab(df_filtered['faixa_valor_mensal'], df_filtered['cancelamento'])
        faixa_churn['taxa_churn'] = (faixa_churn['Yes'] / faixa_churn.sum(axis=1)) * 100
        faixa_churn = faixa_churn.sort_values('taxa_churn', ascending=False)
        
        fig = px.bar(faixa_churn.reset_index(), x='faixa_valor_mensal', y='taxa_churn',
                     title='Taxa de Churn por Faixa de Valor Mensal',
                     labels={'faixa_valor_mensal': 'Faixa de Valor Mensal', 'taxa_churn': 'Taxa de Churn (%)'},
                     color='taxa_churn', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 Churn por Faixa de Tempo de Contrato")
        tempo_churn = pd.crosstab(df_filtered['faixa_tempo'], df_filtered['cancelamento'])
        tempo_churn['taxa_churn'] = (tempo_churn['Yes'] / tempo_churn.sum(axis=1)) * 100
        
        fig = px.bar(tempo_churn.reset_index(), x='faixa_tempo', y='taxa_churn',
                     title='Taxa de Churn por Tempo de Contrato',
                     labels={'faixa_tempo': 'Tempo de Contrato', 'taxa_churn': 'Taxa de Churn (%)'},
                     color='taxa_churn', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4 - Análise Financeira
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Distribuição da Receita")
            receita_status = df_filtered.groupby('cancelamento')['valor_mensal'].sum().reset_index()
            receita_status['cancelamento'] = receita_status['cancelamento'].map({'Yes': 'Cancelados', 'No': 'Ativos'})
            
            fig = px.pie(receita_status, values='valor_mensal', names='cancelamento',
                         title='Distribuição da Receita Mensal',
                         color='cancelamento',
                         color_discrete_map={'Cancelados': '#ff6b6b', 'Ativos': '#51cf66'},
                         hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Ticket Médio por Contrato")
            if 'tipo_contrato' in df_filtered.columns:
                ticket_contrato = df_filtered.groupby(['tipo_contrato', 'cancelamento'])['valor_mensal'].mean().reset_index()
                ticket_contrato['cancelamento'] = ticket_contrato['cancelamento'].map({'Yes': 'Cancelados', 'No': 'Ativos'})
                ticket_contrato = ticket_contrato.dropna()
                
                fig = px.bar(ticket_contrato, x='tipo_contrato', y='valor_mensal', color='cancelamento',
                             title='Ticket Médio por Tipo de Contrato',
                             labels={'tipo_contrato': 'Tipo de Contrato', 'valor_mensal': 'Valor Médio (R$)'},
                             barmode='group',
                             color_discrete_map={'Cancelados': '#ff6b6b', 'Ativos': '#51cf66'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Top clientes em risco
        st.subheader("🚨 Top 20 Clientes de Alto Valor em Risco")
        high_value_risk = df_filtered[df_filtered['cancelamento'] == 'Yes'].nlargest(20, 'valor_mensal')[
            ['id_cliente', 'valor_mensal', 'valor_total', 'tempo_contrato_meses', 'tipo_contrato', 'metodo_pagamento']
        ].head(10)
        
        if len(high_value_risk) > 0:
            high_value_risk.columns = ['ID Cliente', 'Valor Mensal', 'Valor Total', 'Meses', 'Contrato', 'Pagamento']
            st.dataframe(high_value_risk, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum cliente em risco no filtro atual")
    
    # TAB 5 - Recomendações
    with tab5:
        st.subheader("🎯 Recomendações Estratégicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ⚠️ Principais Fatores de Risco
            
            | Fator | Risco | Impacto |
            |-------|-------|---------|
            | **Contrato Mensal** | 🔴 Muito Alto | 42.7% de churn |
            | **Electronic Check** | 🔴 Alto | 45.3% de churn |
            | **Fibra Óptica** | 🟡 Médio | 41.9% de churn |
            | **Sem Serviços Adicionais** | 🟡 Médio | 35%+ de churn |
            | **Cliente Novo (< 1 ano)** | 🟡 Médio | 50% dos churns |
            """)
            
            st.markdown("""
            ### 📊 Métricas de Impacto
            
            | Métrica | Valor | Benchmark |
            |---------|-------|-----------|
            | Churn Rate | {:.1f}% | Ideal < 15% |
            | Receita em Risco | R$ {:.0f} | Muito Alto |
            | Ticket Médio Churn | R$ {:.0f} | +21% vs média |
            """.format(taxa_churn, receita_risco, ticket_medio_churn))
        
        with col2:
            st.markdown("""
            ### 💰 ROI de Retenção
            
            ```python
            Custo Aquisição (CAC): ~R$ 500/cliente
            Custo Retenção: ~R$ 100/cliente
            Economia por cliente retido: ~R$ 400
            ROI = 400% 
                        """)

        st.markdown("---")

        st.subheader("📋 Plano de Ação Prioritário")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""

                🔴 Fase 1 - Urgente
                Ações Imediatas:

                Contratos Mensais

                Migração para plano anual com 1 mês grátis

                Meta: 30% migração em 3 meses

                Electronic Check

                5% desconto para débito automático

                Campanha de e-mail marketing
                """)

        with col2:
            st.markdown("""

                🟡 Fase 2 - Curto Prazo
                Próximos 30-60 dias:

                Novos Clientes

                Programa de onboarding

                Check-in mensal no 1º ano

                Cross-Selling

                Pacotes de segurança online

                Backup + proteção com desconto
                """)

        with col3:
            st.markdown("""

                🟢 Fase 3 - Médio Prazo
                Monitoramento Contínuo:

                Dashboard de Risco

                Alertas automáticos

                Score de propensão a churn

                Programa de Fidelidade

                Pontos por tempo de casa

                Benefícios exclusivos
                """)

        st.markdown("---")

        #Alerta final
        st.warning(f"""
        💡 Alerta Estratégico:

        A taxa de churn atual é de {taxa_churn:.1f}%, significativamente acima do ideal para o setor de telecom (< 15%).

        Cada cliente que cancela representa uma perda média de R$ {ticket_medio_churn:.2f} por mês em receita.

        Investir em retenção é 5 a 25 vezes mais barato que adquirir novos clientes.
        """)

        #Footer
        st.markdown("---")
        st.caption("📊 Telecom Churn Analytics Dashboard | Desenvolvido com Streamlit | Fonte: IBM Telco Customer Churn (Dados Tratados)")
        st.caption(f"🔄 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

else:
    st.warning("⚠️ Não foi possível carregar os dados. Verifique o arquivo 'telco_customer_churn_tratado.csv' e tente novamente.")

