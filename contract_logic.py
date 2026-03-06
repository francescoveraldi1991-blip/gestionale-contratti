import streamlit as st
from fpdf import FPDF
from datetime import date
import requests
import json

def render_smart_editor():
    st.title("AI Legal Drafter 🤖⚖️")
    st.markdown("##### Sistema di Redazione con Chiamata Diretta API (Bypass 404)")

    # --- SEZIONE CHIAVE API ---
    with st.expander("🔑 CONFIGURAZIONE AI", expanded=True):
        api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password")
        if api_key:
            st.success("Chiave inserita. Il sistema proverà la connessione diretta.")

    st.markdown("---")

    # --- INPUT ---
    st.subheader("1. Definizione dell'Accordo")
    col_input, col_style = st.columns([2, 1])
    
    with col_input:
        descrizione = st.text_area("Cosa deve contenere il contratto?", height=150)
    
    with col_style:
        stile = st.radio("Tono legale:", ["Standard", "Rigido", "Semplice"])
        include_vessatorie = st.checkbox("Artt. 1341-1342 CC", value=True)

    if st.button("🪄 GENERA BOZZA CON INTELLIGENZA ARTIFICIALE"):
        if not api_key:
            st.error("Inserisci la API Key!")
        elif not descrizione:
            st.error("Descrivi l'accordo.")
        else:
            with st.spinner("Connessione diretta ai server Google in corso..."):
                try:
                    # --- CHIAMATA REST DIRETTA (Bypassa la libreria locale) ---
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    headers = {'Content-Type': 'application/json'}
                    
                    prompt = f"Agisci come avvocato italiano. Scrivi un contratto formale per: {descrizione}. Stile: {stile}. Se richiesto (vessatorie={include_vessatorie}), aggiungi doppia firma artt. 1341-1342 cc. Restituisci solo il testo."
                    
                    data = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }

                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    result = response.json()

                    # Estrazione del testo dalla risposta JSON di Google
                    if "candidates" in result:
                        testo_ia = result["candidates"][0]["content"]["parts"][0]["text"]
                        st.session_state['ai_contract_draft'] = testo_ia
                        st.success("Bozza generata con successo tramite REST API!")
                    else:
                        st.error(f"Errore risposta Google: {result.get('error', {}).get('message', 'Errore sconosciuto')}")
                
                except Exception as e:
                    st.error(f"Errore di connessione: {e}")

    # --- REVISIONE E PDF ---
    st.markdown("---")
    st.subheader("2. Revisione e Modifica")
    testo_per_editor = st.session_state.get('ai_contract_draft', "")
    testo_finale = st.text_area("Revisiona il testo:", value=testo_per_editor, height=450)

    if st.button("🚀 TRASFORMA IN PDF UFFICIALE"):
        if not testo_finale:
            st.warning("Il testo è vuoto.")
        else:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_margins(left=20, top=20, right=20)
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(w=0, h=10, txt="ELITE LEGAL MANAGEMENT SUITE", border=0, ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Helvetica", size=10)
                
                # Pulizia testo
                testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(w=170, h=6, txt=testo_clean, border=0, align='L')
                
                pdf_output = pdf.output()
                st.download_button(label="📥 SCARICA PDF", data=bytes(pdf_output), file_name=f"Contratto_Elite_{date.today()}.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"Errore PDF: {e}")
