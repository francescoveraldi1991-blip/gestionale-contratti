import streamlit as st
from fpdf import FPDF
from datetime import date
import google.generativeai as genai

def render_smart_editor():
    st.title("AI Legal Drafter 🤖⚖️")
    st.markdown("##### Redazione contrattuale intelligente assistita dall'Intelligenza Artificiale.")

    # --- SEZIONE CHIAVE API NEL MENU DELL'EDITOR ---
    with st.expander("🔑 CONFIGURAZIONE AI (Necessaria per iniziare)", expanded=True):
        api_key = st.text_input("Inserisci la tua Gemini API Key:", type="password", help="Ottieni la tua chiave su Google AI Studio")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                st.success("IA configurata correttamente! Puoi procedere alla stesura.")
            except Exception as e:
                st.error(f"Errore di configurazione: {e}")
        else:
            st.info("ℹ️ Inserisci la chiave API per sbloccare le funzioni di generazione automatica.")

    st.markdown("---")

    # --- 1. INPUT PER L'IA ---
    st.subheader("1. Definizione dell'Accordo")
    col_input, col_style = st.columns([2, 1])
    
    with col_input:
        descrizione = st.text_area(
            "Cosa deve contenere il contratto?",
            placeholder="Esempio: Contratto di collaborazione professionale tra lo Studio Rossi e il consulente Bianchi...",
            height=150
        )
    
    with col_style:
        stile = st.radio("Tono legale:", ["Standard / Equilibrato", "Rigido / Protettivo", "Semplificato"])
        include_vessatorie = st.checkbox("Clausole vessatorie (Art. 1341-1342 CC)", value=True)

    # Pulsante per attivare l'IA
    if st.button("🪄 GENERA BOZZA CON INTELLIGENZA ARTIFICIALE"):
        if not api_key:
            st.error("⚠️ Inserisci prima la tua API Key nel riquadro in alto!")
        elif not descrizione:
            st.error("⚠️ Descrivi almeno brevemente l'oggetto del contratto.")
        else:
            with st.spinner("L'IA sta elaborando il testo legale... attendere."):
                try:
                    # Usiamo 'gemini-pro' per la massima compatibilità
                    model = genai.GenerativeModel('gemini-pro')
                    
                    prompt = f"""
                    Agisci come un avvocato civilista italiano esperto in contrattualistica.
                    Scrivi un contratto formale e legalmente valido basato su queste informazioni: {descrizione}.
                    Stile: {stile}. Includi riferimenti al Codice Civile italiano pertinenti.
                    Se richiesto (vessatorie={include_vessatorie}), aggiungi in calce l'approvazione 
                    specifica delle clausole ai sensi degli artt. 1341 e 1342 c.c.
                    Restituisci ESCLUSIVAMENTE il testo del contratto.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.session_state['ai_contract_draft'] = response.text
                        st.success("Bozza generata con successo!")
                    else:
                        st.error("L'IA non ha prodotto testo. Verifica i filtri di sicurezza.")
                except Exception as e:
                    st.error(f"Errore durante la generazione: {e}")

    # --- 2. AREA DI EDITING ---
    st.markdown("---")
    st.subheader("2. Revisione e Modifica")
    
    # Recuperiamo il testo generato o lasciamo vuoto
    testo_per_editor = st.session_state.get('ai_contract_draft', "")
    testo_finale = st.text_area("Revisiona il testo qui sotto:", value=testo_per_editor, height=450)

    # --- 3. GENERAZIONE PDF ---
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
                
                # Pulizia per caratteri speciali latin-1
                testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(w=170, h=6, txt=testo_clean, border=0, align='L')
                
                pdf_output = pdf.output()
                st.download_button(
                    label="📥 SCARICA CONTRATTO PDF",
                    data=bytes(pdf_output),
                    file_name=f"Contratto_Elite_{date.today()}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Errore nella creazione del PDF: {e}")
