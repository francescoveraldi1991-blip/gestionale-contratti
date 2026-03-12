import streamlit as st
from fpdf import FPDF
from datetime import date
import requests
import json

def render_smart_editor():
    st.title("AI Legal Drafter 🤖⚖️")
    st.markdown("##### Redazione contrattuale professionale tramite Google Gemini API (v1 Stable)")

    # --- SEZIONE CHIAVE API ---
    with st.expander("🔑 CONFIGURAZIONE AI", expanded=True):
        api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password", help="Ottieni la tua chiave su Google AI Studio")
        if api_key:
            st.success("Chiave configurata per la connessione diretta v1.")
        else:
            st.info("ℹ️ Inserisci la chiave API per sbloccare la generazione automatica.")

    st.markdown("---")

    # --- 1. INPUT PER L'IA ---
    st.subheader("1. Dettagli del Contratto")
    col_input, col_style = st.columns([2, 1])
    
    with col_input:
        descrizione = st.text_area(
            "Cosa deve contenere il contratto?",
            placeholder="Esempio: Contratto di fornitura di servizi web tra X e Y, durata 12 mesi, importo 5000€...",
            height=150
        )
    
    with col_style:
        stile = st.radio("Tono legale:", ["Standard / Equilibrato", "Rigido / Protettivo", "Semplificato"])
        include_vessatorie = st.checkbox("Clausole vessatorie (Art. 1341-1342 CC)", value=True)

    # --- LOGICA DI GENERAZIONE ---
    if st.button("🪄 GENERA BOZZA CON INTELLIGENZA ARTIFICIALE"):
        if not api_key:
            st.error("⚠️ Inserisci prima la tua API Key!")
        elif not descrizione:
            st.error("⚠️ Descrivi l'accordo prima di generare.")
        else:
            with st.spinner("L'IA sta redigendo il contratto (Versione v1)..."):
                try:
                    # Endpoint v1 stabile
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    headers = {'Content-Type': 'application/json'}
                    
                    # Costruzione del Prompt
                    prompt_text = f"""
                    Agisci come un avvocato civilista italiano. 
                    Scrivi una bozza di contratto formale basata su queste istruzioni: {descrizione}.
                    Stile richiesto: {stile}.
                    Assicurati di includere:
                    - Articoli numerati e riferimenti al Codice Civile italiano.
                    - Spazi [_________] per i dati sensibili mancanti.
                    - Se richiesto (vessatorie={include_vessatorie}), aggiungi in calce la doppia firma artt. 1341-1342 cc.
                    Restituisci solo il testo del contratto, senza chiacchiere.
                    """
                    
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt_text}]
                        }]
                    }

                    # Chiamata POST
                    response = requests.post(url, headers=headers, json=payload)
                    result = response.json()

                    if response.status_code == 200:
                        # Estrazione sicura del testo
                        testo_generato = result['candidates'][0]['content']['parts'][0]['text']
                        st.session_state['ai_contract_draft'] = testo_generato
                        st.success("Bozza generata correttamente!")
                    else:
                        errore_msg = result.get('error', {}).get('message', 'Errore sconosciuto')
                        st.error(f"Errore API {response.status_code}: {errore_msg}")
                
                except Exception as e:
                    st.error(f"Errore tecnico durante la connessione: {e}")

    # --- 2. AREA DI REVISIONE ---
    st.markdown("---")
    st.subheader("2. Revisione e Modifica")
    
    testo_per_editor = st.session_state.get('ai_contract_draft', "")
    testo_finale = st.text_area("Puoi modificare il testo generato qui:", value=testo_per_editor, height=450)

    # --- 3. GENERAZIONE PDF ---
    if st.button("🚀 TRASFORMA IN PDF UFFICIALE"):
        if not testo_finale:
            st.warning("Il testo è vuoto. Genera una bozza prima.")
        else:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_margins(left=20, top=20, right=20)
                
                # Intestazione PDF
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(w=0, h=10, txt="ELITE MANAGEMENT SUITE - BOZZA LEGALE", border=0, ln=True, align='C')
                pdf.ln(10)
                
                # Corpo del contratto
                pdf.set_font("Helvetica", size=10)
                # Gestione caratteri speciali per PDF standard
                testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(w=170, h=6, txt=testo_clean, border=0, align='L')
                
                pdf_output = pdf.output()
                st.download_button(
                    label="📥 SCARICA PDF",
                    data=bytes(pdf_output),
                    file_name=f"Contratto_Elite_{date.today()}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Errore durante la creazione del PDF: {e}")
