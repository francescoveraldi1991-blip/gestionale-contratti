import streamlit as st
import pandas as pd
from datetime import datetime, date
from style import apply_custom_style

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Applicazione dello stile dal file style.py
apply_custom_style()

# 3. Inizializzazione Database in sessione
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato"])

# 4. Logica calcolo scadenze
def calcola_scadenze_critiche(df):
    if df.empty: return 0
    oggi = date.today()
    critiche = 0
    for idx, row in df.iterrows():
        scadenza = datetime.strptime(row['Scadenza'], '%Y-%m-%d').date()
        giorni_rimanenti = (scadenza - oggi).days
        if 0 <= giorni_rimanenti <= 30:
            critiche += 1
            df.at[idx, 'Stato'] = "⚠️ IN SCADENZA"
        elif giorni_rimanenti < 0:
            df.at[idx, 'Stato'] = "🚫 SCADUTO"
        else:
            df.at[idx, 'Stato'] = "✅ ATTIVO"
    return critiche

# --- SIDEBAR ELITE ---
with st.sidebar:
    # Titolo in Georgia Bianco (gestito tramite classe CSS in style.py)
    st.markdown('<p class="sidebar-title">ELITE v3.0</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Management Excellence</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("DASHBOARD NAVIGATOR", ["📊 Visione Globale", "✍️ Editor Contratti", "📂 Archivio Documentale"])
    st.markdown("---")
    st.caption(f"Status: Premium License 💠")
    st.caption(f"Data Odierna: {date.today().strftime('%d/%m/%Y')}")

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Visione Globale":
    st.title("Executive Dashboard")
    st.markdown("##### Analisi patrimoniale e monitoraggio scadenze contrattuali.")
    
    n_critiche = calcola_scadenze_critiche(st.session_state.db_contratti)
    totale_contratti = len(st.session_state.db_contratti)
    fatturato_totale = st.session_state.db_contratti["Fatturato"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Contratti In Essere", f"{totale_contratti}")
    with col2: st.metric("Critical Alerts", f"{n_critiche}")
    with col3: st.metric("Volume d'Affari", f"€ {fatturato_totale:,.2f}")
    with col4: st.metric("Portfolio Health", "100%", "Excellent")

    st.markdown("---")
    st.subheader("📑 Database Contratti")
    
    if totale_contratti > 0:
        st.dataframe(st.session_state.db_contratti, use_container_width=True)
        
        # Area cancellazione pulita
        with st.expander("⚙️ Gestione Avanzata Portfolio"):
            st.write("Seleziona un contratto per rimuoverlo definitivamente dall'archivio.")
            cliente_da_eliminare = st.selectbox("Contratto da Rimuovere", st.session_state.db_contratti["Cliente"].unique())
            if st.button("Rimuovi dal Database"):
                st.session_state.db_contratti = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] != cliente_da_eliminare]
                st.success("Database aggiornato.")
                st.rerun()
    else:
        st.info("Nessun dato disponibile nel database. Caricare nuovi asset tramite la sezione Archivio.")

# --- MODULO 2: EDITOR (Testuale) ---
elif menu == "✍️ Editor Contratti":
    st.title("Smart Contract Editor")
    st.markdown("##### Generazione di bozze contrattuali secondo standard legali.")
    st.info("Modulo di generazione testi attivo. Per popolare la dashboard, carica i dati in 'Archivio Documentale'.")

# --- MODULO 3: ARCHIVIO (Caricamento PDF) ---
elif menu == "📂 Archivio Documentale":
    st.title("Asset Digitizer")
    st.markdown("##### Digitalizzazione e indicizzazione contratti PDF.")
    
    with st.container():
        file_pdf = st.file_uploader("Carica Documento Firmato (PDF)", type=["pdf"])
        
        c1, c2 = st.columns(2)
        with c1:
            nuovo_cliente = st.text_input("Ragione Sociale Cliente")
            nuovo_settore = st.selectbox("Classe Servizio", ["Manutenzione", "Servizi", "Consulenza"])
        with c2:
            nuova_scadenza = st.date_input("Termine Contrattuale", date.today())
            nuovo_fatturato = st.number_input("Valore Annuo (€)", min_value=0.0, step=1000.0)

    if st.button("Archivia Asset"):
        if file_pdf and nuovo_cliente and nuovo_fatturato > 0:
            nuova_riga = {
                "Cliente": nuovo_cliente, 
                "Settore": nuovo_settore, 
                "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'), 
                "Fatturato": nuovo_fatturato, 
                "Stato": "✅ ATTIVO"
            }
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.balloons()
            st.success(f"Asset per {nuovo_cliente} indicizzato correttamente.")
            st.rerun()
        else:
            st.error("Verifica di aver caricato il PDF e inserito Cliente e Valore Annuo.")
