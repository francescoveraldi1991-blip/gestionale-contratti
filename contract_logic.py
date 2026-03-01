import streamlit as st
from fpdf import FPDF
from datetime import date

def render_smart_editor():
    st.title("Smart Legal Editor ⚖️")
    st.markdown("##### Assistente alla redazione contrattuale conforme alla legge italiana.")

    # --- INPUT UTENTE (Invariati) ---
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

    # --- LOGICA GIURIDICA (Invariata) ---
    testo_legale = f"CONTRATTO DI {tipo_contratto.upper()}\n\n"
    
    if tipo_cliente == "Privato (Consumatore)":
        testo_legale += "Disciplina: CODICE DEL CONSUMO (D.Lgs. 206/2005)\n"
        testo_legale += "Nota: Soggetto alle tutele del consumatore.\n\n"
    else:
        testo_legale += "Disciplina: CODICE CIVILE (Appalto B2B - Art. 1655 e ss.)\n\n"

    testo_legale += "Art. 1 - OGGETTO: L'appaltatore si impegna a eseguire le opere a regola d'arte.\n"

    if fideiussione:
        testo_legale += "\nArt. 2 - GARANZIA: Prestata fideiussione a prima richiesta.\n"
    
    if cauzione:
        testo_legale += "\nArt. 3 - CAUZIONE: Deposito cauzionale del 10%.\n"

    if clausole_vessatorie:
        testo_legale += "\n--- CLAUSOLE VESSATORIE ---\n"
        testo_legale += "Ai sensi degli artt. 1341 e 1342 c.c., si approvano specificamente: Foro competente, Limitazioni responsabilità, Penali.\n"
        testo_legale += "\nFirma del Committente: ______________________\n"

    st.markdown("---")
    st.subheader("Anteprima Documento")
    testo_finale = st.text_area("Bozza Generata:", value=testo_legale, height=350)

    # --- GENERAZIONE PDF CORRETTA ---
    if st.button("🚀 GENERA E SCARICA PDF"):
        try:
            # Inizializzazione PDF con margini espliciti
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.set_margins(left=20, top=20, right=20)
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            
            # Pulizia del testo da caratteri che rompono il layout (es: Tabulatori)
            testo_pulito = testo_finale.replace('\t', '    ')
            
            # Scrittura riga per riga per evitare errori di spazio orizzontale
            for riga in testo_pulito.split('\n'):
                if riga.strip() == "":
                    pdf.ln(6) # Salta una riga se vuota
                else:
                    # multi_cell con larghezza calcolata (w=0 usa tutta la riga tra i margini)
                    pdf.multi_cell(w=0, h=8, txt=riga, border=0, align='L')
            
            # Conversione in bytes per lo scaricamento
            pdf_output = pdf.output()
            
            st.download_button(
                label="📥 Scarica Contratto PDF",
                data=bytes(pdf_output),
                file_name=f"Contratto_{tipo_cliente}_{date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("Documento pronto!")
            
        except Exception as e:
            st.error(f"Errore tecnico nella creazione del PDF: {e}")
