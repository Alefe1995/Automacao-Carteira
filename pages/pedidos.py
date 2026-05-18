import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos, badge_status, cor_prioridade

def render():
    df = carregar_pedidos()

    st.markdown("""
    <div class="page-header">
        <h2>📦 Gestão de Pedidos</h2>
        <p>Monitore, filtre e gerencie todos os pedidos da operação</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filtros ───────────────────────────────────────────────────────────────
    with st.expander("🔎 Filtros", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            status_sel = st.multiselect("Status", df["Status"].unique(), default=list(df["Status"].unique()))
        with c2:
            prio_sel = st.multiselect("Prioridade", df["Prioridade"].unique(), default=list(df["Prioridade"].unique()))
        with c3:
            reg_sel = st.multiselect("Região", df["Região"].unique(), default=list(df["Região"].unique()))
        with c4:
            busca = st.text_input("🔍 Buscar por cliente ou ID")

    df_f = df[
        df["Status"].isin(status_sel) &
        df["Prioridade"].isin(prio_sel) &
        df["Região"].isin(reg_sel)
    ]
    if busca:
        df_f = df_f[
            df_f["Cliente"].str.contains(busca, case=False) |
            df_f["ID"].str.contains(busca, case=False)
        ]

    # ── KPIs rápidos ──────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pedidos filtrados", len(df_f))
    k2.metric("Volume (R$)", f"R$ {df_f['Valor (R$)'].sum():,.0f}".replace(",","."))
    k3.metric("Ticket médio", f"R$ {df_f['Valor (R$)'].mean():,.0f}".replace(",",".") if len(df_f) else "—")
    k4.metric("Alta prioridade", len(df_f[df_f["Prioridade"]=="Alta"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabela ────────────────────────────────────────────────────────────────
    df_show = df_f[["ID","Cliente","Categoria","Status","Prioridade","Valor (R$)","Responsável","Região","Data Criação","Previsão Entrega"]].copy()
    df_show["Prioridade"] = df_show["Prioridade"].apply(lambda p: f"{cor_prioridade(p)} {p}")
    df_show["Valor (R$)"] = df_show["Valor (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",","X").replace(".",",").replace("X","."))

    st.dataframe(
        df_show,
        use_container_width=True,
        hide_index=True,
        height=480,
        column_config={
            "ID": st.column_config.TextColumn("Pedido", width=90),
            "Cliente": st.column_config.TextColumn("Cliente", width=180),
            "Valor (R$)": st.column_config.TextColumn("Valor", width=130),
        }
    )

    # ── Export ────────────────────────────────────────────────────────────────
    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar CSV", csv, "pedidos_filtrados.csv", "text/csv")