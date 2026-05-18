import pandas as pd
import streamlit as st
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "logisync_dados.xlsx")

@st.cache_data(ttl=300)
def carregar_pedidos():
    return pd.read_excel(EXCEL_PATH, sheet_name="Pedidos")

@st.cache_data(ttl=300)
def carregar_tarefas():
    return pd.read_excel(EXCEL_PATH, sheet_name="Tarefas")

@st.cache_data(ttl=300)
def carregar_clientes():
    return pd.read_excel(EXCEL_PATH, sheet_name="Clientes Estratégicos")

@st.cache_data(ttl=300)
def carregar_auditoria():
    return pd.read_excel(EXCEL_PATH, sheet_name="Auditoria")

def badge_status(status):
    mapa = {
        "Pendente": "badge-pendente",
        "Em Processamento": "badge-processamento",
        "Em Trânsito": "badge-transito",
        "Entregue": "badge-entregue",
        "Cancelado": "badge-cancelado",
    }
    css = mapa.get(status, "badge-pendente")
    return f'<span class="badge {css}">{status}</span>'

def cor_prioridade(p):
    return {"Alta": "🔴", "Média": "🟡", "Baixa": "🟢"}.get(p, "⚪")