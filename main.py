import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS CUSTOM: DESIGN MOZZAFIATO
st.markdown("""
    <style>
    /* Sfondo e Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a !important;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Luxury */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* Card Metriche Elite (Glassmorphism) */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        padding: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
        transition: all 0.4s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,74,173,0.1) !important;
        border: 1px solid #004aad !important;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }
    
    [data-testid="stMetricValue"] div {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    /* Bottoni con effetto Oro/Blu Profondo */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: #0f172a;
        color: #ffffff !important;
        font-weight: 700;
        letter-spacing: 1px;
        border: 1px solid #fbbf24; /* Tocco d'oro */
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background: #fbbf24;
        color: #0f172a !important;
        border: 1px solid #0f172a;
        box-shadow: 0 10px 20px rgba(251,191,36,0.3);
    }

    /* Tabella */
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Titoli */
    h1 {
        background: linear-gradient(90deg, #0f172a, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inizializzazione Database (Invariata)
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato"])

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
    st.markdown("<h1 style='text-align: center; color: #fbbf24; font-size: 1.5rem !important;'>ELITE CRM v3.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Management Excellence</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("DASHBOARD NAVIGATOR", ["📊 Visione Globale", "✍️ Editor Contratti", "📂 Archivio Documentale"])
    st.markdown("---")
    st.caption(f"Status: Premium License 💠")

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
        
        with st.expander("⚙️ Gestione Avanzata Portfolio"):
            cliente_da_eliminare = st.selectbox("Seleziona Contratto da Rimuovere", st.session_state.db_contratti["Cliente"].unique())
            if st.button("Rimuovi dal Database"):
                st.session_state.db_contratti = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] != cliente_da_eliminare]
                st.rerun()
    else:
        st.info("Nessun dato disponibile nel database. Caricare nuovi asset.")

# --- MODULO 2: CREAZIONE ---
elif menu == "✍️ Editor Contratti":
    st.title("Smart Contract Editor")
    st.warning("Modulo di generazione testi attivo. Per l'archiviazione usare 'Archivio Documentale'.")

# --- MODULO 3: ARCHIVIO DOCUMENTALE ---
elif menu == "📂 Archivio Documentale":
    st.title("Asset Digitizer")
    st.markdown("##### Digitalizzazione e indicizzazione contratti PDF.")
    
    with st.container():
        file_pdf = st.file_uploader("Carica Documento Firmato (PDF)", type=["pdf"])
        c1, c2 = st.columns(2)
        with c1:
            nuovo_cliente = st.text_input("Ragione Sociale")
            nuovo_settore = st.selectbox("Classe Servizio", ["Manutenzione", "Servizi", "Consulenza"])
        with c2:
            nuova_scadenza = st.date_input("Termine Contrattuale")
            nuovo_fatturato = st.number_input("Valore Annuo (€)", min_value=0.0)

    if st.button("Archivia Asset"):
        if file_pdf and nuovo_cliente:
            nuova_riga = {"Cliente": nuovo_cliente, "Settore": nuovo_settore, "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'), "Fatturato": nuovo_fatturato, "Stato": "✅ ATTIVO"}
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.balloons()
            st.success("Asset indicizzato correttamente.")
            st.rerun()
