import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from style import apply_custom_style
from contract_logic import render_smart_editor
from billing_logic import render_billing_assistant
from email_logic import send_expiry_email

# 1. CONFIGURAZIONE DELLA PAGINA
st.set_page_config(
    page_title="Elite Contract Management | Luxury Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_style()

# --- CREAZIONE CARTELLA CLOUD LOCALE ---
UPLOAD_DIR = "stored_contracts"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 2. INIZIALIZZAZIONE DATABASE
if 'db_contratti' not in st.session_state:
    # Aggiunta colonna 'File_Path' per il recupero cloud
    st.session_state.db_contratti = pd.DataFrame(columns=["Cliente", "Settore", "Scadenza", "Fatturato", "Stato", "File_Path"])

# 3. FUNZIONE DI CALCOLO (Invariata)
def calcola_metriche_e_aggiorna_stato(df):
    if df.empty: return 0, 0, 100
    oggi = date.today()
    alert_count = 0
    fatturato_totale = df["Fatturato"].sum()
    for idx, row in df.iterrows():
        try:
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
        except: continue
    health_score = (len(df[df['Stato'] == "✅ ATTIVO"]) / len(df)) * 100 if len(df) > 0 else 100
    return alert_count, fatturato_totale, health_score

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">ELITE v3.0</p>', unsafe_allow_html=True)
    menu = st.radio("DASHBOARD NAVIGATOR", ["📊 Visione Globale", "✍️ Editor Contratti", "📂 Archivio Documentale", "🧾 Fatturazione"])
    st.caption(f"Status: Premium License 💠")

# --- NAVIGAZIONE ---

if menu == "📊 Visione Globale":
    st.title("EXECUTIVE DASHBOARD")
    n_alerts, tot_fatturato, health = calcola_metriche_e_aggiorna_stato(st.session_state.db_contratti)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Contratti In Essere", f"{len(st.session_state.db_contratti)}")
    with col2: st.metric("Critical Alerts", f"{n_alerts}")
    with col3: st.metric("Volume d'Affari", f"€ {tot_fatturato:,.2f}")
    with col4: st.metric("Portfolio Health", f"{health:.1f}%")

    st.markdown("---")
    
    # Notifiche Email (Invariate)
    if n_alerts > 0:
        email_target = st.text_input("Email per il report:", "tua_email@esempio.it")
        if st.button("📧 INVIA NOTIFICHE EMAIL"):
            critici = st.session_state.db_contratti[st.session_state.db_contratti['Stato'].str.contains("⚠️|🚫")]
            for _, row in critici.iterrows():
                send_expiry_email(email_target, row['Cliente'], row['Scadenza'])
            st.success("Notifiche inviate!")

    st.subheader("Database Contratti & Cloud Storage")
    if not st.session_state.db_contratti.empty:
        # Visualizzazione tabella (senza mostrare il path tecnico del file)
        st.dataframe(st.session_state.db_contratti.drop(columns=['File_Path']), use_container_width=True)
        
        # --- DOWNLOAD CLOUD DEI PDF ---
        st.markdown("##### 📥 Recupero File dal Cloud")
        scelta_download = st.selectbox("Seleziona Contratto da scaricare:", st.session_state.db_contratti["Cliente"].unique())
        row_file = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] == scelta_download].iloc[0]
        
        if row_file["File_Path"] != "Nessun File":
            with open(row_file["File_Path"], "rb") as f:
                st.download_button(label=f"Scarica PDF di {scelta_download}", data=f, file_name=f"Contratto_{scelta_download}.pdf", mime="application/pdf")
        else:
            st.warning("Nessun file PDF associato a questo record.")

        with st.expander("⚙️ Azioni Rapide Database"):
            cliente_sel = st.selectbox("Cliente da eliminare:", st.session_state.db_contratti["Cliente"].unique())
            if st.button("🗑️ ELIMINA"):
                st.session_state.db_contratti = st.session_state.db_contratti[st.session_state.db_contratti["Cliente"] != cliente_sel]
                st.rerun()

elif menu == "✍️ Editor Contratti":
    render_smart_editor()

elif menu == "📂 Archivio Documentale":
    st.title("Asset Digitizer")
    file_pdf = st.file_uploader("Carica il PDF originale per il Cloud", type=["pdf"])
    
    c1, c2 = st.columns(2)
    with c1:
        nuovo_cliente = st.text_input("Ragione Sociale Cliente")
        nuovo_settore = st.selectbox("Classe Servizio", ["Manutenzione", "Servizi", "Consulenza", "Appalto d'opera"])
    with c2:
        nuova_scadenza = st.date_input("Scadenza")
        nuovo_fatturato = st.number_input("Valore Annuo (€)", min_value=0.0)

    if st.button("Archivia e Salva nel Cloud"):
        if nuovo_cliente and nuova_scadenza:
            path_salvataggio = "Nessun File"
            
            # --- LOGICA SALVATAGGIO FISICO FILE ---
            if file_pdf is not None:
                nome_file = f"{nuovo_cliente}_{date.today().strftime('%Y%m%d')}.pdf"
                path_salvataggio = os.path.join(UPLOAD_DIR, nome_file)
                with open(path_salvataggio, "wb") as f:
                    f.write(file_pdf.getbuffer())
            
            nuova_riga = {
                "Cliente": nuovo_cliente, "Settore": nuovo_settore, 
                "Scadenza": nuova_scadenza.strftime('%Y-%m-%d'), 
                "Fatturato": nuovo_fatturato, "Stato": "✅ ATTIVO",
                "File_Path": path_salvataggio # Salviamo il percorso del file
            }
            st.session_state.db_contratti = pd.concat([st.session_state.db_contratti, pd.DataFrame([nuova_riga])], ignore_index=True)
            st.success("Asset e File salvati nel Cloud locale!")
            st.balloons()
        else:
            st.error("Inserisci i dati obbligatori.")

elif menu == "🧾 Fatturazione":
    render_billing_assistant()
