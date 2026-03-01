import streamlit as st
import pandas as pd
from datetime import datetime, date
from style import apply_custom_style
from contract_logic import render_smart_editor
from billing_logic import render_billing_assistant

# 1. CONFIGURAZIONE DELLA PAGINA
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Applica lo stile personalizzato (font Georgia, bordi oro, ecc.)
apply_custom_style()

# 2. INIZIALIZZAZIONE DATABASE (SESSION STATE)
if 'db_contratti' not in st.session_state:
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato"])

# 3. FUNZIONE DI CALCOLO SCADENZE E STATO
def calcola_metriche_e_aggiorna_stato(df):
    if df.empty:
        return 0, 0, 100  # Alert, Fatturato, Health
    
    oggi = date.today()
    alert_count = 0
    fatturato_totale = df["Fatturato"].sum()
    
    for idx, row in df.iterrows():
        try:
            # Converte la stringa scadenza in oggetto data
            scadenza = datetime.strptime(row['Scadenza'], '%Y-%m-%d').date()
            giorni_rimanenti = (scadenza - oggi).days
            
            if giorni_rimanenti < 0:
                df.at[idx, 'Stato'] = "🚫 SCADUTO"
                alert_count += 1
            elif 0 <= giorni_rimanenti <= 30:
                df.at[idx, 'Stato'] = "⚠️ IN SCADENZA"
                alert_count += 1
            else:
                df.at[idx, 'Stato'] = "✅ ATTIVO"
        except:
            continue
            
    # Calcolo salute portfolio (percentuale contratti attivi)
    contratti_attivi = len(df[df['Stato'] == "✅ ATTIVO"])
    health_score = (contratti_attivi / len(df)) * 100 if len(df) > 0 else 100
    
    return alert_count, fatturato_totale, health_score

# --- SIDEBAR NAVIGAZIONE ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">ELITE v3.0</p>', unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("DASHBOARD NAVIGATOR", [
        "📊 Visione Globale", 
        "✍️ Editor Contratti", 
        "📂 Archivio Documentale", 
        "🧾 Fatturazione"
    ])
    st.markdown("---")
    st.caption(f"Status: Premium License 💠")

# --- NAVIGAZIONE PRINCIPALE ---

# SEZIONE 1: VISIONE GLOBALE (HOME PAGE RIPRISTINATA)
if menu == "📊 Visione Globale":
    st.title("EXECUTIVE DASHBOARD")
    st.markdown("##### Analisi patrimoniale e monitoraggio scadenze contrattuali")
    
    # Esegue i calcoli per le schede
    n_alerts, tot_fatturato, health = calcola_metriche_e_aggiorna_stato(st.session_state.db_contratti)
    n_contratti = len(st.session_state.db_contratti)

    # VISUALIZZAZIONE DELLE 4 SCHEDE (METRICHE)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Contratti In Essere", f"{n_contratti}")
    with col2:
        # Il colore rosso/arancione dell'alert è gestito automaticamente da Streamlit con delta se necessario
        st.metric("Critical Alerts", f"{n_alerts}", delta="- Scadenze" if n_alerts > 0 else None, delta_color="inverse")
    with col3:
        st.metric("Volume d'Affari", f"€ {tot_fatturato:,.2f}")
    with col4:
        st.metric("Portfolio Health", f"{health:.1f}%", delta="Status")

    st.markdown("---")
    
    # TABELLA DATABASE
    st.subheader("Database Contratti")
    if n_contratti > 0:
        # Visualizza la tabella con lo stile Georgia applicato
        st.dataframe(st.session_state.db_contratti, use_container_width=True)
        
        # Opzioni di gestione rapida
        with st.expander("⚙️ Azioni Rapide Database"):
            cliente_sel = st.selectbox("Seleziona Cliente per eliminazione:", st.session_state.db_contratti["Cliente"].unique())
            if st.button("Elimina Contratto Selezionato"):
                st.session_state.db_contratti = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] != cliente_sel]
                st.success(f"Contratto di {cliente_sel} rimosso.")
                st.rerun()
    else:
        st.info("Nessun contratto presente nel database. Vai in 'Archivio Documentale' per aggiungere il primo asset.")

# SEZIONE 2: EDITOR CONTRATTI
elif menu == "✍️ Editor Contratti":
    render_smart_editor()

# SEZIONE 3: ARCHIVIO DOCUMENTALE
elif menu == "📂 Archivio Documentale":
    st.title("Asset Digitizer")
    st.markdown("##### Caricamento e archiviazione nuovi contratti")
    
    # Box di caricamento (stile scuro impostato in style.py)
    file_pdf = st.file_uploader("Trascina qui il file PDF del contratto", type=["pdf"])
    
    st.markdown("### Dettagli Anagrafici")
    c1, c2 = st.columns(2)
    with c1:
        nuovo_cliente = st.text_input("Ragione Sociale Cliente")
        nuovo_settore = st.selectbox("Classe Servizio", ["Manutenzione", "Servizi", "Consulenza", "Appalto d'opera"])
    with c2:
        nuova_scadenza = st.date_input("Data di Scadenza Contratto")
        nuovo_fatturato = st.number_input("Valore Annuo Lordo (€)", min_value=0.0)

    if st.button("Archivia e Registra Asset"):
        if nuovo_cliente and nuova_scadenza:
            nuova_riga = {
                "Cliente": nuovo_cliente, 
                "Settore": nuovo_settore, 
                "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'), 
                "Fatturato": nuovo_fatturato, 
                "Stato": "IN ELABORAZIONE"
            }
            # Aggiunge al dataframe in session_state
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.success(f"Contratto di {nuovo_cliente} registrato con successo!")
            st.rerun()
        else:
            st.error("Per favore, inserisci almeno il nome cliente e la data di scadenza.")

# SEZIONE 4: FATTURAZIONE
elif menu == "🧾 Fatturazione":
    render_billing_assistant()
