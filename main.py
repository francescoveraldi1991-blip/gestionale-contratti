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

# 2. CSS CUSTOM PER LEGGIBILITÀ (TESTO NERO FORZATO) E EFFETTO WOW
st.markdown("""
    <style>
    /* Sfondo generale grigio chiarissimo */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* FORZA IL TESTO NERO IN TUTTA L'APP */
    html, body, [class*="st-"], .stMarkdown, p, span, div {
        color: #000000 !important;
    }

    /* Etichette dei campi di input (Label) in nero grassetto */
    label p {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Titoli principali */
    h1, h2, h3, h4 {
        color: #1e293b !important;
        font-weight: 800 !important;
    }
    
    /* Stilizzazione delle metriche (Card bianche con testo blu/nero) */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #444444 !important;
    }
    
    [data-testid="stMetricValue"] div {
        color: #004aad !important;
    }

    /* Sidebar - contrasto scuro con testo bianco per leggibilità */
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Pulsante principale con gradiente */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3.5em;
        background: linear-gradient(90deg, #004aad 0%, #007bff 100%);
        color: #ffffff !important;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 10px rgba(0,74,173,0.3);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0,74,173,0.5);
    }

    /* Input text color (nero per quello che scrivi) */
    input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Colore icone alert */
    .stAlert p {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Elite CRM</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGAZIONE", ["📊 Dashboard", "✍️ Nuovo Contratto"])
    st.markdown("---")
    st.caption("Utente: Amministratore")
    st.caption("Stato Sistema: Online 🟢")

# --- MODULO 1: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Tableau de Bord 📈")
    st.markdown("##### Monitoraggio in tempo reale dei contratti aziendali.")
    
    # Card con statistiche
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Contratti Totali", "24", "+12%")
    with col2:
        st.metric("Scadenze Critiche", "3", "⚠️ Alert")
    with col3:
        st.metric("Fatturato Annuo", "€ 128k", "+5k ISTAT")
    with col4:
        st.metric("Tasso Rinnovo", "95%", "Ottimo")

    st.markdown("---")
    st.subheader("📋 Contratti Recenti")
    
    # Tabella dati pulita
    data = {
        "Cliente": ["Azienda Tech SPA", "Global Service SRL", "Studio Legale Rossi", "Ristorante Da Mario"],
        "Settore": ["Manutenzione", "Servizi", "Consulenza", "Servizi"],
        "Scadenza": ["2026-05-12", "2026-01-20", "2027-11-02", "2026-08-15"],
        "Stato": ["✅ Attivo", "✅ Attivo", "✅ Attivo", "⏳ In Rinnovo"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

# --- MODULO 2: CREAZIONE ---
elif menu == "✍️ Nuovo Contratto":
    st.title("Smart Contract Creator ✨")
    st.markdown("##### Generatore di documenti legali pre-validati.")
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            settore = st.selectbox("Seleziona Tipo Servizio", ["Manutenzione Impianti", "Prestazione di Servizi"])
            cliente = st.text_input("Ragione Sociale Cliente", placeholder="Es. Rossi SRL")
        with c2:
            canone = st.number_input("Importo Annuo Pattuito (€)", min_value=0.0, step=100.0)
            fine = st.date_input("Data di Scadenza Contratto")

    st.markdown("---")
    
    # Sezione clausole con interruttori moderni
    st.markdown("#### ⚙️ Configurazione Clausole Speciali")
    col_a, col_b = st.columns(2)
    with col_a:
        istat = st.toggle("Abilita Adeguamento ISTAT annuale")
    with col_b:
        rinnovo = st.toggle("Abilita Rinnovo Automatico (Tacito)")

    st.markdown("---")

    if st.button("🚀 GENERA DOCUMENTO PROFESSIONALE"):
        if not cliente or canone == 0:
            st.error("⚠️ Attenzione: Inserisci il nome del cliente e un importo valido per procedere.")
        else:
            # Generazione del testo
            testo_contratto = f"""# CONTRATTO DI {settore.upper()}

Con la presente scrittura, tra la ditta fornitrice e il cliente **{cliente}**, si conviene quanto segue:

- **OGGETTO:** Esecuzione di servizi di {settore}.
- **CORRISPETTIVO:** L'importo è fissato in € {canone:,.2f} + IVA annui.
- **DURATA:** Il contratto scadrà il giorno {fine.strftime('%d/%m/%Y')}.
"""
            if istat:
                testo_contratto += "\n- **ADEGUAMENTO ISTAT:** Il canone sarà aggiornato annualmente secondo l'indice FOI."
            if rinnovo:
                testo_contratto += "\n- **RINNOVO:** Il contratto si intende rinnovato tacitamente per lo stesso periodo in assenza di disdetta."
            
            st.balloons()
            st.success("Documento generato correttamente!")
            
            st.markdown("### 📄 Anteprima Documento")
            st.code(testo_contratto, language="markdown")
            
            st.download_button(
                label="📥 SCARICA ORA (FORMATO .MD)",
                data=testo_contratto,
                file_name=f"Contratto_{cliente.replace(' ', '_')}.md",
                mime="text/markdown"
            )
