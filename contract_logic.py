import streamlit as st
from fpdf import FPDF
from datetime import date

def render_smart_editor():
    # TITOLO DELLA PAGINA NELL'APP
    st.title("Smart Legal Editor ⚖️")
    st.markdown("##### Assistente alla redazione contrattuale conforme alla legge italiana.")

    # --- 1. SEZIONE INPUT UTENTE (NON MODIFICATA) ---
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

    # --- 2. LOGICA GIURIDICA E COSTRUZIONE TESTO (NON MODIFICATA) ---
    testo_legale = f"CONTRATTO DI {tipo_contratto.upper()}\n\n"
    testo_legale += f"DATA: {date.today().strftime('%d/%m/%Y')}\n\n"
    
    if tipo_cliente == "Privato (Consumatore)":
        testo_legale += "DISCIPLINA APPLICABILE: CODICE DEL CONSUMO (D.Lgs. 206/2005)\n"
        testo_legale += "Nota: Il presente rapporto è soggetto alle tutele inderogabili a favore del consumatore.\n\n"
    else:
        testo_legale += "DISCIPLINA APPLICABILE: CODICE CIVILE (Art. 1655 e ss.)\n"
        testo_legale += "Nota: Rapporto disciplinato dalle norme ordinarie sul contratto d'appalto tra professionisti.\n\n"

    testo_legale += "Art. 1 (OGGETTO): L'appaltatore si impegna all'esecuzione delle opere descritte nel capitolato allegato, operando con organizzazione di mezzi propri e gestione a proprio rischio.\n"

    if fideiussione:
        testo_legale += "\nArt. 2 (FIDEIUSSIONE): A garanzia dell'esatto adempimento di tutte le obbligazioni, l'appaltatore consegna polizza fideiussoria a prima richiesta.\n"
    
    if cauzione:
        testo_legale += "\nArt. 3 (CAUZIONE): Viene costituito un deposito cauzionale a tutela di eventuali vizi o difformità dell'opera.\n"

    if clausole_vessatorie:
        testo_legale += "\n--- APPROVAZIONE SPECIFICA CLAUSOLE ---\n"
        testo_legale += "Ai sensi e per gli effetti degli artt. 1341 e 1342 c.c., le parti dichiarano di aver letto e approvato specificamente le clausole relative a: Foro Competente, Limitazioni di Responsabilità, Penali e Facoltà di Recesso.\n"
        testo_legale += "\nFirma del Committente: ______________________\n"

    st.markdown("---")
    st.subheader("Anteprima Documento")
    # Area di testo modificabile dall'utente
    testo_per_pdf = st.text_area("Bozza Generata (puoi aggiungere dettagli qui):", value=testo_legale, height=400)

    # --- 3. GENERAZIONE PDF (CON FIX SPAZIO ORIZZONTALE E LOGO) ---
    if st.button("🚀 GENERA E SCARICA PDF"):
        try:
            # Inizializzazione PDF (A4, millimetri)
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            
            # Impostiamo margini fissi per evitare l'errore "horizontal space"
            pdf.set_margins(left=20, top=20, right=20)
            pdf.add_page()
            
            # --- AGGIUNTA LOGO / INTESTAZIONE ---
            # Se hai un file "logo.png" nella cartella, puoi usare: pdf.image("logo.png", x=85, y=10, w=40)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(15, 23, 42) # Colore Blu Notte (come la tua sidebar)
            pdf.cell(w=0, h=10, txt="ELITE MANAGEMENT SUITE", border=0, ln=True, align='C')
            
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(150, 150, 150) # Grigio per il payoff
            pdf.cell(w=0, h=5, txt="Eccellenza nella Gestione Contrattuale", border=0, ln=True, align='C')
            
            # Linea di separazione oro (simulata con un rettangolo sottile)
            pdf.set_fill_color(251, 191, 36) # Colore Oro
            pdf.rect(x=20, y=40, w=170, h=0.5, style='F')
            
            pdf.ln(20) # Spazio dopo l'intestazione
            
            # --- CORPO DEL TESTO ---
            pdf.set_font("Helvetica", size=11)
            pdf.set_text_color(0, 0, 0) # Nero per il testo
            
            # Calcolo larghezza sicura (210mm - 20mm margine sx - 20mm margine dx = 170mm)
            larghezza_sicura = 170
            
            # Pulizia del testo per evitare caratteri non supportati
            testo_pulito = testo_per_pdf.encode('latin-1', 'replace').decode('latin-1')
            
            # Scrittura con multi_cell (gestisce automaticamente gli a capo)
            # w=larghezza_sicura risolve l'errore dello spazio orizzontale
            pdf.multi_cell(w=larghezza_sicura, h=7, txt=testo_pulito, border=0, align='L')
            
            # Output finale
            pdf_output = pdf.output()
            
            # Pulsante di download Streamlit
            st.download_button(
                label="📥 Scarica ora il tuo Contratto PDF",
                data=bytes(pdf_output),
                file_name=f"Contratto_Elite_{date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("PDF generato con successo!")
            
        except Exception as e:
            st.error(f"Errore tecnico durante la conversione: {e}")
