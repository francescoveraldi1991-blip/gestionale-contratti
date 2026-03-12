import streamlit as st
from fpdf import FPDF
from datetime import date
import requests
import json

def render_smart_editor():
    # Forza lo svuotamento della cache se cambi versione (opzionale)
    # st.cache_data.clear() 

    st.title("AI Legal Drafter 🤖⚖️")
    
    with st.expander("🔑 CONFIGURAZIONE AI", expanded=True):
        api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password")
        if api_key:
            st.success("Chiave configurata.")

    st.markdown("---")

    st.subheader("1. Dettagli del Contratto")
    descrizione = st.text_area("Cosa deve contenere il contratto?", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        stile = st.radio("Tono:", ["Standard", "Rigido", "Semplice"])
    with col2:
        include_vessatorie = st.checkbox("Artt. 1341-1342 CC", value=True)

    if st.button("🪄 GENERA BOZZA"):
        if not api_key:
            st.error("Inserisci la API Key!")
        elif not descrizione:
            st.error("Descrivi l'accordo.")
        else:
            with st.spinner("Generazione in corso (Endpoint V1)..."):
                try:
                    # PROVA L'ENDPOINT V1 CON IL MODELLO GEMINI-1.5-FLASH
                    # Ho rimosso ogni riferimento a 'beta'
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    headers = {'Content-Type': 'application/json'}
                    
                    prompt_text = f"Scrivi un contratto legale formale in italiano per: {descrizione}. Stile: {stile}. Se richiesto (vessatorie={include_vessatorie}), aggiungi doppia firma artt. 1341-1342 cc."
                    
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt_text}]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "topK": 40,
                            "topP": 0.95,
                            "maxOutputTokens": 2048,
                        }
                    }

                    response = requests.post(url, headers=headers, json=payload)
                    result = response.json()

                    if response.status_code == 200:
                        testo_ia = result['candidates'][0]['content']['parts'][0]['text']
                        st.session_state['ai_contract_draft'] = testo_ia
                        st.success("Bozza generata!")
                    else:
                        # Se Google risponde ancora con 404, proviamo il modello "gemini-pro" (versione 1.0)
                        st.info("Tentativo con modello alternativo...")
                        url_alt = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                        response_alt = requests.post(url_alt, headers=headers, json=payload)
                        result_alt = response_alt.json()
                        
                        if response_alt.status_code == 200:
                            st.session_state['ai_contract_draft'] = result_alt['candidates'][0]['content']['parts'][0]['text']
                            st.success("Bozza generata con successo!")
                        else:
                            st.error(f"Errore persistente: {result_alt.get('error', {}).get('message', 'Modello non trovato')}")
                
                except Exception as e:
                    st.error(f"Errore tecnico: {e}")

    # --- EDITOR E PDF (Invariati) ---
    st.markdown("---")
    st.subheader("2. Revisione")
    testo_finale = st.text_area("Revisiona qui:", value=st.session_state.get('ai_contract_draft', ""), height=400)

    if st.button("🚀 SCARICA PDF"):
        if testo_finale:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(0, 6, testo_finale.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("📥 Download", data=bytes(pdf.output()), file_name="contratto.pdf")
