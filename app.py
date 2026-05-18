import streamlit as st

st.set_page_config(
    page_title="LogiSync Flow",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilo global ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid #1e2d4a;
}
section[data-testid="stSidebar"] * { color: #c9d6f0 !important; }
section[data-testid="stSidebar"] .stRadio label { 
    padding: 8px 12px; border-radius: 8px; cursor:pointer;
    transition: background .2s;
}
section[data-testid="stSidebar"] .stRadio label:hover { background:#1e2d4a; }

/* Main bg */
.main { background: #f0f4ff; }
.block-container { padding-top: 1.5rem !important; }

/* Cards de KPI */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(10,15,30,0.08);
    border-left: 4px solid;
    margin-bottom: 4px;
}
.kpi-label { font-size:12px; font-weight:500; color:#6b7a9d; text-transform:uppercase; letter-spacing:1px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:28px; font-weight:700; color:#0a0f1e; margin:4px 0; }
.kpi-delta { font-size:12px; color:#22c55e; font-weight:500; }

/* Badge de status */
.badge {
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:11px; font-weight:600; letter-spacing:.5px;
}
.badge-pendente   { background:#fef3c7; color:#b45309; }
.badge-processamento { background:#dbeafe; color:#1d4ed8; }
.badge-transito   { background:#e0f2fe; color:#0369a1; }
.badge-entregue   { background:#dcfce7; color:#15803d; }
.badge-cancelado  { background:#fee2e2; color:#b91c1c; }

/* Header da página */
.page-header {
    background: linear-gradient(135deg, #0a0f1e 0%, #1a2744 100%);
    border-radius: 16px; padding: 24px 32px; margin-bottom: 24px;
    color: white;
}
.page-header h2 { color:white !important; margin:0; font-size:22px; }
.page-header p  { color:#8ca3d4; margin:4px 0 0; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚚 LogiSync Flow")
    st.markdown("---")
    pagina = st.radio(
        "Navegação",
        ["🏠 Dashboard", "📦 Pedidos", "🔄 Pipeline", "✅ Tarefas",
         "⭐ Clientes Estratégicos", "🔍 Auditoria"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<small style='color:#4a5a7a'>v1.0.0 • Dados via Excel</small>", unsafe_allow_html=True)

# ── Roteamento ─────────────────────────────────────────────────────────────────
if pagina == "🏠 Dashboard":
    from pages import dashboard; dashboard.render()
elif pagina == "📦 Pedidos":
    from pages import pedidos; pedidos.render()
elif pagina == "🔄 Pipeline":
    from pages import pipeline; pipeline.render()
elif pagina == "✅ Tarefas":
    from pages import tarefas; tarefas.render()
elif pagina == "⭐ Clientes Estratégicos":
    from pages import clientes; clientes.render()
elif pagina == "🔍 Auditoria":
    from pages import auditoria; auditoria.render()