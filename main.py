import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Pro Contract Manager Elite",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS CUSTOM PER L'EFFETTO WOW
st.markdown("""
    <style>
    /* Sfondo e font generale */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Stilizzazione delle metriche (Card) */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #004aad;
    }
    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Sidebar elegante */
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        color: white;
    }

    /* Pulsante principale */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background: linear-gradient(90deg, #004aad 0%, #007bff 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,74,173,0.4);
    }

    /* Titoli */
    h1 {
        color: #1e293b;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>Elite CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGAZIONE", ["📊 Dashboard", "✍️ Nuovo Contratto"])
    st.markdown("---")
    st.caption("Utente: Amministratore")
    st.caption("Stato Sistema: Online 🟢")

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Tableau de Bord 📈")
    st.markdown("Monitoraggio in tempo reale dei contratti aziendali.")
    
    # Card con statistiche
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Contratti", "24", "+12%")
    with col2:
        st.metric("Scadenze", "3", "⚠️ Alert")
    with col3:
        st.metric("Fatturato", "€ 128k", "+5k ISTAT")
    with col4:
        st.metric("Rinnovi", "95%", "Ottimo")

    st.markdown("---")
    st.subheader("📋 Contratti Recenti")
    
    # Tabella con stile
    data = {
        "Cliente": ["Azienda Tech SPA", "Global Service SRL", "Studio Legale Rossi"],
        "Settore": ["Manutenzione", "Servizi", "Consulenza"],
        "Scadenza": ["2026-05-12", "2026-01-20", "2027-11-02"],
        "Rating": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    }
    st.table(pd.DataFrame(data))

# --- MODULO 2: CREAZIONE ---
elif menu == "✍️ Nuovo Contratto":
    st.title("Smart Contract Creator ✨")
    st.info("Compila i campi per generare un documento legale pre-validato.")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            settore = st.selectbox("Tipo Servizio", ["Manutenzione Impianti", "Prestazione di Servizi"])
            cliente = st.text_input("Ragione Sociale")
        with c2:
            canone = st.number_input("Importo Annuo (€)", min_value=0.0)
            fine = st.date_input("Scadenza")

    st.markdown("---")
    
    # Sezione clausole con icone
    st.markdown("#### ⚙️ Configurazione Avanzata")
    col_a, col_b = st.columns(2)
    istat = col_a.toggle("Attiva Adeguamento ISTAT")
    rinnovo = col_b.toggle("Attiva Rinnovo Automatico")

    if st.button("GENERA DOCUMENTO"):
        if not cliente or canone == 0:
            st.error("Dati mancanti! Inserisci cliente e importo.")
        else:
            testo = f"# CONTRATTO DI {settore.upper()}\n\nTra la scrivente e **{cliente}**.\nImporto: € {canone:,.2f}.\nScadenza: {fine}."
            if istat: testo += "\n- Clausola ISTAT: ATTIVA"
            if rinnovo: testo += "\n- Rinnovo Automatico: ATTIVO"
            
            st.balloons() # Effetto festa!
            st.markdown("### 📄 Anteprima")
            st.code(testo, language="markdown")
            st.download_button("📥 SCARICA ORA", testo, file_name=f"{cliente}.md")
