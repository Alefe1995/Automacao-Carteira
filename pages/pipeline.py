import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos

COLS = [
    ("Pendente",         "#f59e0b", "#fef3c7", "#92400e"),
    ("Em Processamento", "#3b82f6", "#eff6ff", "#1e40af"),
    ("Em Trânsito",      "#0ea5e9", "#f0f9ff", "#075985"),
    ("Entregue",         "#22c55e", "#f0fdf4", "#166534"),
    ("Cancelado",        "#ef4444", "#fef2f2", "#991b1b"),
]

def dot(p):
    c = {"Alta":"#ef4444","Média":"#f59e0b","Baixa":"#22c55e"}.get(p,"#94a3b8")
    return f'<span style="color:{c};">●</span>'

def render():
    df = carregar_pedidos()

    st.markdown("""
    <div class="page-header">
        <h2>🔄 Pipeline de Pedidos</h2>
        <p>Visualização kanban do fluxo operacional por status</p>
    </div>""", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 32px 8px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,2,3])
        with c1:
            prio_f = st.multiselect("Prioridade", df["Prioridade"].unique(),
                default=list(df["Prioridade"].unique()), key="pip_prio")
        with c2:
            resp_f = st.multiselect("Responsável", df["Responsável"].unique(),
                default=list(df["Responsável"].unique()), key="pip_resp")
        with c3:
            busca = st.text_input("Buscar cliente / pedido", key="pip_busca")
        st.markdown('</div>', unsafe_allow_html=True)

    df_f = df[df["Prioridade"].isin(prio_f) & df["Responsável"].isin(resp_f)]
    if busca:
        df_f = df_f[df_f["Cliente"].str.contains(busca, case=False) |
                    df_f["ID"].str.contains(busca, case=False)]

    st.markdown('<div style="padding:0 32px 32px;">', unsafe_allow_html=True)
    cols = st.columns(len(COLS))

    for i, (status, accent, bg, txt) in enumerate(COLS):
        grupo = df_f[df_f["Status"] == status]
        with cols[i]:
            st.markdown(f"""
            <div style="background:{bg};border-top:3px solid {accent};
                        border-radius:10px;padding:10px 12px;margin-bottom:10px;
                        display:flex;justify-content:space-between;align-items:center;">
                <span style="color:{txt};font-size:13px;font-weight:600;">{status}</span>
                <span style="background:{accent};color:white;border-radius:20px;
                             padding:1px 8px;font-size:11px;font-weight:700;">{len(grupo)}</span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in grupo.head(20).iterrows():
                val = f"R$ {row['Valor (R$)']:,.0f}".replace(",",".")
                st.markdown(f"""
                <div style="background:white;border-radius:8px;padding:10px 12px;
                            margin-bottom:6px;border:1px solid #f1f5f9;
                            box-shadow:0 1px 2px rgba(0,0,0,0.04);">
                    <div style="font-size:12px;font-weight:700;color:#0f172a;">{row['ID']}</div>
                    <div style="font-size:11px;color:#64748b;margin:2px 0;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row['Cliente']}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px;">
                        <span style="font-size:11px;color:#374151;font-weight:500;">{val}</span>
                        <span style="font-size:11px;">{dot(row['Prioridade'])} {row['Prioridade']}</span>
                    </div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:3px;">👤 {row['Responsável']}</div>
                </div>
                """, unsafe_allow_html=True)

            if len(grupo) > 20:
                st.caption(f"+ {len(grupo)-20} pedidos")

    st.markdown('</div>', unsafe_allow_html=True)
