import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import carregar_pedidos

def dot(p):
    c = {"Alta":"#ef4444","Média":"#f59e0b","Baixa":"#22c55e"}.get(p,"#94a3b8")
    return f'<span style="color:{c};font-size:14px;">●</span> {p}'

def render():
    df = carregar_pedidos()

    st.markdown("""
    <div class="page-header">
        <h2>📦 Gestão de Pedidos</h2>
        <p>Monitore, filtre e gerencie todos os pedidos da operação</p>
    </div>""", unsafe_allow_html=True)

    # ── Filtros ──
    with st.expander("🔎 Filtros", expanded=True):
        c1, c2, c3, c4 = st.columns([2,2,2,3])
        with c1:
            status_sel = st.multiselect("Status", df["Status"].unique(),
                default=list(df["Status"].unique()), key="ped_status")
        with c2:
            prio_sel = st.multiselect("Prioridade", df["Prioridade"].unique(),
                default=list(df["Prioridade"].unique()), key="ped_prio")
        with c3:
            reg_sel = st.multiselect("Região", df["Região"].unique(),
                default=list(df["Região"].unique()), key="ped_reg")
        with c4:
            busca = st.text_input("🔍 Buscar por cliente ou ID", key="ped_busca")

    df_f = df[df["Status"].isin(status_sel) &
              df["Prioridade"].isin(prio_sel) &
              df["Região"].isin(reg_sel)]
    if busca:
        df_f = df_f[df_f["Cliente"].str.contains(busca, case=False) |
                    df_f["ID"].str.contains(busca, case=False)]

    # ── KPIs ──
    total_f = len(df_f)
    vol_f   = df_f["Valor (R$)"].sum()
    tick_f  = vol_f/total_f if total_f else 0
    alta_f  = len(df_f[df_f["Prioridade"]=="Alta"])

    st.markdown(f"""
    <div class="kpi-wrap" style="padding-top:8px;padding-bottom:8px;">
      <div class="kpi-grid">
        <div class="kpi-item">
          <div class="kpi-label">Pedidos filtrados</div>
          <div class="kpi-value">{total_f}</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Volume (R$)</div>
          <div class="kpi-value">R$ {vol_f:,.0f}".replace(",",".")</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Ticket médio</div>
          <div class="kpi-value">R$ {tick_f:,.0f}".replace(",",".")</div>
        </div>
        <div class="kpi-item" style="padding-left:24px;">
          <div class="kpi-label">Alta prioridade</div>
          <div class="kpi-value">{alta_f}</div>
        </div>
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin:0 32px 16px;">
    """, unsafe_allow_html=True)

    # ── Tabela ──
    with st.container():
        st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

        df_show = df_f[["ID","Cliente","Categoria","Status","Prioridade",
                         "Valor (R$)","Responsável","Região",
                         "Data Criação","Previsão Entrega"]].copy()

        df_show["Valor (R$)"] = df_show["Valor (R$)"].apply(
            lambda x: f"R$ {x:,.2f}".replace(",","X").replace(".",",").replace("X",".")
        )

        st.dataframe(
            df_show, use_container_width=True, hide_index=True, height=500,
            column_config={
                "ID":       st.column_config.TextColumn("Pedido", width=90),
                "Cliente":  st.column_config.TextColumn("Cliente", width=180),
                "Status":   st.column_config.TextColumn("Status", width=140),
                "Prioridade": st.column_config.TextColumn("Prioridade", width=90),
                "Valor (R$)": st.column_config.TextColumn("Valor", width=130),
            }
        )

        csv = df_f.to_csv(index=False).encode("utf-8")
        st.download_button("☁️ Exportar CSV", csv, "pedidos.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)
