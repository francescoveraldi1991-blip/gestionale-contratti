import streamlit as st
from fpdf import FPDF

def render_smart_editor():
    st.title("Smart Legal Editor ⚖️")
    st.markdown("##### Assistente alla redazione contrattuale a norma di legge italiana.")

    with st.container():
        st.subheader("1. Qualificazione delle Parti")
        tipo_cliente = st.radio("Il Committente è:", ["Privato (Consumatore)", "Azienda/Professionista (Business)"])
        
        st.subheader("2. Oggetto del Contratto")
        tipo_contratto = st.selectbox("Seleziona disciplina:", ["Appalto d'opera/servizi tra privati", "Fornitura con posa in opera"])
        
        st.subheader("3. Garanzie e Tutela")
        col1, col2 = st.columns(2)
        with col1:
            fideiussione = st.checkbox("Prevedere Fideiussione Bancaria/Assicurativa")
            cauzione = st.checkbox("Prevedere Deposito Cauzionale")
        with col2:
            clausole_vessatorie = st.checkbox("Inserire Doppia Firma (Art. 1341-1342 CC)", value=True)

    # --- LOGICA GIURIDICA AUTOMATICA ---
    testo_legale = ""
    
    # Disciplina applicabile
    if tipo_cliente == "Privato (Consumatore)":
        disciplina = "Codice del Consumo (D.Lgs. 206/2005)"
        testo_legale += f"Il presente contratto è regolato dal {disciplina}. "
    else:
        disciplina = "Codice Civile (Appalto tra privati - Art. 1655 e ss.)"
        testo_legale += f"Il presente contratto è regolato dal {disciplina}. "

    # Aggiunta Garanzie
    if fideiussione:
        testo_legale += "\n\nArt. Garanzia: L'Appaltatore si impegna a prestare fideiussione a prima richiesta..."
    
    # Clausole Vessatorie
    if clausole_vessatorie:
        testo_legale += "\n\nAi sensi e per gli effetti degli artt. 1341 e 1342 c.c., le parti approvano specificamente le clausole relative a: Limitazioni di responsabilità, Facoltà di recedere, Decadenze..."

    st.markdown("---")
    st.subheader("Anteprima Documento Professionale")
    testo_finale = st.text_area("Bozza Generata (puoi modificarla qui):", 
                                value=f"CONTRATTO DI {tipo_contratto.upper()}\n\n{testo_legale}", 
                                height=300)

    # Funzione per generare PDF
    if st.button("📥 GENERA E SCARICA PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=12) # Usiamo Times per il PDF per massima formalità
        pdf.multi_cell(0, 10, testo_finale)
        
        pdf_output = pdf.output()
        st.download_button(
            label="Clicca qui per il download",
            data=pdf_output,
            file_name=f"Contratto_{tipo_cliente}.pdf",
            mime="application/pdf"
        )
