import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_auditoria

def render():
    df = carregar_auditoria()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    st.markdown("""
    <div class="page-header">
        <h2>🔍 Log de Auditoria</h2>
        <p>Rastreamento completo de ações e acessos no sistema</p>
    </div>""", unsafe_allow_html=True)

    sucesso = len(df[df["Resultado"]=="Sucesso"])
    taxa    = sucesso/len(df)*100

    st.markdown(f"""
    <div class="kpi-wrap" style="padding-top:8px;padding-bottom:8px;">
      <div class="kpi-grid">
        <div class="kpi-item">
          <div class="kpi-label">Total Eventos</div>
          <div class="kpi-value">{len(df)}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Usuários Únicos</div>
          <div class="kpi-value">{df['Usuário'].nunique()}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Falhas</div>
          <div class="kpi-value">{len(df[df['Resultado']=='Falha'])}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Taxa de Sucesso</div>
          <div class="kpi-value">{taxa:.1f}%</div>
        </div>
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 32px 16px;">
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        us_f = st.multiselect("Usuário", df["Usuário"].unique(), default=list(df["Usuário"].unique()))
    with c2:
        ac_f = st.multiselect("Ação", df["Ação"].unique(), default=list(df["Ação"].unique()))
    with c3:
        re_f = st.multiselect("Resultado", df["Resultado"].unique(), default=list(df["Resultado"].unique()))

    df_f = df[df["Usuário"].isin(us_f) & df["Ação"].isin(ac_f) & df["Resultado"].isin(re_f)]

    col1, col2 = st.columns([3,2])
    with col1:
        tl = df_f.groupby(df_f["Timestamp"].dt.date).size().reset_index(name="Eventos")
        tl.columns = ["Data","Eventos"]
        fig = px.line(tl, x="Data", y="Eventos", title="Atividade Diária",
                      markers=True, color_discrete_sequence=["#3b82f6"])
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748b"),
            title=dict(font=dict(size=13, color="#0f172a"), x=0),
            margin=dict(t=36, b=20, l=0, r=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            height=280
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        pa = df_f["Ação"].value_counts().reset_index()
        pa.columns = ["Ação","Qtd"]
        fig2 = px.bar(pa, x="Qtd", y="Ação", orientation="h",
                      title="Ações frequentes",
                      color_discrete_sequence=["#0f172a"])
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748b"),
            title=dict(font=dict(size=13, color="#0f172a"), x=0),
            margin=dict(t=36, b=20, l=0, r=0),
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
            height=280
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    df_show = df_f.sort_values("Timestamp", ascending=False).copy()
    df_show["Timestamp"] = df_show["Timestamp"].dt.strftime("%d/%m/%Y %H:%M:%S")
    st.dataframe(
        df_show[["ID","Timestamp","Usuário","Ação","Entidade","IP","Resultado"]],
        use_container_width=True, hide_index=True, height=380
    )

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("☁️ Exportar Log", csv, "auditoria.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
