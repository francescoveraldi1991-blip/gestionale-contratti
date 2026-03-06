import streamlit as st
from fpdf import FPDF
from datetime import date
import google.generativeai as genai

def render_smart_editor():
    st.title("AI Legal Drafter 🤖⚖️")
    st.markdown("##### Redazione contrattuale intelligente assistita dall'Intelligenza Artificiale.")

    # --- SEZIONE CHIAVE API ---
    with st.expander("🔑 CONFIGURAZIONE AI", expanded=True):
        api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                st.success("IA pronta all'uso!")
            except Exception as e:
                st.error(f"Errore configurazione: {e}")

    st.markdown("---")

    # --- INPUT ---
    st.subheader("1. Definizione dell'Accordo")
    col_input, col_style = st.columns([2, 1])
    
    with col_input:
        descrizione = st.text_area(
            "Cosa deve contenere il contratto?",
            placeholder="Descrivi l'accordo qui...",
            height=150
        )
    
    with col_style:
        stile = st.radio("Tono legale:", ["Standard / Equilibrato", "Rigido / Protettivo", "Semplificato"])
        include_vessatorie = st.checkbox("Clausole vessatorie (Art. 1341-1342 CC)", value=True)

    if st.button("🪄 GENERA BOZZA CON INTELLIGENZA ARTIFICIALE"):
        if not api_key:
            st.error("⚠️ Inserisci la API Key!")
        elif not descrizione:
            st.error("⚠️ Descrivi l'accordo.")
        else:
            with st.spinner("L'IA sta scrivendo il contratto..."):
                try:
                    # PROVA 1: Il nome modello più standard e aggiornato
                    # In alcune versioni vecchie della libreria serve solo 'gemini-pro'
                    # Nelle nuove serve 'gemini-1.5-flash'
                    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
                    
                    prompt = f"""
                    Agisci come un avvocato civilista italiano esperto in contrattualistica.
                    Scrivi un contratto formale e legalmente valido basato su: {descrizione}.
                    Stile: {stile}. Cita gli articoli del Codice Civile italiano pertinenti.
                    Se richiesto (vessatorie={include_vessatorie}), aggiungi la doppia firma artt. 1341-1342 cc.
                    Restituisci solo il testo del contratto, senza introduzioni.
                    """
                    
                    # Generazione del contenuto
                    response = model.generate_content(prompt)
                    
                    if response:
                        st.session_state['ai_contract_draft'] = response.text
                        st.success("Bozza generata con successo!")
                except Exception as e:
                    # Se fallisce con 1.5-flash, proviamo automaticamente con il modello base 'gemini-pro'
                    try:
                        model_alt = genai.GenerativeModel(model_name='gemini-pro')
                        response_alt = model_alt.generate_content(prompt)
                        st.session_state['ai_contract_draft'] = response_alt.text
                        st.success("Bozza generata con successo (Modello Compatibility)!")
                    except Exception as e2:
                        st.error(f"Errore critico di connessione ai modelli Google: {e2}")

    # --- REVISIONE E PDF (Indentazione corretta a 4 spazi) ---
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
                
                testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(w=170, h=6, txt=testo_clean, border=0, align='L')
                
                pdf_output = pdf.output()
                st.download_button(
                    label="📥 SCARICA PDF",
                    data=bytes(pdf_output),
                    file_name=f"Contratto_Elite_{date.today().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Errore PDF: {e}")
