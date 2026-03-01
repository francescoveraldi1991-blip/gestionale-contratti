import streamlit as st
import pandas as pd
from datetime import datetime, date
from style import apply_custom_style
from contract_logic import render_smart_editor # <--- CARICHIAMO IL NUOVO MODULO

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Applicazione dello stile
apply_custom_style()

# 3. Inizializzazione Database
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato"])

# 4. Funzioni di calcolo
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">ELITE v3.0</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Management Excellence</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("DASHBOARD NAVIGATOR", ["📊 Visione Globale", "✍️ Editor Contratti", "📂 Archivio Documentale"])
    st.markdown("---")
    st.caption(f"Status: Premium License 💠")

# --- NAVIGAZIONE ---
if menu == "📊 Visione Globale":
    st.title("Executive Dashboard")
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
        with st.expander("⚙️ Gestione Avanzata"):
            cliente_da_eliminare = st.selectbox("Rimuovi", st.session_state.db_contratti["Cliente"].unique())
            if st.button("Elimina"):
                st.session_state.db_contratti = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] != cliente_da_eliminare]
                st.rerun()
    else:
        st.info("Caricare dati in Archivio.")

elif menu == "✍️ Editor Contratti":
    render_smart_editor() # <--- CHIAMIAMO LA FUNZIONE DAL FILE ESTERNO

elif menu == "📂 Archivio Documentale":
    st.title("Asset Digitizer")
    file_pdf = st.file_uploader("Carica PDF", type=["pdf"])
    c1, c2 = st.columns(2)
    with c1:
        nuovo_cliente = st.text_input("Cliente")
        nuovo_settore = st.selectbox("Classe Servizio", ["Manutenzione", "Servizi", "Consulenza"])
    with c2:
        nuova_scadenza = st.date_input("Scadenza")
        nuovo_fatturato = st.number_input("Valore (€)", min_value=0.0)

    if st.button("Archivia Asset"):
        if file_pdf and nuovo_cliente:
            nuova_riga = {"Cliente": nuovo_cliente, "Settore": nuovo_settore, "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'), "Fatturato": nuovo_fatturato, "Stato": "✅ ATTIVO"}
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.success("Archiviato!")
            st.rerun()
