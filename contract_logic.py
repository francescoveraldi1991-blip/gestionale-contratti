import streamlit as st
from fpdf import FPDF
from datetime import date
import requests
import json

def render_smart_editor():
    st.title("AI Legal Drafter (Powered by Groq) 🤖⚖️")
    st.markdown("##### Redazione professionale con modelli Llama 3")

    # --- SEZIONE CHIAVE API ---
    with st.expander("🔑 CONFIGURAZIONE GROQ", expanded=True):
        api_key = st.text_input("Inserisci la tua Groq API Key (gsk-...):", type="password")
        if api_key:
            st.success("Chiave Groq configurata correttamente!")
        else:
            st.info("ℹ️ Ottieni la chiave gratis su console.groq.com")

    st.markdown("---")

    # --- 1. INPUT ---
    st.subheader("1. Dettagli del Contratto")
    descrizione = st.text_area("Descrivi l'accordo (es. parti, oggetto, compenso):", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        stile = st.radio("Tono legale:", ["Standard", "Protettivo", "Semplice"])
    with col2:
        include_vessatorie = st.checkbox("Clausole vessatorie (1341-1342 CC)", value=True)

    # --- LOGICA DI GENERAZIONE ---
    if st.button("🪄 GENERA CONTRATTO ORA"):
        if not api_key:
            st.error("⚠️ Inserisci la API Key di Groq!")
        elif not descrizione:
            st.error("⚠️ Inserisci una descrizione.")
        else:
            with st.spinner("L'IA sta elaborando la struttura legale..."):
                try:
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    prompt = f"""
                    Sei un avvocato civilista italiano. Scrivi un contratto formale basato su: {descrizione}.
                    REGOLE:
                    - Usa lo stile {stile}.
                    - Includi riferimenti normativi (Codice Civile).
                    - Usa [_________] per i dati mancanti.
                    - Se richiesto (vessatorie={include_vessatorie}), aggiungi la sezione per la doppia firma ex artt. 1341-1342 c.c.
                    - Lingua: Italiano professionale.
                    Restituisci solo il testo del contratto.
                    """
                    
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "Sei un esperto legale specializzato in diritto civile italiano."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.5 # Più bassa per essere più precisi e meno 'creativi'
                    }

                    response = requests.post(url, headers=headers, json=payload)
                    result = response.json()

                    if response.status_code == 200:
                        testo_ia = result['choices'][0]['message']['content']
                        st.session_state['ai_contract_draft'] = testo_ia
                        st.success("Contratto generato!")
                    else:
                        st.error(f"Errore: {result.get('error', {}).get('message', 'Errore Groq')}")
                
                except Exception as e:
                    st.error(f"Errore di connessione: {e}")

    # --- 2. EDITOR E PDF ---
    st.markdown("---")
    st.subheader("2. Revisione e Stampa")
    testo_finale = st.text_area("Testo del contratto:", value=st.session_state.get('ai_contract_draft', ""), height=450)

    if st.button("🚀 GENERA PDF"):
        if not testo_finale:
            st.warning("Genera prima il testo.")
        else:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_margins(20, 20, 20)
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(0, 10, "DOCUMENTO LEGALE - ELITE MANAGEMENT", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Helvetica", size=10)
                
                # Gestione caratteri speciali
                testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, testo_clean)
                
                st.download_button("📥 Scarica Contratto", data=bytes(pdf.output()), file_name="contratto_generato.pdf")
            except Exception as e:
                st.error(f"Errore PDF: {e}")
