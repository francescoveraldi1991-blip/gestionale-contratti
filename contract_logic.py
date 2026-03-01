import streamlit as st
from fpdf import FPDF

def render_smart_editor():
    st.title("Smart Legal Editor ⚖️")
    st.markdown("##### Assistente alla redazione contrattuale conforme alla legge italiana.")

    # --- INPUT UTENTE ---
    with st.container():
        st.subheader("1. Qualificazione delle Parti")
        tipo_cliente = st.radio("Il Committente è:", ["Privato (Consumatore)", "Azienda/Professionista (Business)"])
        
        st.subheader("2. Oggetto del Contratto")
        tipo_contratto = st.selectbox("Seleziona disciplina:", [
            "Appalto d'opera/servizi", 
            "Contratto di Manutenzione", 
            "Fornitura con posa in opera"
        ])
        
        st.subheader("3. Garanzie e Tutela")
        col1, col2 = st.columns(2)
        with col1:
            fideiussione = st.checkbox("Prevedere Fideiussione Bancaria/Assicurativa")
            cauzione = st.checkbox("Prevedere Deposito Cauzionale")
        with col2:
            clausole_vessatorie = st.checkbox("Inserire Doppia Firma (Art. 1341-1342 CC)", value=True)

    # --- LOGICA GIURIDICA ---
    testo_legale = f"CONTRATTO DI {tipo_contratto.upper()}\n\n"
    
    if tipo_cliente == "Privato (Consumatore)":
        testo_legale += "Disciplina: CODICE DEL CONSUMO (D.Lgs. 206/2005)\n"
        testo_legale += "Nota: Il presente contratto è soggetto alle tutele del consumatore, incluse le norme sul foro competente e il recesso.\n\n"
    else:
        testo_legale += "Disciplina: CODICE CIVILE (Appalto tra privati - Art. 1655 e ss.)\n"
        testo_legale += "Nota: Rapporto disciplinato dalle norme ordinarie sul contratto d'appalto B2B.\n\n"

    testo_legale += "Art. 1 - OGGETTO: L'appaltatore si impegna a eseguire le opere secondo le regole dell'arte...\n"

    if fideiussione:
        testo_legale += "\nArt. 2 - GARANZIA: L'appaltatore presta fideiussione a prima richiesta per l'adempimento delle obbligazioni contrattuali.\n"
    
    if cauzione:
        testo_legale += "\nArt. 3 - CAUZIONE: È previsto un deposito cauzionale pari al 10% dell'importo totale.\n"

    if clausole_vessatorie:
        testo_legale += "\n--- CLAUSOLE VESSATORIE ---\n"
        testo_legale += "Ai sensi degli artt. 1341 e 1342 c.c., il Committente dichiara di aver letto e approvato specificamente le clausole relative a:\n"
        testo_legale += "- Foro competente e risoluzione controversie\n- Limitazioni di responsabilità\n- Sospensione dei lavori e penali\n"
        testo_legale += "\nFirma del Committente: ______________________\n"

    st.markdown("---")
    st.subheader("Anteprima Documento")
    testo_finale = st.text_area("Bozza Generata (modificabile):", value=testo_legale, height=350)

    # --- FIX ERRORE: GENERAZIONE PDF ---
    if st.button("🚀 GENERA E SCARICA PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            # Usiamo Helvetica (standard) per evitare problemi di encoding
            pdf.set_font("Helvetica", size=12)
            
            # Dividiamo il testo per righe per scriverlo correttamente nel PDF
            for riga in testo_finale.split('\n'):
                pdf.multi_cell(0, 8, riga)
            
            # --- IL FIX: Trasformiamo l'output in bytes ---
            pdf_bytes = pdf.output()
            
            st.download_button(
                label="📥 Clicca qui per il Download",
                data=bytes(pdf_bytes), # Conversione esplicita in bytes
                file_name=f"Contratto_Elite_{date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("PDF pronto per il download!")
        except Exception as e:
            st.error(f"Errore durante la creazione del PDF: {e}")

from datetime import date # Assicuriamoci che date sia disponibile per il file_name
