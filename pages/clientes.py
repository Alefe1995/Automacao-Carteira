import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_clientes

def render():
    df = carregar_clientes()

    st.markdown("""
    <div class="page-header">
        <h2>⭐ Clientes Estratégicos</h2>
        <p>Painel de relacionamento e performance dos principais clientes</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    ativos = len(df[df["Status"]=="Ativo"])
    volume_total = df["Volume Total (R$)"].sum()
    nps_medio = df["NPS"].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Clientes", len(df))
    k2.metric("Clientes Ativos", ativos)
    k3.metric("Volume Total", f"R$ {volume_total/1e6:.1f}M")
    k4.metric("NPS Médio", f"{nps_medio:.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    c1, c2 = st.columns(2)
    with c1:
        status_f = st.multiselect("Status", df["Status"].unique(), default=list(df["Status"].unique()))
    with c2:
        seg_f = st.multiselect("Segmento", df["Segmento"].unique(), default=list(df["Segmento"].unique()))

    df_f = df[df["Status"].isin(status_f) & df["Segmento"].isin(seg_f)]

    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        top = df_f.sort_values("Volume Total (R$)", ascending=False)
        fig = px.bar(top, x="Cliente", y="Volume Total (R$)",
                     color="Segmento", title="Volume por Cliente (R$)",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40,b=80,l=10,r=10),
            xaxis=dict(tickangle=35, showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f4ff"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(df_f, x="Total Pedidos", y="NPS",
                          size="Volume Total (R$)", color="Segmento",
                          hover_name="Cliente", title="NPS vs Volume de Pedidos",
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabela de clientes
    st.markdown("#### 📋 Detalhe por Cliente")
    df_show = df_f.copy()
    df_show["Volume Total (R$)"] = df_show["Volume Total (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))
    df_show["Ticket Médio (R$)"] = df_show["Ticket Médio (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))

    # NPS como barra de progresso no dataframe
    st.dataframe(
        df_show[["Cliente","Segmento","Região","Status","Total Pedidos","Volume Total (R$)","Ticket Médio (R$)","NPS","Gerente de Conta","Desde"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "NPS": st.column_config.ProgressColumn("NPS", min_value=0, max_value=100, format="%d"),
        }
    )

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar CSV", csv, "clientes_estrategicos.csv", "text/csv")