import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione della pagina stile Enterprise
st.set_page_config(page_title="Advanced Contract Management", layout="wide")

# --- CSS per un look professionale ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stAlert { border-radius: 10px; }
    .stButton>button { background-color: #004aad; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Enterprise Contract Management")
st.markdown("---")

# --- SIDEBAR NAVIGAZIONE ---
with st.sidebar:
    st.header("Menu Gestionale")
    menu = st.radio("Seleziona Area", ["📊 Dashboard & Scadenze", "✍️ Nuovo Contratto (Smart)"])
    st.markdown("---")
    st.info("Versione 2.0 - Modulo Legale Attivo")

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Dashboard & Scadenze":
    st.subheader("Stato Generale Contratti")
    c1, c2, c3 = st.columns(3)
    c1.metric("Contratti Attivi", "5", "+1")
    c2.metric("Scadenze < 30gg", "2", "⚠️")
    c3.metric("Indice ISTAT Medio", "2.1%", "FOI")

    # Dati di esempio per la tabella
    data = {
        "Cliente": ["Rossi SRL", "Azienda Bianchi", "Verdi Manutenzioni"],
        "Tipo": ["Servizi", "Manutenzione", "Manutenzione"],
        "Scadenza": ["2024-12-31", "2025-06-30", "2024-03-15"],
        "Stato": ["Attivo", "Attivo", "In Scadenza"]
    }
    st.table(pd.DataFrame(data))

# --- MODULO 2: SMART EDITOR (CON SCHELETRI LEGALI) ---
elif menu == "✍️ Nuovo Contratto (Smart)":
    st.subheader("Generatore Assistito di Contratti")
    
    # --- CHECK LEGALE (Progress Bar) ---
    st.markdown("#### Verifica Completezza Documento")
    campi_compilati = 0
    
    col_a, col_b = st.columns(2)
    with col_a:
        settore = st.selectbox("Ambito del Contratto", ["Manutenzione Impianti", "Prestazione di Servizi"])
        cliente = st.text_input("Ragione Sociale Cliente")
        if cliente: campi_compilati += 1
        piva = st.text_input("Partita IVA / C.F.")
        if piva: campi_compilati += 1
    
    with col_b:
        canone = st.number_input("Canone Annuo (€)", min_value=0.0)
        if canone > 0: campi_compilati += 1
        inizio = st.date_input("Data Inizio", datetime.now())
        fine = st.date_input("Data Fine")
        if fine > inizio: campi_compilati += 1

    # Calcolo percentuale progresso (4 campi base)
    progresso = campi_compilati / 4
    st.progress(progresso)
    if progresso < 1.0:
        st.warning("Completa tutti i dati sopra per abilitare la generazione professionale.")
    else:
        st.success("Check Legale Superato: Documento pronto per la generazione.")

    st.markdown("---")
    st.markdown("#### Opzioni Clausole Speciali")
    c_istat = st.checkbox("Inserisci Adeguamento ISTAT (Indice FOI)")
    c_rinnovo = st.checkbox("Inserisci Rinnovo Tacito (60 gg)")

    if st.button("Genera Bozza e Scarica"):
        # COSTRUZIONE DELLO SCHELETRO IN BASE AL SETTORE
        if settore == "Manutenzione Impianti":
            testo_contratto = f"""
# CONTRATTO DI MANUTENZIONE TECNICA
**TRA:** Nostra Azienda (Fornitore) e **{cliente}** (Committente, P.IVA: {piva})

**Art. 1 (Oggetto):** Il Fornitore si impegna alla manutenzione ordinaria degli impianti del Committente per garantire efficienza e sicurezza.
