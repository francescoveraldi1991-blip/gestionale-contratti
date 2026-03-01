import streamlit as st
import pandas as pd
from datetime import datetime, date
from style import apply_custom_style
from contract_logic import render_smart_editor
from billing_logic import render_billing_assistant # <--- NUOVA IMPORTAZIONE

# 1. Configurazione della pagina (Invariata)
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_style()

if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato"])

# --- SIDEBAR (AGGIORNATA) ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">ELITE v3.0</p>', unsafe_allow_html=True)
    st.markdown("---")
    # Aggiunta voce "Fatturazione"
    menu = st.radio("DASHBOARD NAVIGATOR", ["📊 Visione Globale", "✍️ Editor Contratti", "📂 Archivio Documentale", "🧾 Fatturazione"])
    st.markdown("---")
    st.caption(f"Status: Premium License 💠")

# --- NAVIGAZIONE ---
if menu == "📊 Visione Globale":
    # ... (Codice esistente per la Dashboard - Invariato)
    st.title("Executive Dashboard")
    # (Tieni tutto il tuo codice originale qui)
    st.info("Benvenuto nella visione globale del tuo portfolio.")

elif menu == "✍️ Editor Contratti":
    render_smart_editor()

elif menu == "📂 Archivio Documentale":
    # ... (Codice esistente per l'Archivio - Invariato)
    st.title("Asset Digitizer")

elif menu == "🧾 Fatturazione": # <--- NUOVA SEZIONE
    render_billing_assistant()
