import streamlit as st

st.set_page_config(
    page_title="LogiSync Flow",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Sidebar escura ── */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b !important;
    width: 220px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio > div {
    display: flex; flex-direction: column; gap: 2px;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex !important; align-items: center;
    padding: 8px 16px !important; border-radius: 8px !important;
    cursor: pointer; transition: all .15s;
    font-size: 13px !important; font-weight: 400 !important;
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #1e293b !important; color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[aria-checked="true"] {
    background: #1e293b !important; color: #f1f5f9 !important; font-weight: 500 !important;
}

/* ── Fundo principal branco ── */
.main .block-container {
    padding: 0 !important; max-width: 100% !important;
    background: #f8fafc;
}
.main { background: #f8fafc !important; }

/* ── Header de página ── */
.page-header {
    background: #0f172a;
    padding: 22px 32px 18px;
    margin-bottom: 24px;
}
.page-header h2 {
    color: #f1f5f9 !important; font-size: 20px !important;
    font-weight: 600 !important; margin: 0 0 4px !important;
}
.page-header p { color: #64748b !important; font-size: 13px !important; margin: 0 !important; }

/* ── KPI simples (sem card colorido) ── */
.kpi-wrap { padding: 20px 32px; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; }
.kpi-item {
    padding: 8px 24px 8px 0;
    border-right: 1px solid #e2e8f0;
}
.kpi-item:last-child { border-right: none; padding-right: 0; padding-left: 24px; }
.kpi-item:first-child { padding-left: 0; }
.kpi-label { font-size: 12px; color: #64748b; font-weight: 400; text-transform: uppercase; letter-spacing: .6px; margin-bottom: 4px; }
.kpi-value { font-size: 32px; font-weight: 700; color: #0f172a; line-height: 1.1; }
.kpi-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }

/* ── Seção de conteúdo ── */
.content-wrap { padding: 0 32px 32px; }

/* ── Tabela limpa ── */
.stDataFrame { border: none !important; }
.stDataFrame table { font-size: 13px !important; }
thead tr th {
    background: #f1f5f9 !important; color: #64748b !important;
    font-size: 11px !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: .5px !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
tbody tr:hover td { background: #f8fafc !important; }

/* ── Badges de status ── */
.badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 11px; font-weight: 500;
}
.badge-pendente        { background:#fef9c3; color:#854d0e; }
.badge-processamento   { background:#dbeafe; color:#1e40af; }
.badge-transito        { background:#e0f2fe; color:#0369a1; }
.badge-entregue        { background:#dcfce7; color:#166534; }
.badge-cancelado       { background:#fee2e2; color:#991b1b; }
.badge-afazer          { background:#f1f5f9; color:#475569; }
.badge-emandamento     { background:#dbeafe; color:#1e40af; }
.badge-concluida       { background:#dcfce7; color:#166534; }
.badge-bloqueada       { background:#fee2e2; color:#991b1b; }

/* ── Ponto de prioridade ── */
.dot-alta   { color: #ef4444; font-size: 16px; }
.dot-media  { color: #f59e0b; font-size: 16px; }
.dot-baixa  { color: #22c55e; font-size: 16px; }

/* ── Filtros ── */
.stMultiSelect [data-baseweb="tag"] {
    background: #e2e8f0 !important; border-radius: 4px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: #334155 !important; font-size: 12px !important; }

/* ── Kanban ── */
.kanban-col {
    background: #f8fafc; border-radius: 10px;
    border: 1px solid #e2e8f0; padding: 0;
    min-height: 200px;
}
.kanban-header {
    padding: 12px 14px; border-radius: 10px 10px 0 0;
    display: flex; justify-content: space-between; align-items: center;
}
.kanban-count {
    font-size: 11px; font-weight: 700; padding: 2px 8px;
    border-radius: 20px; color: white;
}
.kanban-card {
    background: white; border-radius: 8px; padding: 12px 14px;
    margin: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid #f1f5f9;
}
.kanban-card-id { font-size: 12px; font-weight: 700; color: #0f172a; }
.kanban-card-cli { font-size: 11px; color: #64748b; margin: 2px 0; }
.kanban-card-val { font-size: 12px; color: #374151; font-weight: 500; }

/* Remove streamlit default padding */
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
div[data-testid="stVerticalBlock"] > div { padding-top: 0 !important; }
.stPlotlyChart { padding: 0 !important; }

/* Gráficos sem borda */
.js-plotly-plot { border: none !important; }

/* Esconde header padrão streamlit */
header[data-testid="stHeader"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 16px; border-bottom:1px solid #1e293b; margin-bottom:12px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:22px;">🚚</span>
            <span style="color:#f1f5f9;font-size:15px;font-weight:600;">LogiSync Flow</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio("", [
        "🔵  Dashboard",
        "🔴  Pedidos",
        "🔵  Pipeline",
        "🟢  Tarefas",
        "⭐  Clientes Estratégicos",
        "⚫  Auditoria",
    ])

    st.markdown("""
    <div style="position:absolute;bottom:20px;left:16px;right:16px;">
        <span style="color:#334155;font-size:11px;">v1.0.0 • Dados via Excel</span>
    </div>
    """, unsafe_allow_html=True)

# ── Roteamento ──
p = pagina.split("  ")[1] if "  " in pagina else pagina

if "Dashboard" in p:
    from pages import dashboard; dashboard.render()
elif "Pedidos" in p:
    from pages import pedidos; pedidos.render()
elif "Pipeline" in p:
    from pages import pipeline; pipeline.render()
elif "Tarefas" in p:
    from pages import tarefas; tarefas.render()
elif "Clientes" in p:
    from pages import clientes; clientes.render()
elif "Auditoria" in p:
    from pages import auditoria; auditoria.render()
