import streamlit as st

def render_billing_assistant():
    st.title("Assistente Fatturazione & ISTAT 🧾")
    st.markdown("##### Calcolo dei componenti fiscali e adeguamento canoni a norma di legge.")

    tab1, tab2 = st.tabs(["🧮 Calcolatore Fattura", "📈 Adeguamento ISTAT"])

    with tab1:
        st.subheader("Predisposizione Dati Fattura")
        col1, col2 = st.columns(2)
        
        with col1:
            imponibile = st.number_input("Imponibile Lordo (€)", min_value=0.0, step=100.0, value=1000.0)
            iva_perc = st.selectbox("Aliquota IVA (%)", [22, 10, 5, 4, 0])
            cassa_perc = st.number_input("Cassa Previdenziale (%)", min_value=0, max_value=10, value=0)
        
        with col2:
            ritenuta = st.checkbox("Applica Ritenuta d'Acconto (20%)")
            bollo = st.checkbox("Marca da Bollo (€ 2,00)", value=imponibile > 77.47 and iva_perc == 0)

        # Calcoli
        valore_cassa = imponibile * (cassa_perc / 100)
        base_iva = imponibile + valore_cassa
        valore_iva = base_iva * (iva_perc / 100)
        totale_fattura = base_iva + valore_iva
        
        valore_ritenuta = imponibile * 0.20 if ritenuta else 0
        netto_a_pagare = totale_fattura - valore_ritenuta + (2.0 if bollo else 0)

        st.markdown("---")
        st.write("### Riepilogo Documento")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.write(f"**Imponibile:** € {imponibile:,.2f}")
            st.write(f"**Cassa ({cassa_perc}%):** € {valore_cassa:,.2f}")
            st.write(f"**IVA ({iva_perc}%):** € {valore_iva:,.2f}")
        with res_col2:
            st.write(f"**Ritenuta d'Acconto:** - € {valore_ritenuta:,.2f}")
            if bollo: st.write("**Marca da Bollo:** € 2,00")
            st.subheader(f"Netto a Pagare: € {netto_a_pagare:,.2f}")

    with tab2:
        st.subheader("Calcolo Adeguamento ISTAT")
        st.info("In Italia, l'adeguamento si calcola solitamente applicando il 75% o il 100% della variazione dell'indice FOI.")
        
        canone_attuale = st.number_input("Canone Annuo Attuale (€)", min_value=0.0, value=12000.0)
        variazione_istat = st.number_input("Variazione Indice ISTAT FOI (%)", min_value=-10.0, max_value=20.0, value=2.0, help="Dato fornito mensilmente dall'ISTAT")
        quota_adeguamento = st.radio("Quota di adeguamento da applicare:", [100, 75], index=0)
        
        # Calcolo: Nuovo Canone = Canone * (1 + (Variazione * Quota/100))
        variazione_effettiva = (variazione_istat * (quota_adeguamento / 100)) / 100
        nuovo_canone = canone_attuale * (1 + variazione_effettiva)
        differenza_mensile = (nuovo_canone - canone_attuale) / 12

        st.markdown("---")
        st.success(f"**Nuovo Canone Annuo Adeguato:** € {nuovo_canone:,.2f}")
        st.write(f"L'incremento totale annuo è di € {nuovo_canone - canone_attuale:,.2f}")
        st.write(f"L'impatto sul canone mensile è di **+ € {differenza_mensile:,.2f}**")
        
        st.caption("Nota: Ricorda di inviare comunicazione scritta al cliente per l'applicazione dell'adeguamento.")
