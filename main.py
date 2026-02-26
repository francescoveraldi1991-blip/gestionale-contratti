import streamlit as st
import pandas as pd
import os
import frontmatter # Questa libreria serve per leggere lo YAML nei file markdown

st.set_page_config(page_title="Gestionale Contratti ISTAT", layout="wide")

st.title("Business Contract Manager 📊")
st.write("Benvenuto nel tuo gestionale contratti su GitHub + Streamlit.")

# Funzione per leggere i contratti dalla cartella _contratti
def carica_contratti():
    lista_contratti = []
    path_contratti = "_contratti"
    
    if os.path.exists(path_contratti):
        for file in os.listdir(path_contratti):
            if file.endswith(".md"):
                with open(os.path.join(path_contratti, file), encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    # Aggiungiamo i dati dello YAML alla nostra lista
                    dati = post.metadata
                    dati['file_name'] = file
                    lista_contratti.append(dati)
    return lista_contratti

# Mostriamo la tabella
contratti = carica_contratti()
if contratti:
    df = pd.DataFrame(contratti)
    # Selezioniamo solo le colonne che ci interessano per la Home
    colonne_view = ['id', 'cliente_fornitore', 'scadenza_naturale', 'importo_base']
    st.table(df[colonne_view])
else:
    st.warning("Nessun contratto trovato nella cartella _contratti.")

st.sidebar.info("Usa il menu a sinistra per aggiungere nuovi contratti o calcolare l'ISTAT.")
