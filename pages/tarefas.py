import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_tarefas

STATUS_BADGE = {
    "A Fazer":      ("badge-afazer",    "#475569"),
    "Em Andamento": ("badge-emandamento","#1e40af"),
    "Concluída":    ("badge-concluida",  "#166534"),
    "Bloqueada":    ("badge-bloqueada",  "#991b1b"),
}
PRIO_COR = {"Alta":"#ef4444","Média":"#f59e0b","Baixa":"#22c55e"}

def render():
    df = carregar_tarefas()

    st.markdown("""
    <div class="page-header">
        <h2>✅ Gerenciamento de Tarefas</h2>
        <p>Acompanhe e gerencie as tarefas operacionais da equipe</p>
    </div>""", unsafe_allow_html=True)

    # ── KPIs ──
    st.markdown(f"""
    <div class="kpi-wrap" style="padding-top:8px;padding-bottom:8px;">
      <div class="kpi-grid">
        <div class="kpi-item">
          <div class="kpi-label">Total Tarefas</div>
          <div class="kpi-value">{len(df)}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Concluídas</div>
          <div class="kpi-value">{len(df[df['Status']=='Concluída'])}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Bloqueadas</div>
          <div class="kpi-value">{len(df[df['Status']=='Bloqueada'])}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Alta Prioridade</div>
          <div class="kpi-value">{len(df[df['Prioridade']=='Alta'])}</div>
        </div>
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 32px 16px;">
    """, unsafe_allow_html=True)

    # ── Filtros ──
    with st.container():
        st.markdown('<div style="padding:0 32px 12px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st_f = st.multiselect("Status", df["Status"].unique(),
                default=list(df["Status"].unique()), key="tar_s")
        with c2:
            pr_f = st.multiselect("Prioridade", df["Prioridade"].unique(),
                default=list(df["Prioridade"].unique()), key="tar_p")
        with c3:
            rs_f = st.multiselect("Responsável", df["Responsável"].unique(),
                default=list(df["Responsável"].unique()), key="tar_r")
        st.markdown('</div>', unsafe_allow_html=True)

    df_f = df[df["Status"].isin(st_f) &
              df["Prioridade"].isin(pr_f) &
              df["Responsável"].isin(rs_f)]

    # ── Layout: gráfico + lista ──
    st.markdown('<div style="padding:0 32px 32px;">', unsafe_allow_html=True)
    col_g, col_l = st.columns([2, 3])

    with col_g:
        por_resp = df_f.groupby(["Responsável","Status"]).size().reset_index(name="Qtd")
        fig = px.bar(por_resp, x="Qtd", y="Responsável", color="Status",
                     orientation="h", title="Tarefas por Responsável",
                     color_discrete_map={
                         "A Fazer":"#94a3b8","Em Andamento":"#3b82f6",
                         "Concluída":"#22c55e","Bloqueada":"#ef4444"
                     })
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=11, color="#64748b"),
            title=dict(font=dict(size=13, color="#0f172a"), x=0),
            margin=dict(t=36, b=20, l=0, r=0),
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
            legend=dict(orientation="h", y=-0.25, font=dict(size=10)),
            height=340
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_l:
        st.markdown("#### Lista de Tarefas")
        for _, row in df_f.iterrows():
            badge_cls, badge_txt_col = STATUS_BADGE.get(row["Status"], ("badge-afazer","#475569"))
            prio_cor = PRIO_COR.get(row["Prioridade"], "#94a3b8")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:10px 0;border-bottom:1px solid #f1f5f9;">
                <div style="flex:1;min-width:0;">
                    <div style="font-size:13px;font-weight:500;color:#0f172a;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {row['Título']}
                    </div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">
                        👤 {row['Responsável']} &nbsp;|&nbsp;
                        📅 Prazo: {row['Prazo']} &nbsp;|&nbsp;
                        🔗 {row['Pedido Relacionado']}
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:8px;margin-left:12px;flex-shrink:0;">
                    <span class="badge {badge_cls}">{row['Status']}</span>
                    <span style="color:{prio_cor};font-size:16px;">●</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("☁️ Exportar CSV", csv, "tarefas.csv", "text/csv")
