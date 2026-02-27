import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Pro Contract Manager Elite",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inizializziamo il database in memoria
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=[
        "Cliente", "Settore", "Scadenza", "Fatturato", "Stato"
    ])

# 2. CSS CUSTOM (Invariato)
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

# --- FUNZIONE DI CONTROLLO SCADENZE ---
def calcola_scadenze_critiche(df):
    if df.empty:
        return 0
    oggi = date.today()
    critiche = 0
    for idx, row in df.iterrows():
        scadenza = datetime.strptime(row['Scadenza'], '%Y-%m-%d').date()
        # Se mancano meno di 30 giorni alla scadenza
        giorni_rimanenti = (scadenza - oggi).days
        if 0 <= giorni_rimanenti <= 30:
            critiche += 1
            df.at[idx, 'Stato'] = "⚠️ IN SCADENZA"
        elif giorni_rimanenti < 0:
            df.at[idx, 'Stato'] = "🚫 SCADUTO"
    return critiche

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Elite CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGAZIONE", ["📊 Dashboard", "✍️ Nuovo Contratto", "📂 Carica PDF Esterno"])
    st.markdown("---")
    st.caption(f"Data Oggi: {date.today().strftime('%d/%m/%Y')}")

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Tableau de Bord 📈")
    
    # Aggiorniamo gli stati e calcoliamo le criticità
    n_critiche = calcola_scadenze_critiche(st.session_state.db_contratti)
    
    totale_contratti = len(st.session_state.db_contratti)
    fatturato_totale = st.session_state.db_contratti["Fatturato"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Contratti Totali", f"{totale_contratti}")
    with col2:
        # La scheda ora si aggiorna dinamicamente
        st.metric("Scadenze Critiche", f"{n_critiche}", delta="Alert" if n_critiche > 0 else None, delta_color="inverse")
    with col3:
        st.metric("Fatturato Annuo", f"€ {fatturato_totale:,.2f}")
    with col4:
        st.metric("Tasso Rinnovo", "100%", "Ottimo")

    st.markdown("---")
    st.subheader("📋 Contratti in Archivio")
    
    if totale_contratti > 0:
        # Mostriamo la tabella con gli stati aggiornati (⚠️ IN SCADENZA o 🚫 SCADUTO)
        st.dataframe(st.session_state.db_contratti, use_container_width=True)
    else:
        st.info("L'archivio è vuoto. Carica un PDF per iniziare.")

# --- MODULO 2: CREAZIONE (Invariato) ---
elif menu == "✍️ Nuovo Contratto":
    st.title("Smart Contract Creator ✨")
    st.warning("Usa la sezione 'Carica PDF' per popolare la Dashboard.")

# --- MODULO 3: CARICAMENTO PDF (Aggiornato per salvare la data corretta) ---
elif menu == "📂 Carica PDF Esterno":
    st.title("Archiviazione Contratto PDF 📂")
    
    file_pdf = st.file_uploader("Trascina qui il contratto PDF", type=["pdf"])
    
    c1, c2 = st.columns(2)
    with c1:
        nuovo_cliente = st.text_input("Ragione Sociale Cliente")
        nuovo_settore = st.selectbox("Settore", ["Manutenzione", "Servizi", "Consulenza"])
    with c2:
        nuova_scadenza = st.date_input("Data di Scadenza")
        nuovo_fatturato = st.number_input("Fatturato Annuo (€)", min_value=0.0)

    if st.button("🚀 SALVA E AGGIORNA GESTIONALE"):
        if not file_pdf or not nuovo_cliente:
            st.error("Carica il file e inserisci il nome cliente.")
        else:
            nuova_riga = {
                "Cliente": nuovo_cliente,
                "Settore": nuovo_settore,
                "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'),
                "Fatturato": nuovo_fatturato,
                "Stato": "✅ Attivo" # Lo stato iniziale è attivo, verrà ricontrollato dalla Dashboard
            }
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.success("Contratto archiviato!")
