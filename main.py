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

# Inizializziamo il database in memoria se non esiste (per rendere la dashboard dinamica)
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=[
        "Cliente", "Settore", "Scadenza", "Fatturato", "Stato"
    ])

# 2. CSS CUSTOM (Invariato, con fix per testo nero)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    html, body, [class*="st-"], .stMarkdown, p, span, div { color: #000000 !important; }
    label p { color: #000000 !important; font-weight: 700 !important; font-size: 1.1rem !important; }
    h1, h2, h3, h4 { color: #1e293b !important; font-weight: 800 !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; }
    [data-testid="stMetricLabel"] p { color: #444444 !important; }
    [data-testid="stMetricValue"] div { color: #004aad !important; }
    [data-testid="stSidebar"] { background-color: #0e1117 !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; background: linear-gradient(90deg, #004aad 0%, #007bff 100%); color: #ffffff !important; font-weight: bold; border: none; }
    input { color: #000000 !important; background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Elite CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGAZIONE", ["📊 Dashboard", "✍️ Nuovo Contratto", "📂 Carica PDF Esterno"])
    st.markdown("---")
    st.caption("Utente: Amministratore")
    st.caption("Stato Sistema: Online 🟢")

# --- MODULO 1: DASHBOARD (Ora Dinamica) ---
if menu == "📊 Dashboard":
    st.title("Tableau de Bord 📈")
    st.markdown("##### Monitoraggio in tempo reale dei contratti aziendali.")
    
    # Calcolo metriche dinamiche
    totale_contratti = len(st.session_state.db_contratti)
    fatturato_totale = st.session_state.db_contratti["Fatturato"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Contratti Totali", f"{totale_contratti}")
    with col2:
        st.metric("Scadenze Critiche", "0", "⚠️ Alert")
    with col3:
        st.metric("Fatturato Annuo", f"€ {fatturato_totale:,.2f}")
    with col4:
        st.metric("Tasso Rinnovo", "100%", "Ottimo")

    st.markdown("---")
    st.subheader("📋 Contratti in Archivio")
    
    if totale_contratti > 0:
        st.dataframe(st.session_state.db_contratti, use_container_width=True)
    else:
        st.info("L'archivio è vuoto. Carica un PDF o genera un nuovo contratto.")

# --- MODULO 2: CREAZIONE (Invariato) ---
elif menu == "✍️ Nuovo Contratto":
    st.title("Smart Contract Creator ✨")
    # ... (Il codice precedente della creazione rimane qui, rimosso per brevità ma va mantenuto uguale)
    st.warning("Usa questa sezione per generare testi. Per popolare la Dashboard, usa la sezione 'Carica PDF'.")

# --- MODULO NUOVO: CARICAMENTO PDF ---
elif menu == "📂 Carica PDF Esterno":
    st.title("Archiviazione Contratto PDF 📂")
    st.markdown("##### Carica un file PDF e inserisci i dati per l'aggiornamento della Dashboard.")
    
    with st.container():
        # Uploader del file
        file_pdf = st.file_uploader("Trascina qui il contratto PDF", type=["pdf"])
        
        st.markdown("---")
        st.markdown("#### 📝 Inserimento Dati Tabella")
        
        c1, c2 = st.columns(2)
        with c1:
            nuovo_cliente = st.text_input("Ragione Sociale Cliente")
            nuovo_settore = st.selectbox("Settore", ["Manutenzione", "Servizi", "Consulenza"])
            nuova_scadenza = st.date_input("Data di Scadenza")
        with c2:
            nuovo_fatturato = st.number_input("Fatturato Annuo (€)", min_value=0.0, step=1000.0)
            nuovo_stato = st.selectbox("Stato Iniziale", ["✅ Attivo", "⏳ In Attesa", "⚠️ In Scadenza"])

    if st.button("🚀 SALVA E AGGIORNA GESTIONALE"):
        if not file_pdf:
            st.error("Devi caricare un file PDF per procedere.")
        elif not nuovo_cliente or nuovo_fatturato == 0:
            st.error("Inserisci il nome del cliente e il fatturato.")
        else:
            # Creazione riga dati
            nuova_riga = {
                "Cliente": nuovo_cliente,
                "Settore": nuovo_settore,
                "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'),
                "Fatturato": nuovo_fatturato,
                "Stato": nuovo_stato
            }
            
            # Aggiunta al database in sessione
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            
            st.balloons()
            st.success(f"Contratto di {nuovo_cliente} archiviato con successo! Dashboard aggiornata.")
