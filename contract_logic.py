import streamlit as st
from fpdf import FPDF
from datetime import date

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

    # --- COSTRUZIONE TESTO ---
    testo_legale = f"CONTRATTO DI {tipo_contratto.upper()}\n\n"
    testo_legale += f"DATA: {date.today().strftime('%d/%m/%Y')}\n\n"
    
    if tipo_cliente == "Privato (Consumatore)":
        testo_legale += "DISCIPLINA APPLICABILE: CODICE DEL CONSUMO (D.Lgs. 206/2005)\n"
    else:
        testo_legale += "DISCIPLINA APPLICABILE: CODICE CIVILE (Art. 1655 e ss.)\n"

    testo_legale += "\nArt. 1 (OGGETTO): L'appaltatore si impegna all'esecuzione delle opere descritte secondo la diligenza professionale e le regole dell'arte.\n"

    if fideiussione:
        testo_legale += "\nArt. 2 (FIDEIUSSIONE): A garanzia delle obbligazioni assunte, viene consegnata fideiussione a prima richiesta.\n"
    
    if cauzione:
        testo_legale += "\nArt. 3 (CAUZIONE): Viene costituito un deposito cauzionale infruttifero.\n"

    if clausole_vessatorie:
        testo_legale += "\n--- APPROVAZIONE SPECIFICA CLAUSOLE ---\n"
        testo_legale += "Ai sensi e per gli effetti degli artt. 1341 e 1342 c.c., le parti dichiarano di aver letto e approvato specificamente le clausole relative a: Foro Competente, Limitazioni di Responsabilità, Penali e Recesso.\n"
        testo_legale += "\nFirma per esteso del Committente: ______________________\n"

    st.markdown("---")
    st.subheader("Anteprima Documento")
    # Il testo viene visualizzato e può essere modificato
    testo_per_pdf = st.text_area("Bozza Generata (puoi aggiungere i dati mancanti qui):", value=testo_legale, height=400)

    # --- GENERAZIONE PDF (VERSIONE ULTRA-STABILE) ---
    if st.button("🚀 GENERA E SCARICA PDF"):
        try:
            # Creazione PDF con parametri espliciti
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()
            
            # Impostiamo il font standard che non dà problemi di encoding
            pdf.set_font("Helvetica", size=11)
            
            # Calcoliamo la larghezza utile della pagina (Pagina - Margini)
            # 210mm (A4) - 20mm (Margine Sinistro) - 20mm (Margine Destro) = 170mm
            larghezza_utile = 170 
            
            # Pulizia preventiva del testo per evitare caratteri speciali "invisibili"
            testo_pulito = testo_per_pdf.encode('latin-1', 'replace').decode('latin-1')
            
            # Scriviamo tutto il blocco di testo in una volta sola. 
            # fpdf2 gestirà automaticamente gli "a capo" e i margini.
            pdf.multi_cell(w=larghezza_utile, h=7, txt=testo_pulito, border=0, align='L')
            
            # Generazione del file binario
            output_pdf = pdf.output()
            
            # Pulsante di download
            st.download_button(
                label="📥 Scarica ora il tuo Contratto PDF",
                data=bytes(output_pdf),
                file_name=f"Contratto_Elite_{date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("Analisi completata. Il PDF è pronto per il download.")
            
        except Exception as e:
            st.error(f"Errore tecnico durante la conversione: {e}")
