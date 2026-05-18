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
    </div>""", unsafe_allow_html=True)

    ativos = len(df[df["Status"]=="Ativo"])
    vol    = df["Volume Total (R$)"].sum()
    nps    = df["NPS"].mean()

    st.markdown(f"""
    <div class="kpi-wrap" style="padding-top:8px;padding-bottom:8px;">
      <div class="kpi-grid">
        <div class="kpi-item">
          <div class="kpi-label">Total Clientes</div>
          <div class="kpi-value">{len(df)}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Clientes Ativos</div>
          <div class="kpi-value">{ativos}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Volume Total</div>
          <div class="kpi-value">R$ {vol/1e6:.1f}M</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">NPS Médio</div>
          <div class="kpi-value">{nps:.0f}</div>
        </div>
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 32px 16px;">
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st_f = st.multiselect("Status", df["Status"].unique(), default=list(df["Status"].unique()))
    with c2:
        sg_f = st.multiselect("Segmento", df["Segmento"].unique(), default=list(df["Segmento"].unique()))

    df_f = df[df["Status"].isin(st_f) & df["Segmento"].isin(sg_f)]

    col1, col2 = st.columns(2)
    with col1:
        top = df_f.sort_values("Volume Total (R$)", ascending=False)
        fig = px.bar(top, x="Cliente", y="Volume Total (R$)", color="Segmento",
                     title="Volume por Cliente (R$)",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748b"),
            title=dict(font=dict(size=13, color="#0f172a"), x=0),
            margin=dict(t=36, b=80, l=0, r=0),
            xaxis=dict(tickangle=35, showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            showlegend=False, height=300
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        fig2 = px.scatter(df_f, x="Total Pedidos", y="NPS",
                          size="Volume Total (R$)", color="Segmento",
                          hover_name="Cliente", title="NPS vs Volume de Pedidos",
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748b"),
            title=dict(font=dict(size=13, color="#0f172a"), x=0),
            margin=dict(t=36, b=20, l=0, r=0), height=300
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    df_show = df_f.copy()
    df_show["Volume Total (R$)"] = df_show["Volume Total (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))
    df_show["Ticket Médio (R$)"] = df_show["Ticket Médio (R$)"].apply(lambda x: f"R$ {x:,.0f}".replace(",","."))

    st.dataframe(
        df_show[["Cliente","Segmento","Região","Status","Total Pedidos",
                 "Volume Total (R$)","Ticket Médio (R$)","NPS","Gerente de Conta","Desde"]],
        use_container_width=True, hide_index=True,
        column_config={"NPS": st.column_config.ProgressColumn("NPS", min_value=0, max_value=100, format="%d")}
    )

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("☁️ Exportar CSV", csv, "clientes.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
