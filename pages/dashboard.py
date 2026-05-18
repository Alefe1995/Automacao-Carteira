import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos, carregar_tarefas

COR_PRINCIPAL = "#0f172a"
COR_GRAFICO   = "#1e3a5f"

def render():
    df  = carregar_pedidos()
    df_t = carregar_tarefas()

    st.markdown("""
    <div class="page-header">
        <h2>🏠 Dashboard Executivo</h2>
        <p>Visão consolidada de operações logísticas em tempo real</p>
    </div>""", unsafe_allow_html=True)

    # ── KPIs ──
    total   = len(df)
    volume  = df["Valor (R$)"].sum()
    entregues = len(df[df["Status"]=="Entregue"])
    taxa    = entregues/total*100
    transito = len(df[df["Status"]=="Em Trânsito"])
    cancelados = len(df[df["Status"]=="Cancelado"])
    ticket  = volume/total

    st.markdown(f"""
    <div class="kpi-wrap">
      <div class="kpi-grid">
        <div class="kpi-item">
          <div class="kpi-label">Total de Pedidos</div>
          <div class="kpi-value">{total}</div>
          <div class="kpi-sub">↑ últimos 90 dias</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Volume Total</div>
          <div class="kpi-value">R$ {volume/1e6:.1f}M</div>
          <div class="kpi-sub">↑ ticket médio R$ {ticket:,.0f}".replace(",",".")</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Taxa de Entrega</div>
          <div class="kpi-value">{taxa:.1f}%</div>
          <div class="kpi-sub">{entregues} pedidos entregues</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Em Trânsito</div>
          <div class="kpi-value">{transito}</div>
          <div class="kpi-sub">{cancelados} cancelados</div>
        </div>
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 32px 24px;">
    """, unsafe_allow_html=True)

    # ── Gráficos ──
    with st.container():
        st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 2])

        with col1:
            df["Data Criação"] = pd.to_datetime(df["Data Criação"])
            serie = df.groupby(df["Data Criação"].dt.to_period("W").astype(str))["Valor (R$)"].sum().reset_index()
            serie.columns = ["Semana", "Valor"]
            fig = px.area(serie, x="Semana", y="Valor", title="Volume por Semana (R$)",
                          color_discrete_sequence=[COR_GRAFICO])
            fig.update_traces(line_width=2, fillcolor="rgba(30,58,95,0.15)")
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Inter", size=11, color="#64748b"),
                title=dict(font=dict(size=13, color="#0f172a"), x=0),
                margin=dict(t=36, b=40, l=0, r=0),
                xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickformat=",.0f"),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            sc = df["Status"].value_counts().reset_index()
            sc.columns = ["Status", "Qtd"]
            cores = {"Entregue":"#22c55e","Em Trânsito":"#3b82f6",
                     "Em Processamento":"#f59e0b","Pendente":"#94a3b8","Cancelado":"#ef4444"}
            fig2 = px.pie(sc, values="Qtd", names="Status", title="Distribuição por Status",
                          color="Status", color_discrete_map=cores, hole=0.52)
            fig2.update_traces(textfont_size=11)
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Inter", size=11, color="#64748b"),
                title=dict(font=dict(size=13, color="#0f172a"), x=0),
                margin=dict(t=36, b=0, l=0, r=0),
                legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
                height=300
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        col3, col4 = st.columns(2)

        with col3:
            reg = df.groupby("Região")["Valor (R$)"].sum().reset_index().sort_values("Valor (R$)", ascending=True)
            fig3 = px.bar(reg, x="Valor (R$)", y="Região", orientation="h",
                          title="Volume por Região (R$)",
                          color_discrete_sequence=[COR_GRAFICO])
            fig3.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Inter", size=11, color="#64748b"),
                title=dict(font=dict(size=13, color="#0f172a"), x=0),
                margin=dict(t=36, b=20, l=0, r=0),
                xaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickformat=",.0f"),
                yaxis=dict(showgrid=False),
                height=280
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        with col4:
            ts = df_t["Status"].value_counts().reset_index()
            ts.columns = ["Status", "Qtd"]
            cores_t = {"A Fazer":"#94a3b8","Em Andamento":"#3b82f6",
                       "Concluída":"#22c55e","Bloqueada":"#ef4444"}
            fig4 = px.bar(ts, x="Status", y="Qtd", title="Tarefas por Status",
                          color="Status", color_discrete_map=cores_t)
            fig4.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font=dict(family="Inter", size=11, color="#64748b"),
                title=dict(font=dict(size=13, color="#0f172a"), x=0),
                margin=dict(t=36, b=20, l=0, r=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                showlegend=False, height=280
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

        # Top 5
        st.markdown("#### 🏆 Top 5 Clientes por Volume")
        top = df.groupby("Cliente")["Valor (R$)"].sum().sort_values(ascending=False).head(5).reset_index()
        top.insert(0, "Rank", ["🥇","🥈","🥉","4º","5º"])
        top["Volume"] = top["Valor (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))
        st.dataframe(top[["Rank","Cliente","Volume"]], hide_index=True, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)
