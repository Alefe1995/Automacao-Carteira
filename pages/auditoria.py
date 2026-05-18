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
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Eventos", len(df))
    k2.metric("Usuários Únicos", df["Usuário"].nunique())
    k3.metric("Falhas", len(df[df["Resultado"]=="Falha"]))
    k4.metric("Taxa de Sucesso", f"{len(df[df['Resultado']=='Sucesso'])/len(df)*100:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    c1, c2, c3 = st.columns(3)
    with c1:
        usuario_f = st.multiselect("Usuário", df["Usuário"].unique(), default=list(df["Usuário"].unique()))
    with c2:
        acao_f = st.multiselect("Ação", df["Ação"].unique(), default=list(df["Ação"].unique()))
    with c3:
        result_f = st.multiselect("Resultado", df["Resultado"].unique(), default=list(df["Resultado"].unique()))

    df_f = df[df["Usuário"].isin(usuario_f) & df["Ação"].isin(acao_f) & df["Resultado"].isin(result_f)]

    # Gráfico de atividade
    col1, col2 = st.columns([3,2])
    with col1:
        timeline = df_f.groupby(df_f["Timestamp"].dt.date).size().reset_index(name="Eventos")
        timeline.columns = ["Data","Eventos"]
        fig = px.line(timeline, x="Data", y="Eventos", title="Atividade Diária",
                      markers=True, color_discrete_sequence=["#3b82f6"])
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40,b=20,l=10,r=10),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#f0f4ff")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        por_acao = df_f["Ação"].value_counts().reset_index()
        por_acao.columns = ["Ação","Qtd"]
        fig2 = px.bar(por_acao, x="Qtd", y="Ação", orientation="h",
                      title="Ações mais frequentes",
                      color_discrete_sequence=["#1a2744"])
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40,b=20,l=10,r=10),
            xaxis=dict(showgrid=True,gridcolor="#f0f4ff"), yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tabela de logs
    st.markdown("#### 📋 Registro de Eventos")
    df_show = df_f.sort_values("Timestamp", ascending=False).copy()
    df_show["Timestamp"] = df_show["Timestamp"].dt.strftime("%d/%m/%Y %H:%M:%S")

    def highlight_falha(row):
        return ['background-color: #fee2e2' if row["Resultado"]=="Falha" else '' for _ in row]

    st.dataframe(
        df_show[["ID","Timestamp","Usuário","Ação","Entidade","IP","Resultado"]],
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "Resultado": st.column_config.TextColumn("Resultado", width=90),
        }
    )

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar Log", csv, "auditoria.csv", "text/csv")