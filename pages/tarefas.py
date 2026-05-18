import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_tarefas, cor_prioridade

STATUS_COR = {
    "A Fazer":     ("#f1f5f9", "#64748b"),
    "Em Andamento":("#dbeafe", "#1d4ed8"),
    "Concluída":   ("#dcfce7", "#15803d"),
    "Bloqueada":   ("#fee2e2", "#b91c1c"),
}

def render():
    df = carregar_tarefas()

    st.markdown("""
    <div class="page-header">
        <h2>✅ Gerenciamento de Tarefas</h2>
        <p>Acompanhe e gerencie as tarefas operacionais da equipe</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Tarefas", len(df))
    k2.metric("Concluídas", len(df[df["Status"]=="Concluída"]))
    k3.metric("Bloqueadas", len(df[df["Status"]=="Bloqueada"]))
    k4.metric("Alta Prioridade", len(df[df["Prioridade"]=="Alta"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    c1, c2, c3 = st.columns(3)
    with c1:
        status_f = st.multiselect("Status", df["Status"].unique(), default=list(df["Status"].unique()), key="tar_status")
    with c2:
        prio_f = st.multiselect("Prioridade", df["Prioridade"].unique(), default=list(df["Prioridade"].unique()), key="tar_prio")
    with c3:
        resp_f = st.multiselect("Responsável", df["Responsável"].unique(), default=list(df["Responsável"].unique()), key="tar_resp")

    df_f = df[df["Status"].isin(status_f) & df["Prioridade"].isin(prio_f) & df["Responsável"].isin(resp_f)]

    # Gráfico por responsável
    col_g, col_t = st.columns([1,2])
    with col_g:
        por_resp = df_f.groupby(["Responsável","Status"]).size().reset_index(name="Qtd")
        fig = px.bar(por_resp, x="Qtd", y="Responsável", color="Status", orientation="h",
                     title="Tarefas por Responsável",
                     color_discrete_map={
                         "A Fazer":"#94a3b8","Em Andamento":"#3b82f6",
                         "Concluída":"#22c55e","Bloqueada":"#ef4444"
                     })
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font_family="Syne",
            margin=dict(t=40,b=20,l=10,r=10), height=300,
            legend=dict(orientation="h", y=-0.3)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_t:
        st.markdown("#### Lista de Tarefas")
        for _, row in df_f.iterrows():
            bg, txt = STATUS_COR.get(row["Status"], ("#f1f5f9","#64748b"))
            prio_icon = cor_prioridade(row["Prioridade"])
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:14px 18px;
                        margin-bottom:8px; box-shadow:0 1px 6px rgba(0,0,0,0.06);
                        display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div style="flex:1; min-width:180px;">
                    <div style="font-family:'Syne',sans-serif; font-weight:600; font-size:13px; color:#0a0f1e;">
                        {row['Título']}
                    </div>
                    <div style="font-size:11px; color:#6b7a9d; margin-top:3px;">
                        👤 {row['Responsável']} &nbsp;|&nbsp; 📅 Prazo: {row['Prazo']} &nbsp;|&nbsp; 🔗 {row['Pedido Relacionado']}
                    </div>
                </div>
                <div style="display:flex; gap:8px; align-items:center; margin-top:4px;">
                    <span style="background:{bg}; color:{txt}; border-radius:20px; padding:3px 10px;
                                 font-size:11px; font-weight:600;">{row['Status']}</span>
                    <span style="font-size:13px;">{prio_icon}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar CSV", csv, "tarefas.csv", "text/csv")