import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione stile "Professional"
st.set_page_config(page_title="Advanced Contract Management", layout="wide")

# --- CSS Personalizzato per sembrare un software serio ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Enterprise Contract Management")
st.markdown("---")

# Sidebar di Navigazione
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353039331e16a02ad.svg", width=50)
    menu = st.radio("Menu Gestionale", ["📊 Dashboard & Scadenze", "✍️ Nuovo Contratto (Smart)", "📈 Calcolo Adeguamento ISTAT"])

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Dashboard & Scadenze":
    st.subheader("Stato dei Contratti")
    col1, col2, col3 = st.columns(3)
    col1.metric("Contratti Attivi", "12", "+2 questo mese")
    col2.metric("Scadenze 30gg", "3", "-1")
    col3.metric("Volume Affari", "€ 45.200", "+5% ISTAT")
    
    # Esempio di tabella avanzata
    data = {
        "Cliente": ["Azienda Alfa", "Beta Service", "Gamma SRL"],
        "Settore": ["Manutenzione", "Servizi", "Manutenzione"],
        "Fine Contratto": ["2024-12-01", "2025-06-15", "2024-03-20"],
        "ISTAT": ["✅ Si", "❌ No", "✅ Si"],
        "Stato": ["Attivo", "Attivo", "⚠️ In Scadenza"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

# --- MODULO 2: SMART EDITOR ---
elif menu == "✍️ Nuovo Contratto (Smart)":
    st.subheader("Generatore Legale Assistito")
    
    with st.expander("1. Anagrafica Parti"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Ragione Sociale / Nome")
        piva = c2.text_input("P.IVA / CF")
    
    with st.expander("2. Dettagli Servizio"):
        settore = st.selectbox("Tipo di Contratto", ["Manutenzione Impianti", "Servizi Pulizia", "Consulenza IT"])
        canone = st.number_input("Canone Annuo (€)", min_value=0.0)
    
    with st.expander("3. Clausole Legali"):
        istat = st.checkbox("Inserisci clausola adeguamento ISTAT (Art. 32)")
        rinnovo = st.checkbox("Inserisci clausola Rinnovo Tacito")

    if st.button("Genera Bozza Contratto"):
        st.info("Bozza Generata con successo!")
        testo_legale = f"""
        **CONTRATTO DI {settore.upper()}**
        
        Tra **{nome}** (di seguito Committente) e **Nostra Azienda**...
        Il canone pattuito è di € {canone}. 
        { "L'importo sarà aggiornato annualmente secondo indici ISTAT." if istat else "" }
        { "Il contratto si intende rinnovato tacitamente alla scadenza." if rinnovo else "" }
        """
        st.markdown(testo_legale)
        st.download_button("Scarica Contratto (TXT)", testo_legale)
