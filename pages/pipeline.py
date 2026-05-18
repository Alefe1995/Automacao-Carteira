import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos, cor_prioridade

COLUNAS = ["Pendente", "Em Processamento", "Em Trânsito", "Entregue", "Cancelado"]
CORES = {
    "Pendente":          ("#fef3c7", "#b45309", "#f59e0b"),
    "Em Processamento":  ("#dbeafe", "#1d4ed8", "#3b82f6"),
    "Em Trânsito":       ("#e0f2fe", "#0369a1", "#0ea5e9"),
    "Entregue":          ("#dcfce7", "#15803d", "#22c55e"),
    "Cancelado":         ("#fee2e2", "#b91c1c", "#ef4444"),
}

def render():
    df = carregar_pedidos()

    st.markdown("""
    <div class="page-header">
        <h2>🔄 Pipeline de Pedidos</h2>
        <p>Visualização kanban do fluxo operacional por status</p>
    </div>
    """, unsafe_allow_html=True)

    # Filtros rápidos
    col_f1, col_f2, col_f3 = st.columns([2,2,4])
    with col_f1:
        prio_f = st.multiselect("Prioridade", df["Prioridade"].unique(), default=list(df["Prioridade"].unique()), key="pipe_prio")
    with col_f2:
        resp_f = st.multiselect("Responsável", df["Responsável"].unique(), default=list(df["Responsável"].unique()), key="pipe_resp")
    with col_f3:
        busca_f = st.text_input("Buscar cliente / pedido", key="pipe_busca")

    df_f = df[df["Prioridade"].isin(prio_f) & df["Responsável"].isin(resp_f)]
    if busca_f:
        df_f = df_f[df_f["Cliente"].str.contains(busca_f, case=False) | df_f["ID"].str.contains(busca_f, case=False)]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Kanban via HTML ────────────────────────────────────────────────────────
    cols = st.columns(len(COLUNAS))

    for i, status in enumerate(COLUNAS):
        bg, text_color, accent = CORES[status]
        grupo = df_f[df_f["Status"] == status]

        with cols[i]:
            st.markdown(f"""
            <div style="background:{bg}; border-top:3px solid {accent}; border-radius:12px;
                        padding:12px; margin-bottom:8px;">
                <span style="color:{text_color}; font-family:'Syne',sans-serif; font-weight:700; font-size:14px;">
                    {status}
                </span>
                <span style="background:{accent}; color:white; border-radius:20px;
                             padding:2px 8px; font-size:11px; font-weight:600; float:right;">
                    {len(grupo)}
                </span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in grupo.head(15).iterrows():
                prio_icon = cor_prioridade(row["Prioridade"])
                valor_fmt = f"R$ {row['Valor (R$)']:,.0f}".replace(",",".")
                st.markdown(f"""
                <div style="background:white; border-radius:10px; padding:12px 14px;
                            margin-bottom:8px; box-shadow:0 1px 6px rgba(0,0,0,0.07);
                            border-left:3px solid {accent};">
                    <div style="font-family:'Syne',sans-serif; font-size:12px; font-weight:700;
                                color:#0a0f1e;">{row['ID']}</div>
                    <div style="font-size:11px; color:#6b7a9d; margin:3px 0;
                                overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{row['Cliente']}</div>
                    <div style="display:flex; justify-content:space-between; margin-top:6px;">
                        <span style="font-size:11px; color:#374151; font-weight:500;">{valor_fmt}</span>
                        <span style="font-size:11px;">{prio_icon} {row['Prioridade']}</span>
                    </div>
                    <div style="font-size:10px; color:#94a3b8; margin-top:4px;">👤 {row['Responsável']}</div>
                </div>
                """, unsafe_allow_html=True)

            if len(grupo) > 15:
                st.caption(f"+ {len(grupo)-15} pedidos não exibidos")