import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos, carregar_tarefas

def render():
    df = carregar_pedidos()
    df_t = carregar_tarefas()

    st.markdown("""
    <div class="page-header">
        <h2>🏠 Dashboard Executivo</h2>
        <p>Visão consolidada de operações logísticas em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_pedidos = len(df)
    valor_total = df["Valor (R$)"].sum()
    entregues = len(df[df["Status"] == "Entregue"])
    taxa_entrega = entregues / total_pedidos * 100
    em_transito = len(df[df["Status"] == "Em Trânsito"])
    cancelados = len(df[df["Status"] == "Cancelado"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card" style="border-color:#3b82f6">
            <div class="kpi-label">Total de Pedidos</div>
            <div class="kpi-value">{total_pedidos}</div>
            <div class="kpi-delta">↑ últimos 90 dias</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card" style="border-color:#22c55e">
            <div class="kpi-label">Volume Total</div>
            <div class="kpi-value">R$ {valor_total/1e6:.1f}M</div>
            <div class="kpi-delta">↑ ticket médio R$ {valor_total/total_pedidos:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card" style="border-color:#f59e0b">
            <div class="kpi-label">Taxa de Entrega</div>
            <div class="kpi-value">{taxa_entrega:.1f}%</div>
            <div class="kpi-delta">{entregues} pedidos entregues</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card" style="border-color:#ef4444">
            <div class="kpi-label">Em Trânsito</div>
            <div class="kpi-value">{em_transito}</div>
            <div class="kpi-delta">{cancelados} cancelados</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráficos linha 1 ──────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        df["Data Criação"] = pd.to_datetime(df["Data Criação"])
        serie = df.groupby(df["Data Criação"].dt.to_period("W").astype(str))["Valor (R$)"].sum().reset_index()
        serie.columns = ["Semana", "Valor"]
        fig = px.area(serie, x="Semana", y="Valor",
                      title="Volume por Semana (R$)",
                      color_discrete_sequence=["#3b82f6"])
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40, b=20, l=10, r=10),
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=True, gridcolor="#f0f4ff")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        status_count = df["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Qtd"]
        cores = {"Entregue":"#22c55e","Em Trânsito":"#3b82f6",
                 "Em Processamento":"#f59e0b","Pendente":"#94a3b8","Cancelado":"#ef4444"}
        fig2 = px.pie(status_count, values="Qtd", names="Status",
                      title="Distribuição por Status",
                      color="Status", color_discrete_map=cores, hole=0.5)
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40, b=20, l=10, r=10),
            legend=dict(orientation="h", y=-0.15)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráficos linha 2 ──────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        por_regiao = df.groupby("Região")["Valor (R$)"].sum().reset_index().sort_values("Valor (R$)", ascending=True)
        fig3 = px.bar(por_regiao, x="Valor (R$)", y="Região", orientation="h",
                      title="Volume por Região (R$)",
                      color_discrete_sequence=["#1a2744"])
        fig3.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40, b=20, l=10, r=10),
            xaxis=dict(showgrid=True, gridcolor="#f0f4ff"),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        tarefas_status = df_t["Status"].value_counts().reset_index()
        tarefas_status.columns = ["Status", "Qtd"]
        cores_t = {"A Fazer":"#94a3b8","Em Andamento":"#3b82f6","Concluída":"#22c55e","Bloqueada":"#ef4444"}
        fig4 = px.bar(tarefas_status, x="Status", y="Qtd",
                      title="Tarefas por Status",
                      color="Status", color_discrete_map=cores_t)
        fig4.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40, b=20, l=10, r=10),
            showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f4ff")
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── Top clientes ──────────────────────────────────────────────────────────
    st.markdown("#### 🏆 Top 5 Clientes por Volume")
    top = df.groupby("Cliente")["Valor (R$)"].sum().sort_values(ascending=False).head(5).reset_index()
    top["Volume"] = top["Valor (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))
    top["Rank"] = ["🥇","🥈","🥉","4º","5º"]
    st.dataframe(top[["Rank","Cliente","Volume"]], hide_index=True, use_container_width=True)