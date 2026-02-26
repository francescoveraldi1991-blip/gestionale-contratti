import streamlit as st
import pandas as pd
import os
import frontmatter
from datetime import datetime

st.set_page_config(page_title="Gestionale Contratti", layout="wide")

# --- INTERFACCIA ---
st.title("Business Contract Manager 📊")

menu = ["Dashboard Archivio", "Crea Nuovo Contratto"]
scelta = st.sidebar.selectbox("Menu Principale", menu)

# --- FUNZIONE PER CARICARE I DATI ---
def carica_dati():
    lista = []
    path = "_contratti"
    if os.path.exists(path):
        for file in os.listdir(path):
            if file.endswith(".md"):
                with open(os.path.join(path, file), encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    dati = post.metadata
                    # Calcolo giorni rimanenti alla scadenza
                    if 'data_fine' in dati:
                        scadenza = datetime.strptime(dati['data_fine'], '%Y-%m-%d').date()
                        dati['Giorni alla Scadenza'] = (scadenza - datetime.now().date()).days
                    lista.append(dati)
    return lista

# --- LOGICA DELLE PAGINE ---
if scelta == "Dashboard Archivio":
    st.subheader("🗄️ Archivio Contratti Stipulati")
    contratti = carica_dati()
    
    if contratti:
        df = pd.DataFrame(contratti)
        # Riordiniamo le colonne come le vuoi tu
        colonne = ['cliente_nome', 'cliente_cognome', 'data_stipula', 'data_inizio', 'data_fine', 'rinnovo_tacito', 'adeguamento_istat']
        # Mostriamo la tabella interattiva
        st.dataframe(df[colonne], use_container_width=True)
    else:
        st.info("Nessun contratto presente nell'archivio. Usa il menu a sinistra per crearne uno.")

elif scelta == "Crea Nuovo Contratto":
    st.subheader("✍️ Generatore Contratti a Norma di Legge")
    
    with st.form("form_contratto"):
        col1, col2 = st.columns(2)
        with col1:
            settore = st.selectbox("Settore", ["Manutenzione", "Servizi"])
            nome = st.text_input("Nome")
            cognome = st.text_input("Cognome")
        with col2:
            stipula = st.date_input("Data Stipula")
            inizio = st.date_input("Inizio Contratto")
            fine = st.date_input("Fine Contratto")
            
        rinnovo = st.checkbox("Rinnovo Tacito?")
        istat = st.checkbox("Prevedi Adeguamento ISTAT?")
        
        submit = st.form_submit_button("Genera Anteprima e Salva")
        
        if submit:
            st.success(f"Contratto di {settore} generato per {nome} {cognome}!")
            # Qui aggiungeremo in seguito la funzione per salvare il file direttamente su GitHub
