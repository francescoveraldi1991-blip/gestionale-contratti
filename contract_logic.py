import streamlit as st
from fpdf import FPDF
from datetime import date
import google.generativeai as genai

# Configura l'IA (Sostituisci con la tua chiave o usa i Secrets di Streamlit)
def init_ai():
    api_key = st.sidebar.text_input("Inserisci Gemini API Key 🔑", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def render_smart_editor():
    st.title("AI Legal Drafter 🤖⚖️")
    st.markdown("##### Scrivi i dettagli e lascia che l'intelligenza artificiale rediga il contratto per te.")

    ai_ready = init_ai()

    if not ai_ready:
        st.warning("👈 Per favore, inserisci la tua API Key nella barra laterale per attivare l'Intelligenza Artificiale.")
        return

    # --- INPUT PER L'IA ---
    with st.container():
        st.subheader("Istruzioni per l'IA")
        descrizione = st.text_area(
            "Descrivi l'accordo (es: Contratto di fornitura software tra Azienda X e Y, durata 2 anni, pagamento trimestrale):",
            placeholder="Specifica le parti, l'oggetto, il prezzo e eventuali clausole particolari...",
            height=150
        )
        
        col1, col2 = st.columns(2)
        with col1:
            stile = st.selectbox("Tono del contratto:", ["Formale/Standard", "Protettivo per l'Appaltatore", "Protettivo per il Committente"])
        with col2:
            include_vessatorie = st.checkbox("Includi doppia firma (Art. 1341-1342 CC)", value=True)

    if st.button("🪄 GENERA BOZZA CON IA"):
        if descrizione:
            with st.spinner("L'IA sta redigendo il contratto secondo la legge italiana..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # PROMPT PROFESSIONALE
                    prompt = f"""
                    Agisci come un avvocato esperto in diritto civile italiano. 
                    Scrivi una bozza di contratto basata su queste istruzioni: {descrizione}.
                    Usa uno stile {stile}. 
                    Assicurati di includere:
                    - Articoli numerati.
                    - Riferimenti al Codice Civile italiano pertinenti.
                    - Spazi vuoti [_________] per i dati mancanti.
                    - Se richiesto (vessatorie={include_vessatorie}), aggiungi in fondo la clausola di doppia firma ex artt. 1341-1342 c.c.
                    Restituisci solo il testo del contratto.
                    """
                    
                    response = model.generate_content(prompt)
                    st.session_state.testo_generato = response.text
                except Exception as e:
                    st.error(f"Errore IA: {e}")
        else:
            st.error("Descrivi almeno brevemente l'accordo prima di generare.")

    # --- EDITOR DI TESTO ---
    st.markdown("---")
    st.subheader("Editor della Bozza")
    
    # Recupera il testo generato o usa uno placeholder
    testo_iniziale = st.session_state.get('testo_generato', "Il testo generato apparirà qui...")
    testo_finale = st.text_area("Puoi modificare il testo generato qui:", value=testo_iniziale, height=500)

    # --- ESPORTAZIONE PDF (Versione Robusta) ---
    if st.button("🚀 GENERA PDF UFFICIALE"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(left=20, top=20, right=20)
            pdf.set_font("Helvetica", size=11)
            
            # Pulizia testo per PDF
            testo_clean = testo_finale.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(w=170, h=7, txt=testo_clean, border=0, align='L')
            
            pdf_output = pdf.output()
            st.download_button(
                label="📥 Scarica PDF",
                data=bytes(pdf_output),
                file_name=f"Bozza_Contratto_{date.today()}.pdf",
                mime="application/pdf"
            )
            st.success("Contratto pronto per la firma!")
        except Exception as e:
            st.error(f"Errore creazione PDF: {e}")
